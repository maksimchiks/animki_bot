import asyncio
import logging
from highrise import BaseBot, User

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("animki-bot")

timed_emotes = [
    {"value": "sit-idle-cute", "text": "Rest", "time": 17.0},
    {"value": "idle_zombie", "text": "Zombie", "time": 28.7},
    {"value": "dance-russian", "text": "Russian Dance", "time": 10.2},
]

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.tasks = {}

    async def on_ready(self):
        log.info("BOT READY")

    async def on_user_join(self, user: User):
        await self.highrise.chat(
            f"👋 @{user.username}\n"
            f"1–{len(timed_emotes)} — анимации\n"
            f"0 — стоп\n"
            f"ping — проверка"
        )

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()

        if msg == "ping":
            await self.highrise.chat("✅ Я жив")
            return

        if msg == "0":
            await self.stop_anim(user)
            return

        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(timed_emotes):
                await self.start_anim(user, idx)

    async def start_anim(self, user: User, idx: int):
        await self.stop_anim(user)
        em = timed_emotes[idx]

        async def loop():
            try:
                while True:
                    await self.highrise.send_emote(em["value"], user.id)
                    await asyncio.sleep(max(em["time"] - 0.2, 0.2))
            except asyncio.CancelledError:
                pass

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()