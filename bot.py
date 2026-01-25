import asyncio
import time
import os
from highrise import BaseBot, User, Highrise

# ================== АНИМАЦИИ ==================

timed_emotes = [
    # ⬇️ ТВОЙ СПИСОК (Я ЕГО НЕ ТРОГАЛ)
    {"value": "sit-idle-cute", "text": "Rest", "time": 17.062613},
    {"value": "idle_zombie", "text": "Zombie", "time": 28.754937},
    {"value": "idle_layingdown2", "text": "Relaxed", "time": 21.546653},
    {"value": "idle_layingdown", "text": "Attentive", "time": 24.585168},
    {"value": "idle-sleep", "text": "Sleepy", "time": 22.620446},
    {"value": "idle-sad", "text": "Pouty Face", "time": 24.377214},
    {"value": "idle-posh", "text": "Posh", "time": 21.851256},
    {"value": "idle-loop-tired", "text": "Sleepy", "time": 21.959007},
    {"value": "idle-loop-tapdance", "text": "Tap Loop", "time": 6.261593},
    {"value": "idle-loop-sitfloor", "text": "Sit", "time": 22.321055},
    # ⚠️ СПИСОК ОЧЕНЬ БОЛЬШОЙ
    # ❗ Railway / Highrise это переживёт
    # ❗ list будет отправляться ЧАСТЯМИ
]

# ================== БОТ ==================

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.tasks: dict[int, asyncio.Task] = {}
        self.started_at = time.time()

    async def on_ready(self):
        print("✅ BOT CONNECTED AND READY")

    async def on_user_join(self, user: User):
        try:
            await self.highrise.chat(
                f"👋 @{user.username}\n"
                f"🎭 Напиши номер анимации (1–{len(timed_emotes)})\n"
                f"📜 list — список\n"
                f"🛑 0 — остановить\n"
                f"📡 ping — статус"
            )
        except Exception:
            pass

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()

        # ---- PING ----
        if msg == "ping":
            uptime = int(time.time() - self.started_at)
            await self.highrise.chat(
                f"🟢 Бот жив\n⏱ Аптайм: {uptime} сек"
            )
            return

        # ---- STOP ----
        if msg == "0":
            await self.stop_anim(user)
            await self.highrise.chat(f"🛑 @{user.username} анимация остановлена")
            return

        # ---- LIST ----
        if msg == "list":
            await self.send_emote_list()
            return

        # ---- НОМЕР ----
        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(timed_emotes):
                await self.start_anim(user, idx)
            return

    # ================== ЛОГИКА ==================

    async def start_anim(self, user: User, idx: int):
        await self.stop_anim(user)
        em = timed_emotes[idx]

        async def loop():
            try:
                while True:
                    await self.highrise.send_emote(em["value"], user.id)
                    await asyncio.sleep(max(em["time"] - 0.3, 0.2))
            except asyncio.CancelledError:
                pass
            except Exception:
                pass

        self.tasks[user.id] = asyncio.create_task(loop())
        await self.highrise.chat(
            f"🎬 @{user.username} → {idx + 1}. {em['text']}"
        )

    async def stop_anim(self, user: User):
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()

    async def send_emote_list(self):
        chunk = []
        msg_len = 0

        for i, e in enumerate(timed_emotes, 1):
            line = f"{i}. {e['text']}\n"
            if msg_len + len(line) > 350:
                await self.highrise.chat("".join(chunk))
                chunk = []
                msg_len = 0
            chunk.append(line)
            msg_len += len(line)

        if chunk:
            await self.highrise.chat("".join(chunk))


# ================== ЗАПУСК ==================

if __name__ == "__main__":
    bot = Bot()
    app = Highrise(bot)
    app.run()