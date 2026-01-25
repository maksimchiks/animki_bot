import asyncio
import os
from highrise import BaseBot, Highrise, User
from highrise.models import Emote


ANIMS = [
    {"id": "sit-idle-cute", "time": 17.0},
    {"id": "idle_zombie", "time": 28.7},
]

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.tasks = {}

    async def on_ready(self):
        print("✅ BOT READY")

    async def on_user_join(self, user: User):
        await self.highrise.chat(
            f"👋 @{user.username}\n"
            f"1–{len(ANIMS)} — анимации\n"
            f"0 — стоп\n"
            f"ping — проверка"
        )

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()
        print(f"CHAT {user.username}: {msg}")

        if msg == "ping":
            await self.highrise.chat("✅ Я жив")
            return

        if msg == "0":
            await self.stop_anim(user)
            return

        if msg.isdigit():
            i = int(msg) - 1
            if 0 <= i < len(ANIMS):
                await self.start_anim(user, ANIMS[i])

    async def start_anim(self, user: User, anim):
        await self.stop_anim(user)

        async def loop():
            while True:
                await self.highrise.send_emote(Emote(anim["id"]), user.id)
                await asyncio.sleep(anim["time"])

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()


if __name__ == "__main__":
    ROOM_ID = os.getenv("ROOM_ID")
    API_TOKEN = os.getenv("API_TOKEN")

    bot = Bot()
    app = Highrise(bot, ROOM_ID, API_TOKEN)
    app.run()