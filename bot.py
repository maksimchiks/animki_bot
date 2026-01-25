import asyncio
import os
import logging
from highrise import BaseBot, User
from highrise import BotRunner

# ================= ЛОГИ =================
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("animki-bot")

# ================= АНИМАЦИИ =================
timed_emotes = [
    {"value": "sit-idle-cute", "text": "Rest", "time": 17.06},
    {"value": "idle_zombie", "text": "Zombie", "time": 28.75},
    {"value": "idle_layingdown2", "text": "Relaxed", "time": 21.54},
    {"value": "idle_layingdown", "text": "Attentive", "time": 24.58},
    {"value": "idle-sleep", "text": "Sleepy", "time": 22.62},
    {"value": "idle-sad", "text": "Pouty Face", "time": 24.37},
    {"value": "idle-posh", "text": "Posh", "time": 21.85},
    {"value": "idle-loop-happy", "text": "Chillin'", "time": 18.79},
    {"value": "idle-angry", "text": "Irritated", "time": 25.42},
    {"value": "emote-wave", "text": "Wave", "time": 2.7},
    {"value": "emote-dab", "text": "Dab", "time": 2.7},
    {"value": "emote-hello", "text": "Hello", "time": 2.7},
    {"value": "dance-russian", "text": "Russian Dance", "time": 10.25},
    {"value": "dance-floss", "text": "Floss", "time": 21.32},
]

# ================= БОТ =================
class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.tasks: dict[str, asyncio.Task] = {}

    async def on_ready(self):
        log.info("BOT CONNECTED AND READY")

    async def on_user_join(self, user: User):
        await self.highrise.chat(
            f"👋 @{user.username}\n"
            f"🎭 Напиши номер анимации (1–{len(timed_emotes)})\n"
            f"📜 list — список\n"
            f"🛑 0 — остановить\n"
            f"📡 ping — проверить бота"
        )

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()

        # PING
        if msg == "ping":
            await self.highrise.chat("✅ Я жив и работаю 24/7")
            return

        # STOP = 0
        if msg == "0":
            await self.stop_anim(user)
            await self.highrise.chat(f"⛔ @{user.username} анимация остановлена")
            return

        # LIST
        if msg == "list":
            text = "🎭 АНИМАЦИИ:\n"
            for i, e in enumerate(timed_emotes, 1):
                text += f"{i}. {e['text']}\n"
            await self.highrise.chat(text)
            return

        # START ANIMATION
        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(timed_emotes):
                await self.start_anim(user, idx)

    async def start_anim(self, user: User, idx: int):
        await self.stop_anim(user)
        em = timed_emotes[idx]

        async def loop():
            log.info(f"Start animation {em['value']} for {user.username}")
            try:
                while True:
                    await self.highrise.send_emote(em["value"], user.id)
                    await asyncio.sleep(max(em["time"] - 0.3, 0.2))
            except asyncio.CancelledError:
                log.info(f"Animation stopped for {user.username}")

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()

# ================= ЗАПУСК (ВАЖНО) =================
if __name__ == "__main__":
    log.info("=== BOT STARTING ===")

    BotRunner.run(
        bot_definition=Bot,
        api_token=os.getenv("HIGHRISE_API_TOKEN"),
        room_id=os.getenv("HIGHRISE_ROOM_ID"),
    )