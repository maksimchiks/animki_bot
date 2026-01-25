import asyncio
from highrise import BaseBot, User

# ================= АНИМАЦИИ =================
timed_emotes = [
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
    {"value": "idle-loop-shy", "text": "Shy", "time": 16.47449},
    {"value": "idle-loop-sad", "text": "Bummed", "time": 6.052999},
    {"value": "idle-loop-happy", "text": "Chillin'", "time": 18.798322},
    {"value": "idle-loop-annoyed", "text": "Annoyed", "time": 17.058522},
    {"value": "idle-loop-aerobics", "text": "Aerobics", "time": 8.507535},
    {"value": "idle-lookup", "text": "Ponder", "time": 22.339865},
    {"value": "idle-hero", "text": "Hero Pose", "time": 21.877099},
    {"value": "idle-floorsleeping2", "text": "Relaxing", "time": 17.253372},
    {"value": "idle-floorsleeping", "text": "Cozy Nap", "time": 13.935264},
    {"value": "idle-enthusiastic", "text": "Enthused", "time": 15.941537},
    {"value": "idle-dance-swinging", "text": "Boogie Swing", "time": 13.198551},
    {"value": "idle-dance-headbobbing", "text": "Feel The Beat", "time": 25.367458},
    {"value": "idle-angry", "text": "Irritated", "time": 25.427848},
    {"value": "emote-yes", "text": "Yes", "time": 2.565001},
    {"value": "emote-wings", "text": "I Believe I Can Fly", "time": 13.134487},
    {"value": "emote-wave", "text": "The Wave", "time": 2.690873},
    {"value": "emote-tired", "text": "Tired", "time": 4.61063},
    {"value": "emote-think", "text": "Think", "time": 3.691104},
    {"value": "emote-theatrical", "text": "Theatrical", "time": 8.591869},
    {"value": "emote-tapdance", "text": "Tap Dance", "time": 11.057294},
    {"value": "emote-superrun", "text": "Super Run", "time": 6.273226},
    {"value": "emote-superpunch", "text": "Super Punch", "time": 3.751054},
    {"value": "emote-sumo", "text": "Sumo Fight", "time": 10.868834},
    {"value": "emote-suckthumb", "text": "Thumb Suck", "time": 4.185944},
    {"value": "emote-splitsdrop", "text": "Splits Drop", "time": 4.46931},
    {"value": "emote-snowball", "text": "Snowball Fight!", "time": 5.230467},
    {"value": "emote-snowangel", "text": "Snow Angel", "time": 6.218627},
    {"value": "emote-shy", "text": "Shy", "time": 4.477567},
    {"value": "emote-secrethandshake", "text": "Secret Handshake", "time": 3.879024},
    {"value": "emote-sad", "text": "Sad", "time": 5.411073},
    {"value": "emote-ropepull", "text": "Rope Pull", "time": 8.769656},
    {"value": "emote-roll", "text": "Roll", "time": 3.560517},
    {"value": "emote-rofl", "text": "ROFL!", "time": 6.314731},
    {"value": "emote-robot", "text": "Robot", "time": 7.607362},
    {"value": "emote-rainbow", "text": "Rainbow", "time": 2.813373},
    {"value": "emote-proposing", "text": "Proposing", "time": 4.27888},
    {"value": "emote-peekaboo", "text": "Peekaboo!", "time": 3.629867},
    {"value": "emote-peace", "text": "Peace", "time": 5.755004},
    {"value": "emote-panic", "text": "Panic", "time": 2.850966},
    {"value": "emote-no", "text": "No", "time": 2.703034},
    {"value": "emote-ninjarun", "text": "Ninja Run", "time": 4.754721},
    {"value": "emote-nightfever", "text": "Night Fever", "time": 5.488424},
    {"value": "emote-monster_fail", "text": "Monster Fail", "time": 4.632708},
    {"value": "emote-model", "text": "Model", "time": 6.490173},
    {"value": "emote-lust", "text": "Flirty Wave", "time": 4.655965},
    {"value": "emote-levelup", "text": "Level Up!", "time": 6.0545},
    {"value": "emote-laughing2", "text": "Amused", "time": 5.056641},
    {"value": "emote-laughing", "text": "Laugh", "time": 2.69161},
    {"value": "emote-kiss", "text": "Kiss", "time": 2.387175},
    {"value": "emote-kicking", "text": "Super Kick", "time": 4.867992},
    {"value": "emote-jumpb", "text": "Jump", "time": 3.584234},
    {"value": "emote-judochop", "text": "Judo Chop", "time": 2.427442},
    {"value": "emote-jetpack", "text": "Imaginary Jetpack", "time": 16.759457},
    {"value": "emote-hugyourself", "text": "Hug Yourself", "time": 4.992751},
    {"value": "emote-hot", "text": "Sweating", "time": 4.353037},
    {"value": "emote-hero", "text": "Hero Entrance", "time": 4.996096},
    {"value": "emote-hello", "text": "Hello", "time": 2.734844},
    {"value": "emote-headball", "text": "Headball", "time": 10.073119},
    {"value": "emote-harlemshake", "text": "Harlem Shake", "time": 13.558597},
    {"value": "emote-happy", "text": "Happy", "time": 3.483462},
    {"value": "emote-handstand", "text": "Handstand", "time": 4.015678},
    {"value": "emote-greedy", "text": "Greedy Emote", "time": 4.639828},
    {"value": "emote-graceful", "text": "Graceful", "time": 3.7498},
    {"value": "emote-gordonshuffle", "text": "Moonwalk", "time": 8.052307},
    {"value": "emote-ghost-idle", "text": "Ghost Float", "time": 19.570492},
    {"value": "emote-gangnam", "text": "Gangnam Style", "time": 7.275486},
    {"value": "emote-frollicking", "text": "Frolic", "time": 3.700665},
    {"value": "emote-fainting", "text": "Faint", "time": 18.423499},
    {"value": "emote-fail2", "text": "Clumsy", "time": 6.475972},
    {"value": "emote-fail1", "text": "Fall", "time": 5.617942},
    {"value": "emote-exasperatedb", "text": "Face Palm", "time": 2.722748},
    {"value": "emote-exasperated", "text": "Exasperated", "time": 2.367483},
    {"value": "emote-elbowbump", "text": "Elbow Bump", "time": 3.799768},
    {"value": "emote-disco", "text": "Disco", "time": 5.366973},
    {"value": "emote-disappear", "text": "Blast Off", "time": 6.195985},
    {"value": "emote-deathdrop", "text": "Faint Drop", "time": 3.762728},
    {"value": "emote-death2", "text": "Collapse", "time": 4.855549},
    {"value": "emote-death", "text": "Revival", "time": 6.615967},
    {"value": "emote-dab", "text": "Dab", "time": 2.717871},
    {"value": "emote-curtsy", "text": "Curtsy", "time": 2.425714},
    {"value": "emote-confused", "text": "Confusion", "time": 8.578827},
    {"value": "emote-cold", "text": "Cold", "time": 3.664348},
    {"value": "emote-charging", "text": "Charging", "time": 8.025079},
    {"value": "emote-bunnyhop", "text": "Bunny Hop", "time": 12.380685},
    {"value": "emote-bow", "text": "Bow", "time": 3.344036},
    {"value": "emote-boo", "text": "Boo", "time": 4.501502},
    {"value": "emote-baseball", "text": "Home Run!", "time": 7.254841},
    {"value": "emote-apart", "text": "Falling Apart", "time": 4.809542},
    {"value": "emoji-thumbsup", "text": "Thumbs Up", "time": 2.702369},
    {"value": "emoji-there", "text": "Point", "time": 2.059095},
    {"value": "emoji-sneeze", "text": "Sneeze", "time": 2.996694},
    {"value": "emoji-smirking", "text": "Smirk", "time": 4.823158},
    {"value": "emoji-sick", "text": "Sick", "time": 5.070367},
    {"value": "emoji-scared", "text": "Gasp", "time": 3.008487},
    {"value": "emoji-punch", "text": "Punch", "time": 1.755783},
    {"value": "emoji-pray", "text": "Pray", "time": 4.503179},
    {"value": "emoji-poop", "text": "Stinky", "time": 4.795735},
    {"value": "emoji-naughty", "text": "Naughty", "time": 4.277602},
    {"value": "emoji-mind-blown", "text": "Mind Blown", "time": 2.397167},
    {"value": "emoji-lying", "text": "Lying", "time": 6.313748},
    {"value": "emoji-halo", "text": "Levitate", "time": 5.837754},
    {"value": "emoji-hadoken", "text": "Fireball Lunge", "time": 2.723709},
    {"value": "emoji-give-up", "text": "Give Up", "time": 5.407888},
    {"value": "emoji-gagging", "text": "Tummy Ache", "time": 5.500202},
    {"value": "emoji-flex", "text": "Flex", "time": 2.099351},
    {"value": "emoji-dizzy", "text": "Stunned", "time": 4.053049},
    {"value": "emoji-cursing", "text": "Cursing", "time": 2.382069},
    {"value": "emoji-crying", "text": "Sob", "time": 3.696499},
    {"value": "emoji-clapping", "text": "Clap", "time": 2.161757},
    {"value": "emoji-celebrate", "text": "Celebrate", "time": 3.412258},
    {"value": "emoji-arrogance", "text": "Arrogance", "time": 6.869441},
    {"value": "emoji-angry", "text": "Angry", "time": 5.760023},
]

# ================= БОТ =================
class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.tasks = {}

    async def on_user_join(self, user: User):
        await self.highrise.chat(
            f"👋 @{user.username}\n"
            f"🎭 Напиши номер анимации (1–{len(timed_emotes)})\n"
            f"📜 list — список\n"
            f"🛑 stop — остановить"
        )

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()

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

        async def loop():
            try:
                while True:
                    await self.highrise.send_emote(em["value"], user.id)
                    await asyncio.sleep(max(em["time"] - 0.3, 0.1))
            except asyncio.CancelledError:
                pass

        self.tasks[user.id] = asyncio.create_task(loop())

    async def stop_anim(self, user: User):
        task = self.tasks.get(user.id)
        if task:
            task.cancel()
            self.tasks.pop(user.id, None)