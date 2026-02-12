import asyncio
import time
import random

from highrise import BaseBot
from highrise.models import User
from highrise.models import User, Reaction
from highrise.models import Position

PAGE_SIZE = 20

# ====== ВСТАВЬ СЮДА СВОЙ timed_emotes СПИСОК ======
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
    {"value": "emote-frollicking", "text": "Frolic ", "time": 3.700665},
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
    {"value": "emoji-cursing", "text": "Cursing Emote", "time": 2.382069},
    {"value": "emoji-crying", "text": "Sob", "time": 4.696499},
    {"value": "emoji-clapping", "text": "Clap", "time": 2.161757},
    {"value": "emoji-celebrate", "text": "Raise The Roof", "time": 3.412258},
    {"value": "emoji-arrogance", "text": "Arrogance", "time": 6.869441},
    {"value": "emoji-angry", "text": "Angry", "time": 5.760023},
    {"value": "dance-voguehands", "text": "Vogue Hands", "time": 9.150634},
    {"value": "dance-tiktok8", "text": "Savage Dance", "time": 10.938702},
    {"value": "dance-tiktok2", "text": "Don't Start Now", "time": 10.392353},
    {"value": "dance-spiritual", "text": "Yoga Flow", "time": 15.795092},
    {"value": "dance-smoothwalk", "text": "Smoothwalk", "time": 6.690023},
    {"value": "dance-singleladies", "text": "Ring on It", "time": 21.191372},
    {"value": "dance-shoppingcart", "text": "Let's Go Shopping", "time": 4.316035},
    {"value": "dance-russian", "text": "Russian Dance", "time": 10.252905},
    {"value": "dance-robotic", "text": "Robotic", "time": 17.814959},
    {"value": "dance-pennywise", "text": "Penny's Dance", "time": 1.214349},
    {"value": "dance-orangejustice", "text": "Orange Juice Dance", "time": 6.475263},
    {"value": "dance-metal", "text": "Rock Out", "time": 15.076377},
    {"value": "dance-martial-artist", "text": "Karate", "time": 13.284405},
    {"value": "dance-macarena", "text": "Macarena", "time": 12.214141},
    {"value": "dance-handsup", "text": "Hands in the Air", "time": 22.283413},
    {"value": "dance-floss", "text": "Floss", "time": 21.329661},
    {"value": "dance-duckwalk", "text": "Duck Walk", "time": 11.748784},
    {"value": "dance-breakdance", "text": "Breakdance", "time": 17.623849},
    {"value": "dance-blackpink", "text": "K-Pop Dance", "time": 7.150958},
    {"value": "dance-aerobics", "text": "Push Ups", "time": 8.796402},
    {"value": "emote-hyped", "text": "Hyped", "time": 7.492423},
    {"value": "dance-jinglebell", "text": "Jinglebell", "time": 11},
    {"value": "idle-nervous", "text": "Nervous", "time": 21.714221},
    {"value": "idle-toilet", "text": "Toilet", "time": 32.174447},
    {"value": "emote-attention", "text": "Attention", "time": 4.401206},
    {"value": "emote-astronaut", "text": "Astronaut", "time": 13.791175},
    {"value": "dance-zombie", "text": "Dance Zombie", "time": 12.922772},
    {"value": "emoji-ghost", "text": "Ghost", "time": 3.472759},
    {"value": "emote-hearteyes", "text": "Heart Eyes", "time": 4.034386},
    {"value": "emote-swordfight", "text": "Swordfight", "time": 5.914365},
    {"value": "emote-timejump", "text": "TimeJump", "time": 4.007305},
    {"value": "emote-snake", "text": "Snake", "time": 5.262578},
    {"value": "emote-heartfingers", "text": "Heart Fingers", "time": 4.001974},
    {"value": "emote-heartshape", "text": "Heart Shape", "time": 6.232394},
    {"value": "emote-hug", "text": "Hug", "time": 3.503262},
    {"value": "emote-lagughing", "text": "Laugh", "time": 1.125537},
    {"value": "emoji-eyeroll", "text": "Eyeroll", "time": 3.020264},
    {"value": "emote-embarrassed", "text": "Embarrassed", "time": 7.414283},
    {"value": "emote-float", "text": "Float", "time": 8.995302},
    {"value": "emote-telekinesis", "text": "Telekinesis", "time": 10.492032},
    {"value": "dance-sexy", "text": "Sexy dance", "time": 12.30883},
    {"value": "emote-puppet", "text": "Puppet", "time": 16.325823},
    {"value": "idle-fighter", "text": "Fighter idle", "time": 17.19123},
    {"value": "dance-pinguin", "text": "Penguin dance", "time": 11.58291},
    {"value": "dance-creepypuppet", "text": "Creepy puppet", "time": 6.416121},
    {"value": "emote-sleigh", "text": "Sleigh", "time": 11.333165},
    {"value": "emote-maniac", "text": "Maniac", "time": 4.906886},
    {"value": "emote-energyball", "text": "Energy Ball", "time": 7.575354},
    {"value": "idle_singing", "text": "Singing", "time": 10.260182},
    {"value": "emote-frog", "text": "Frog", "time": 14.55257},
    {"value": "emote-superpose", "text": "Superpose", "time": 4.530791},
    {"value": "emote-cute", "text": "Cute", "time": 6.170464},
    {"value": "dance-tiktok9", "text": "TikTok Dance 9", "time": 11.892918},
    {"value": "dance-weird", "text": "Weird Dance", "time": 21.556237},
    {"value": "dance-tiktok10", "text": "TikTok Dance 10", "time": 8.225648},
    {"value": "emote-pose7", "text": "Pose 7", "time": 4.655283},
    {"value": "emote-pose8", "text": "Pose 8", "time": 4.808806},
    {"value": "idle-dance-casual", "text": "Casual Dance", "time": 9.079756},
    {"value": "emote-pose1", "text": "Pose 1", "time": 2.825795},
    {"value": "emote-pose3", "text": "Pose 3", "time": 5.10562},
    {"value": "emote-pose5", "text": "Pose 5", "time": 4.621532},
    {"value": "emote-cutey", "text": "Cutey", "time": 3.26032},
    {"value": "emote-punkguitar", "text": "Punk Guitar", "time": 9.365807},
    {"value": "emote-zombierun", "text": "Zombie Run", "time": 9.182984},
    {"value": "emote-fashionista", "text": "Fashionista", "time": 5.606485},
    {"value": "emote-gravity", "text": "Gravity", "time": 8.955966},
    {"value": "dance-icecream", "text": "Ice Cream Dance", "time": 14.769573},
    {"value": "dance-wrong", "text": "Wrong Dance", "time": 12.422389},
    {"value": "idle-uwu", "text": "UwU", "time": 24.761968},
    {"value": "idle-dance-tiktok4", "text": "TikTok Dance 4", "time": 15.500708},
    {"value": "emote-shy2", "text": "Advanced Shy", "time": 4.989278},
    {"value": "dance-anime", "text": "Anime Dance", "time": 8.46671},
    {"value": "dance-kawai", "text": "Kawaii", "time": 10.290789},
    {"value": "idle-wild", "text": "Scritchy", "time": 26.422824},
    {"value": "emote-iceskating", "text": "Ice Skating", "time": 7.299156},
    {"value": "emote-pose6", "text": "SurpriseBig", "time": 5.375124},
    {"value": "emote-celebrationstep", "text": "Celebration Step", "time": 3.353703},
    {"value": "emote-creepycute", "text": "Creepycute", "time": 7.902453},
    {"value": "emote-frustrated", "text": "Frustrated", "time": 5.584622},
    {"value": "emote-pose10", "text": "Pose 10", "time": 3.989871},
    {"value": "sit-relaxed", "text": "Relaxed", "time": 29.889858},
    {"value": "sit-open", "text": "Laid Back", "time": 26.025963},
    {"value": "emote-stargaze", "text": "Star gazing", "time": 1.127464},
    {"value": "emote-slap", "text": "Slap", "time": 2.724945},
    {"value": "emote-boxer", "text": "Boxer", "time": 5.555702},
    {"value": "emote-headblowup", "text": "Head Blowup", "time": 11.667537},
    {"value": "emote-kawaiigogo", "text": "KawaiiGoGo", "time": 10},
    {"value": "emote-repose", "text": "Repose", "time": 1.118455},
    {"value": "idle-dance-tiktok7", "text": "Tiktok7", "time": 12.956484},
    {"value": "emote-shrink", "text": "Shrink", "time": 8.738784},
    {"value": "emote-pose9", "text": "Ditzy Pose", "time": 4.583117},
    {"value": "emote-teleporting", "text": "Teleporting", "time": 11.7676},
    {"value": "dance-touch", "text": "Touch", "time": 11.7},
    {"value": "idle-guitar", "text": "Air Guitar", "time": 13.229398},
    {"value": "emote-gift", "text": "This Is For You", "time": 5.8},
    {"value": "dance-employee", "text": "Push it", "time": 8},

]

POPULAR_EMOTES = [
    75,   # Rest
    9,   # Sleepy
    15,  # Bummed
    1,  # Chillin'
    21,  # Feel The Beat
]


class Bot(BaseBot):
    async def before_start(self, *args, **kwargs):
        self.tasks: dict[str, asyncio.Task] = {}
        self.started_at = time.time()
        self._alive_task: asyncio.Task | None = None
        self._chat_keepalive_task: asyncio.Task | None = None
        
        self._keepalive_task = asyncio.create_task(self._keep_alive())
        asyncio.create_task(self.popular_emote_loop())
        asyncio.create_task(self._alive_loop())
        
    async def run(self):
        """Entry point for Railway - auto-reconnect on crash"""
        from highrise import Highrise
        import os
        
        while True:
            try:
                token = os.environ.get("HIGHRISE_API_TOKEN") or os.environ.get("BEARER_TOKEN")
                room_id = os.environ.get("HIGHRISE_ROOM_ID") or os.environ.get("ROOM_ID")
                
                if not token or not room_id:
                    raise ValueError("HIGHRISE_API_TOKEN and HIGHRISE_ROOM_ID required")
                
                print("[Bot] Connecting to Highrise...")
                Highrise(token=token, room_id=room_id).run(self)
            except Exception as e:
                print(f"[Bot] Error: {e}")
                print("[Bot] Reconnecting in 10 seconds...")
                await asyncio.sleep(10)
    
    async def send_emote_list(self, user: User):
        CHUNK = 20
        for start in range(0, len(timed_emotes), CHUNK):
            part = timed_emotes[start:start + CHUNK]
            text = f"🎭 Анимации ({start + 1}-{start + len(part)}):\n"
            for i, em in enumerate(part, start=start + 1):
                text += f"{i} — {em['text']}\n"
            try:
                await self.highrise.send_whisper(user.id, text)
                await asyncio.sleep(0.4)
            except Exception:
                return
    
    async def popular_emote_loop(self):
        await asyncio.sleep(120)
        while True:
            try:
                lines = ["🔥 Популярные анимации:"]
                for idx in POPULAR_EMOTES:
                    if idx < len(timed_emotes):
                        em = timed_emotes[idx]
                        lines.append(f"{idx + 1} — {em['text']}")
                lines.append("👉 Напиши номер анимации")
                await self.highrise.chat("\n".join(lines))
            except Exception:
                pass
            await asyncio.sleep(600)
    
    async def safe_react(self, user_id: str):
        """Send emote instead of reaction when user joins"""
        try:
            await self.highrise.send_emote("emote-heart", user_id)
        except Exception:
            pass
    
    async def _keep_alive(self):
        """Keep connection alive with periodic signals"""
        while True:
            try:
                await asyncio.sleep(30)
                await self.highrise.send_emote("emote-wave", "bot")
            except asyncio.CancelledError:
                return
            except Exception:
                await asyncio.sleep(5)
    
    async def on_ready(self, *args, **kwargs):
        print("[Bot] Connected and ready!")
        try:
            await self.highrise.chat(
                f"✅ Бот онлайн. Номера анимок: 1-{len(timed_emotes)} | 0 — стоп | ping — проверка"
            )
        except Exception:
            pass
    
    async def _alive_loop(self):
        while True:
            try:
                uptime = int(time.time() - self.started_at)
                print(f"[alive] uptime={uptime}s users_with_tasks={len(self.tasks)}", flush=True)
                await asyncio.sleep(25)
            except asyncio.CancelledError:
                return
            except Exception:
                await asyncio.sleep(5)
    
    async def on_user_join(self, user: User, position: Position = None, **kwargs):
        try:
            await self.highrise.send_whisper(
                user.id,
                f"👋 @{user.username}\n"
                f"Напиши номер анимации (1-{len(timed_emotes)})\n"
                f"0 — остановить\n"
                f"ping — проверка"
            )
            await self.safe_react(user.id)
        except Exception:
            pass
    
    async def on_chat(self, user: User, message: str, **kwargs):
        msg = (message or "").strip().lower()
        
        # ===== LIST =====
        if msg.startswith("list"):
            page = 1
            if msg != "list" and msg.replace("list", "").strip().isdigit():
                page = int(msg.replace("list", "").strip())
            
            PAGE_SIZE = 10
            total_pages = (len(timed_emotes) + PAGE_SIZE - 1) // PAGE_SIZE
            page = max(1, min(page, total_pages))
            
            start = (page - 1) * PAGE_SIZE
            end = start + PAGE_SIZE
            
            lines = [f"🎭 Анимации — страница {page}/{total_pages}"]
            for i, em in enumerate(timed_emotes[start:end], start=start + 1):
                lines.append(f"{i}. {em['text']}")
            
            lines.append("\n👉 Напиши номер анимации")
            if page < total_pages:
                lines.append(f"📄 list {page+1} — следующая страница")
            else:
                lines.append("✅ Конец списка")
            
            await self.highrise.send_whisper(user.id, "\n".join(lines))
            return
        
        # ===== PING =====
        if msg == "ping":
            if not hasattr(self, "started_at"):
                self.started_at = time.time()
            uptime = int(time.time() - self.started_at)
            await self.highrise.chat(f"🏓 pong | аптайм {uptime} сек")
            return
        
        # ===== STOP =====
        if msg == "0":
            await self.stop_anim(user)
            await self.highrise.chat("⛔ Анимация остановлена")
            return
        
        # ===== NUMBER =====
        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(timed_emotes):
                await self.start_anim(user, idx)
            return
        
        for i, em in enumerate(timed_emotes):
            name = em.get("text", "").lower().replace(" ", "")
            key = em.get("value", "").lower()
            
            if msg == name or msg == key:
                await self.start_anim(user, i)
                return
    
    async def start_anim(self, user: User, idx: int):
        if not hasattr(self, "tasks"):
            self.tasks = {}
        
        await self.stop_anim(user)
        
        async def loop():
            em = timed_emotes[idx]
            emote_id = em.get("value")
            delay = float(em.get("time", 2.0))
            
            if not emote_id:
                return
            if delay <= 0:
                delay = 2.0
            
            while True:
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                    await asyncio.sleep(max(delay - 0.15, 0.2))
                except asyncio.CancelledError:
                    return
                except Exception:
                    await asyncio.sleep(1.0)
        
        self.tasks[user.id] = asyncio.create_task(loop())
    
    async def stop_anim(self, user: User):
        if not hasattr(self, "tasks"):
            self.tasks = {}
        
        task = self.tasks.pop(user.id, None)
        if task:
            task.cancel()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
