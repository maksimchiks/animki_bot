import asyncio
import logging
from highrise import BaseBot, User

# ================= ЛОГИ =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("ANIMKI_BOT")

# ================= АНИМАЦИИ =================
timed_emotes = [
    # ⬇️ ТВОЙ СПИСОК БЕЗ ИЗМЕНЕНИЙ
    {"value": "sit-idle-cute", "text": "Rest", "time": 17.062613},
    {"value": "idle_zombie", "text": "Zombie", "time": 28.754937},
    {"value": "idle_layingdown2", "text": "Relaxed", "time": 21.546653},
    {"value": "idle_layingdown", "text": "Attentive", "time": 24.585168},
    {"value": "idle-sleep", "text": "Sleepy", "time": 22.620446},
    {"value": "idle-sad", "text": "Pouty Face", "time": 24.377214},
    
]

# ================= БОТ =================
class Bot(BaseBot):

    def init(self):
        super().init()
        self.tasks: dict[str, asyncio.Task] = {}
        self.heartbeat_task: asyncio.Task | None = None
        log.info("Bot init completed")

    async def on_start(self):
        log.info("Bot connected to Highrise")
        self.heartbeat_task = asyncio.create_task(self.heartbeat())

    async def heartbeat(self):
        try:
            while True:
                log.info("[HEARTBEAT] bot is alive")
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            log.warning("Heartbeat stopped")

    # ❌ НЕТ приветствия
    async def on_user_join(self, user: User):
        log.info(f"User joined: @{user.username}")

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()
        log.info(f"Chat from @{user.username}: {msg}")

        if msg == "stop":
            await self.stop_anim(user)
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
        log.info(f"Start animation {em['value']} for @{user.username}")

        async def loop():
            try:
                while True:
                    await self.highrise.send_emote(em["value"], user.id)
                    await asyncio.sleep(max(em["time"] - 0.3, 0.1))
            except asyncio.CancelledError:
                log.info(f"Animation stopped for @{user.username}")

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()
            log.info(f"Stopped animation for @{user.username}")