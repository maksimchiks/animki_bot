import asyncio
import logging
from highrise import BaseBot, User

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("animki-bot")

# ================= АНИМАЦИИ =================
timed_emotes = [
    {"value": "sit-idle-cute", "text": "Rest", "time": 17.06},
    {"value": "idle_zombie", "text": "Zombie", "time": 28.75},
    {"value": "idle_layingdown2", "text": "Relaxed", "time": 21.54},
    {"value": "idle-loop-happy", "text": "Chillin'", "time": 18.79},
    {"value": "idle-loop-tapdance", "text": "Tap Loop", "time": 6.26},
    {"value": "emote-wave", "text": "Wave", "time": 2.7},
    {"value": "emote-disco", "text": "Disco", "time": 5.36},
    {"value": "emote-gangnam", "text": "Gangnam", "time": 7.27},
    {"value": "emoji-thumbsup", "text": "Thumbs Up", "time": 2.7},
]

# ================= БОТ =================
class Bot(BaseBot):

    def __init__(self):
        super().__init__()
        self.tasks: dict[str, asyncio.Task] = {}

    async def on_start(self):
        log.info("BOT STARTED AND READY")
        await self.highrise.chat(
            "🤖 Бот онлайн!\n"
            "🎭 Напиши номер анимации\n"
            "📜 list — список\n"
            "🛑 0 — остановить\n"
            "📡 ping — проверить бота"
        )

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

        if msg == "ping":
            await self.highrise.chat("🏓 pong — я жив")
            return

        if msg == "0":
            await self.stop_anim(user)
            await self.highrise.chat(f"🛑 @{user.username} анимация остановлена")
            return

        if msg in ("list", "анимки"):
            text = "🎭 АНИМАЦИИ:\n"
            for i, e in enumerate(timed_emotes, 1):
                text += f"{i}. {e['text']}\n"
            await self.highrise.chat(text)
            return

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
                    await asyncio.sleep(max(em["time"] - 0.2, 0.1))
            except asyncio.CancelledError:
                log.info(f"Animation stopped for {user.username}")

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()