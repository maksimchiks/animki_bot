import asyncio
from highrise import BotDefinition, User
from highrise.models import Emote

tasks = {}

emotes = [
    {"id": "sit-idle-cute", "time": 17.0},
    {"id": "idle_zombie", "time": 28.7},
]

bot = BotDefinition("AnimkisBot")


@bot.event
async def on_ready(ctx):
    print("BOT READY")


@bot.event
async def on_user_join(ctx, user: User):
    await ctx.send_chat(
        f"👋 @{user.username}\n"
        f"1–{len(emotes)} — анимации\n"
        f"0 — стоп\n"
        f"ping — проверка"
    )


@bot.event
async def on_chat(ctx, user: User, message: str):
    msg = message.strip().lower()
    print(f"CHAT {user.username}: {msg}")

    if msg == "ping":
        await ctx.send_chat("✅ Я жив")
        return

    if msg == "0":
        await stop_anim(ctx, user)
        return

    if msg.isdigit():
        i = int(msg) - 1
        if 0 <= i < len(emotes):
            await start_anim(ctx, user, emotes[i])


async def start_anim(ctx, user, emote):
    await stop_anim(ctx, user)

    async def loop():
        while True:
            await ctx.send_emote(Emote(emote["id"]), user.id)
            await asyncio.sleep(max(emote["time"] - 0.2, 0.2))

    tasks[user.id] = asyncio.create_task(loop())


async def stop_anim(ctx, user):
    task = tasks.pop(user.id, None)
    if task:
        task.cancel()