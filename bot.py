import asyncio
import time
import random

from highrise import BaseBot
from highrise.models import User
from highrise.models import User, Reaction
from highrise.models import Position
from highrise.models import Item

PAGE_SIZE = 20

# ====== ВСТАВЬ СЮДА СВОЙ timed_emotes СПИСОК ======
timed_emotes = [
     {"value": "sit-idle-cute", "text": "Rest", "time": 16.062613},
    {"value": "idle_zombie", "text": "Zombie", "time": 27.754937},
    {"value": "idle_layingdown2", "text": "Relaxed", "time": 20.546653},
    {"value": "idle_layingdown", "text": "Attentive", "time": 23.585168},
    {"value": "idle-sleep", "text": "Sleepy", "time": 21.620446},
    {"value": "idle-sad", "text": "Pouty Face", "time": 23.377214},
    {"value": "idle-posh", "text": "Posh", "time": 20.851256},
    {"value": "idle-loop-tired", "text": "Sleepy", "time": 20.959007},
    {"value": "idle-loop-tapdance", "text": "Tap Loop", "time": 6.261593},
    {"value": "idle-loop-sitfloor", "text": "Sit", "time": 21.321055},
    {"value": "idle-loop-shy", "text": "Shy", "time": 15.47449},
    {"value": "idle-loop-sad", "text": "Bummed", "time": 6.052999},
    {"value": "idle-loop-happy", "text": "Chillin'", "time": 17.798322},
    {"value": "idle-loop-annoyed", "text": "Annoyed", "time": 16.058522},
    {"value": "idle-loop-aerobics", "text": "Aerobics", "time": 8.507535},
    {"value": "idle-lookup", "text": "Ponder", "time": 21.339865},
    {"value": "idle-hero", "text": "Hero Pose", "time": 20.877099},
    {"value": "idle-floorsleeping2", "text": "Relaxing", "time": 16.253372},
    {"value": "idle-floorsleeping", "text": "Cozy Nap", "time": 12.935264},
    {"value": "idle-enthusiastic", "text": "Enthused", "time": 14.941537},
    {"value": "idle-dance-swinging", "text": "Boogie Swing", "time": 12.198551},
    {"value": "idle-dance-headbobbing", "text": "Feel The Beat", "time": 24.367458},
    {"value": "idle-angry", "text": "Irritated", "time": 24.427848},
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
    {"value": "emote-ghost-idle", "text": "Ghost Float", "time": 18.570492},
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
    {"value": "idle-nervous", "text": "Nervous", "time": 20.714221},
    {"value": "idle-toilet", "text": "Toilet", "time": 31.174447},
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
    {"value": "idle-fighter", "text": "Fighter idle", "time": 16.19123},
    {"value": "dance-pinguin", "text": "Penguin dance", "time": 11.58291},
    {"value": "dance-creepypuppet", "text": "Creepy puppet", "time": 6.416121},
    {"value": "emote-sleigh", "text": "Sleigh", "time": 11.333165},
    {"value": "emote-maniac", "text": "Maniac", "time": 4.906886},
    {"value": "emote-energyball", "text": "Energy Ball", "time": 7.575354},
    {"value": "idle_singing", "text": "Singing", "time": 9.260182},
    {"value": "emote-frog", "text": "Frog", "time": 14.55257},
    {"value": "emote-superpose", "text": "Superpose", "time": 4.530791},
    {"value": "emote-cute", "text": "Cute", "time": 6.170464},
    {"value": "dance-tiktok9", "text": "TikTok Dance 9", "time": 11.892918},
    {"value": "dance-weird", "text": "Weird Dance", "time": 21.556237},
    {"value": "dance-tiktok10", "text": "TikTok Dance 10", "time": 8.225648},
    {"value": "emote-pose7", "text": "Pose 7", "time": 4.655283},
    {"value": "emote-pose8", "text": "Pose 8", "time": 4.808806},
    {"value": "idle-dance-casual", "text": "Casual Dance", "time": 8.079756},
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
    {"value": "idle-uwu", "text": "UwU", "time": 23.761968},
    {"value": "idle-dance-tiktok4", "text": "TikTok Dance 4", "time": 14.500708},
    {"value": "emote-shy2", "text": "Advanced Shy", "time": 4.989278},
    {"value": "dance-anime", "text": "Anime Dance", "time": 8.46671},
    {"value": "dance-kawai", "text": "Kawaii", "time": 10.290789},
    {"value": "idle-wild", "text": "Scritchy", "time": 25.422824},
    {"value": "emote-iceskating", "text": "Ice Skating", "time": 7.299156},
    {"value": "emote-pose6", "text": "SurpriseBig", "time": 5.375124},
    {"value": "emote-celebrationstep", "text": "Celebration Step", "time": 3.353703},
    {"value": "emote-creepycute", "text": "Creepycute", "time": 7.902453},
    {"value": "emote-frustrated", "text": "Frustrated", "time": 5.584622},
    {"value": "emote-pose10", "text": "Pose 10", "time": 3.989871},
    {"value": "sit-relaxed", "text": "Relaxed", "time": 27.889858},
    {"value": "sit-open", "text": "Laid Back", "time": 25.025963},
    {"value": "emote-stargaze", "text": "Star gazing", "time": 1.127464},
    {"value": "emote-slap", "text": "Slap", "time": 2.724945},
    {"value": "emote-boxer", "text": "Boxer", "time": 5.555702},
    {"value": "emote-headblowup", "text": "Head Blowup", "time": 11.667537},
    {"value": "emote-kawaiigogo", "text": "KawaiiGoGo", "time": 10},
    {"value": "emote-repose", "text": "Repose", "time": 1.118455},
    {"value": "idle-dance-tiktok7", "text": "Tiktok7", "time": 11.956484},
    {"value": "emote-shrink", "text": "Shrink", "time": 8.738784},
    {"value": "emote-pose9", "text": "Ditzy Pose", "time": 4.583117},
    {"value": "emote-teleporting", "text": "Teleporting", "time": 11.7676},
    {"value": "dance-touch", "text": "Touch", "time": 11.7},
    {"value": "idle-guitar", "text": "Air Guitar", "time": 12.229398},
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

# Список танцев для команды /dance
DANCE_EMOTES = [
    "dance-voguehands",
    "dance-tiktok8",
    "dance-spiritual",
    "dance-orangejustice",
    "dance-blackpink",
    "dance-floss",
    "dance-breakdance",
    "dance-robotic",
    "dance-macarena",
    "dance-handsup",
    "dance-anime",
    "dance-kawai",
    "dance-metal",
    "dance-duckwalk",
    "dance-shoppingcart",
    "dance-russian",
    "dance-pinguin",
    "dance-creepypuppet",
    "dance-touch",
    "dance-employee",
]

# Preset локации для телепорта
TELEPORT_PRESETS = {
    "center": Position(0.5, 0.25, 14.5),
    "центр": Position(0.5, 0.25, 14.5),
    "spawn": Position(10.0, 0.75, 1.5),
    "спавн": Position(10.0, 0.75, 1.5),
}

# ====== VIP СИСТЕМА ======
import json
import os

VIP_USERS_FILE = "vip_users.json"

def load_vip_users():
    try:
        if os.path.exists(VIP_USERS_FILE):
            with open(VIP_USERS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_vip_users(vip_users):
    try:
        with open(VIP_USERS_FILE, 'w') as f:
            json.dump(vip_users, f)
    except:
        pass

# Цены на VIP (сумма -> дней VIP)
VIP_PRICES = {
    5: 3,      # 5 голды = 3 дня
    100: 7,     # 100 голды = 7 дней
    200: 15,    # 200 голды = 15 дней
    400: 30,    # 400 голды = 30 дней
}

# Список VIP пользователей
VIP_USERS = load_vip_users()

# ID админов
ADMIN_IDS = []

# ====== СПИСКИ ОДЕЖДЫ ======
# Формат: {"id": "item_id", "name": "Название"}

HAIR_FRONT = [
    {"id": "hair_front-n_malenew33", "name": "Short Short Fro"},
    {"id": "hair_front-n_malenew32", "name": "Box Braids"},
    {"id": "hair_front-n_malenew31", "name": "Long Undercut Dreads"},
    {"id": "hair_front-n_malenew30", "name": "Undercut Dreads"},
    {"id": "hair_front-n_malenew29", "name": "Side Swept Fro"},
    {"id": "hair_front-n_malenew27", "name": "Long Buzzed Fro"},
    {"id": "hair_front-n_malenew26", "name": "Short Buzzed Fro"},
    {"id": "hair_front-n_malenew25", "name": "Curly Undercut"},
    {"id": "hair_front-n_malenew24", "name": "Tight Curls"},
    {"id": "hair_front-n_malenew23", "name": "Loose Curls"},
    {"id": "hair_front-n_malenew22", "name": "Wavy Bob"},
    {"id": "hair_front-n_malenew21", "name": "Textured Crop"},
    {"id": "hair_front-n_malenew20", "name": "Slicked Back"},
    {"id": "hair_front-n_malenew19", "name": "Short Spikes"},
    {"id": "hair_front-n_malenew18", "name": "Messy"},
    {"id": "hair_front-n_malenew17", "name": "Medium Side Part"},
    {"id": "hair_front-n_malenew16", "name": "Short Side Part"},
    {"id": "hair_front-n_malenew15", "name": "Long Flowy"},
    {"id": "hair_front-n_malenew14", "name": "Long Straight"},
    {"id": "hair_front-n_malenew13", "name": "Afro"},
    {"id": "hair_front-n_malenew12", "name": "Big Curls"},
    {"id": "hair_front-n_malenew11", "name": "Dreadlocks"},
    {"id": "hair_front-n_malenew10", "name": "Braided"},
    {"id": "hair_front-n_malenew9", "name": "Cornrows"},
    {"id": "hair_front-n_malenew8", "name": "Ponytail"},
    {"id": "hair_front-n_malenew7", "name": "Bun"},
    {"id": "hair_front-n_malenew6", "name": "Short Curly"},
    {"id": "hair_front-n_malenew5", "name": "Short Wavy"},
    {"id": "hair_front-n_malenew4", "name": "Short Straight"},
    {"id": "hair_front-n_malenew3", "name": "Medium Curly"},
    {"id": "hair_front-n_malenew2", "name": "Medium Wavy"},
    {"id": "hair_front-n_malenew1", "name": "Medium Straight"},
]

HAIR_BACK = [
    {"id": "hair_back-n_malenew33", "name": "Short Short Fro"},
    {"id": "hair_back-n_malenew32", "name": "Box Braids"},
    {"id": "hair_back-n_malenew31", "name": "Long Undercut Dreads"},
    {"id": "hair_back-n_malenew30", "name": "Undercut Dreads"},
    {"id": "hair_back-n_malenew29", "name": "Side Swept Fro"},
    {"id": "hair_back-n_malenew28", "name": "Long Buzzed"},
    {"id": "hair_back-n_malenew27", "name": "Long Buzzed Fro"},
    {"id": "hair_back-n_malenew26", "name": "Short Buzzed Fro"},
    {"id": "hair_back-n_malenew25", "name": "Curly Undercut"},
    {"id": "hair_back-n_malenew24", "name": "Tight Curls"},
    {"id": "hair_back-n_malenew23", "name": "Loose Curls"},
    {"id": "hair_back-n_malenew22", "name": "Wavy Bob"},
    {"id": "hair_back-n_malenew21", "name": "Textured Crop"},
    {"id": "hair_back-n_malenew20", "name": "Slicked Back"},
    {"id": "hair_back-n_malenew19", "name": "Short Spikes"},
    {"id": "hair_back-n_malenew18", "name": "Messy"},
    {"id": "hair_back-n_malenew17", "name": "Medium Side Part"},
    {"id": "hair_back-n_malenew16", "name": "Short Side Part"},
    {"id": "hair_back-n_malenew15", "name": "Long Flowy"},
    {"id": "hair_back-n_malenew14", "name": "Long Straight"},
    {"id": "hair_back-n_malenew13", "name": "Afro"},
    {"id": "hair_back-n_malenew12", "name": "Big Curls"},
    {"id": "hair_back-n_malenew11", "name": "Dreadlocks"},
    {"id": "hair_back-n_malenew10", "name": "Braided"},
    {"id": "hair_back-n_malenew9", "name": "Cornrows"},
    {"id": "hair_back-n_malenew8", "name": "Ponytail"},
    {"id": "hair_back-n_malenew7", "name": "Bun"},
    {"id": "hair_back-n_malenew6", "name": "Short Curly"},
    {"id": "hair_back-n_malenew5", "name": "Short Wavy"},
    {"id": "hair_back-n_malenew4", "name": "Short Straight"},
    {"id": "hair_back-n_malenew3", "name": "Medium Curly"},
    {"id": "hair_back-n_malenew2", "name": "Medium Wavy"},
    {"id": "hair_back-n_malenew1", "name": "Medium Straight"},
]

FACE_HAIR = [
    {"id": "face_hair-n_beard2018fullbeard1", "name": "Full Beard"},
    {"id": "face_hair-n_beard2018fullbeard2", "name": "Full Beard Dark"},
    {"id": "face_hair-n_beard2018fullbeard3", "name": "Full Beard Light"},
    {"id": "face_hair-n_beard2018goatee1", "name": "Goatee"},
    {"id": "face_hair-n_beard2018goatee2", "name": "Goatee Dark"},
    {"id": "face_hair-n_beard2018goatee3", "name": "Goatee Light"},
    {"id": "face_hair-n_beard2018mustache1", "name": "Mustache"},
    {"id": "face_hair-n_beard2018mustache2", "name": "Handlebar"},
    {"id": "face_hair-n_beard2018mustache3", "name": "Pencil"},
    {"id": "face_hair-n_beard2018stubble1", "name": "Stubble"},
    {"id": "face_hair-n_beard2018stubble2", "name": "Light Stubble"},
    {"id": "face_hair-n_beard2018sideburns1", "name": "Sideburns"},
]

EYEBROW = [
    {"id": "eyebrow-n_basic2018newbrows01", "name": "Arched"},
    {"id": "eyebrow-n_basic2018newbrows02", "name": "S-Shaped"},
    {"id": "eyebrow-n_basic2018newbrows03", "name": "Straight"},
    {"id": "eyebrow-n_basic2018newbrows04", "name": "Curved"},
    {"id": "eyebrow-n_basic2018newbrows05", "name": "Thick"},
    {"id": "eyebrow-n_basic2018newbrows06", "name": "Thin"},
    {"id": "eyebrow-n_basic2018newbrows07", "name": "Medium"},
    {"id": "eyebrow-n_basic2018newbrows08", "name": "Angled"},
    {"id": "eyebrow-n_basic2018newbrows09", "name": "Round"},
    {"id": "eyebrow-n_basic2018newbrows10", "name": "Flat"},
]

EYE = [
    {"id": "eye-n_basic2018malesquaresleepy", "name": "Sleepy"},
    {"id": "eye-n_basic2018malealarmeround", "name": "Alert Round"},
    {"id": "eye-n_basic2018malecatty", "name": "Catty"},
    {"id": "eye-n_basic2018malecattyround", "name": "Round Catty"},
    {"id": "eye-n_basic2018malecupido", "name": "Cupid"},
    {"id": "eye-n_basic2018maledroppy", "name": "Droopy"},
    {"id": "eye-n_basic2018maleharlequin", "name": "Harlequin"},
    {"id": "eye-n_basic2018malehyper", "name": "Hyper"},
    {"id": "eye-n_basic2018malelimited", "name": "Limited"},
    {"id": "eye-n_basic2018malelollipop", "name": "Lollipop"},
    {"id": "eye-n_basic2018malemoon", "name": "Moon"},
    {"id": "eye-n_basic2018malenormal", "name": "Normal"},
    {"id": "eye-n_basic2018maleotic", "name": "Otic"},
    {"id": "eye-n_basic2018malepeering", "name": "Peering"},
    {"id": "eye-n_basic2018maleport", "name": "Port"},
    {"id": "eye-n_basic2018malesandclock", "name": "Sandclock"},
    {"id": "eye-n_basic2018malesleepy", "name": "Sleepy Alt"},
    {"id": "eye-n_basic2018malespinner", "name": "Spinner"},
    {"id": "eye-n_basic2018maletired", "name": "Tired"},
    {"id": "eye-n_basic2018maleuptired", "name": "Up Tired"},
]

NOSE = [
    {"id": "nose-n_basic2018newnose01", "name": "Button"},
    {"id": "nose-n_basic2018newnose02", "name": "Curved"},
    {"id": "nose-n_basic2018newnose03", "name": "Dainty"},
    {"id": "nose-n_basic2018newnose04", "name": "Hook"},
    {"id": "nose-n_basic2018newnose05", "name": "Noble"},
    {"id": "nose-n_basic2018newnose06", "name": "Round"},
    {"id": "nose-n_basic2018newnose07", "name": "Sharp"},
    {"id": "nose-n_basic2018newnose08", "name": "Straight"},
    {"id": "nose-n_basic2018newnose09", "name": "Upturned"},
    {"id": "nose-n_basic2018newnose10", "name": "Wide"},
]

MOUTH = [
    {"id": "mouth-basic2018chippermouth", "name": "Chirpy"},
    {"id": "mouth-basic2018concernedmouth", "name": "Concerned"},
    {"id": "mouth-basic2018cowmouth", "name": "Cow"},
    {"id": "mouth-basic2018daintymouth", "name": "Dainty"},
    {"id": "mouth-basic2018enviousmouth", "name": "Envious"},
    {"id": "mouth-basic2018happymouth", "name": "Happy"},
    {"id": "mouth-basic2018malemouth01", "name": "Neutral"},
    {"id": "mouth-basic2018malemouth02", "name": "Smile"},
    {"id": "mouth-basic2018malemouth03", "name": "Open"},
    {"id": "mouth-basic2018malemouth04", "name": "Frown"},
    {"id": "mouth-basic2018malemouth05", "name": "Pout"},
    {"id": "mouth-basic2018malemouth06", "name": "Grimace"},
    {"id": "mouth-basic2018malemouth07", "name": "Yawn"},
    {"id": "mouth-basic2018malemouth08", "name": "Scream"},
    {"id": "mouth-basic2018malemouth09", "name": "Cheeky"},
    {"id": "mouth-basic2018malemouth10", "name": "Smirk"},
]

SHIRT = [
    {"id": "shirt-n_starteritems2019tankwhite", "name": "Tank - White"},
    {"id": "shirt-n_starteritems2019tankblack", "name": "Tank - Black"},
    {"id": "shirt-n_starteritems2019maletshirtwhite", "name": "T-Shirt - White"},
    {"id": "shirt-n_starteritems2019maletshirtblack", "name": "T-Shirt - Black"},
    {"id": "shirt-n_room32019jerseywhite", "name": "Vintage Jersey"},
    {"id": "shirt-n_room32019jerseyblue", "name": "Blue Jersey"},
    {"id": "shirt-n_room32019jerseyred", "name": "Red Jersey"},
    {"id": "shirt-n_room32019jerseyblack", "name": "Black Jersey"},
    {"id": "shirt-n_room12019formalwhite", "name": "Formal White"},
    {"id": "shirt-n_room12019formalblack", "name": "Formal Black"},
    {"id": "shirt-n_room12019formaltan", "name": "Formal Tan"},
    {"id": "shirt-n_room12019formalgrey", "name": "Formal Grey"},
    {"id": "shirt-n_room12019sweaterblue", "name": "Sweater Blue"},
    {"id": "shirt-n_room12019sweatergreen", "name": "Sweater Green"},
    {"id": "shirt-n_room12019sweaterred", "name": "Sweater Red"},
    {"id": "shirt-n_room12019sweateryellow", "name": "Sweater Yellow"},
    {"id": "shirt-n_room12019sweaterpurple", "name": "Sweater Purple"},
    {"id": "shirt-n_room12019hoodieblue", "name": "Hoodie Blue"},
    {"id": "shirt-n_room12019hoodieblack", "name": "Hoodie Black"},
    {"id": "shirt-n_room12019hoodiegrey", "name": "Hoodie Grey"},
    {"id": "shirt-n_room12019hoodieorange", "name": "Hoodie Orange"},
    {"id": "shirt-n_room12019hoodiepink", "name": "Hoodie Pink"},
    {"id": "shirt-n_room12019polo", "name": "Polo"},
    {"id": "shirt-n_room12019polored", "name": "Polo Red"},
    {"id": "shirt-n_room12019poloblue", "name": "Polo Blue"},
]

PANTS = [
    {"id": "pants-n_starteritems2019mensshortswhite", "name": "Shorts - White"},
    {"id": "pants-n_starteritems2019mensshortsblue", "name": "Shorts - Blue"},
    {"id": "pants-n_starteritems2019mensshortsblack", "name": "Shorts - Black"},
    {"id": "pants-n_starteritems2019cuffedjeansblue", "name": "Cuffed Jeans"},
    {"id": "pants-n_room12019formalslackskhaki", "name": "Khaki Slacks"},
    {"id": "pants-n_room12019formalslacksnavy", "name": "Navy Slacks"},
    {"id": "pants-n_room12019formalslacksblack", "name": "Black Slacks"},
    {"id": "pants-n_room12019trackpantsblue", "name": "Track Pants Blue"},
    {"id": "pants-n_room12019trackpantsblack", "name": "Track Pants Black"},
    {"id": "pants-n_room12019trackpantsred", "name": "Track Pants Red"},
    {"id": "pants-n_room12019sweatpantsblue", "name": "Sweatpants Blue"},
    {"id": "pants-n_room12019sweatpantsgrey", "name": "Sweatpants Grey"},
    {"id": "pants-n_room12019sweatpantsblack", "name": "Sweatpants Black"},
    {"id": "pants-n_room12019cargopantscamo", "name": "Cargo Camo"},
    {"id": "pants-n_room12019cargopantsbrown", "name": "Cargo Brown"},
    {"id": "pants-n_room12019cargopantsblack", "name": "Cargo Black"},
    {"id": "pants-n_room12019skinnyjeansblue", "name": "Skinny Jeans Blue"},
    {"id": "pants-n_room12019skinnyjeansblack", "name": "Skinny Jeans Black"},
    {"id": "pants-n_room12019shortspatterned", "name": "Shorts Patterned"},
]

SKIRTS = [
    {"id": "skirt-n_starteritems2018whiteskirt", "name": "Skirt - White"},
    {"id": "skirt-n_starteritems2018blueskirt", "name": "Skirt - Blue"},
    {"id": "skirt-n_starteritems2018blackskirt", "name": "Skirt - Black"},
    {"id": "skirt-n_room12019pleatedblue", "name": "Pleated Blue"},
    {"id": "skirt-n_room12019pleatedblack", "name": "Pleated Black"},
    {"id": "skirt-n_room12019pleatedred", "name": "Pleated Red"},
    {"id": "skirt-n_room12019miniskirtblack", "name": "Mini Black"},
    {"id": "skirt-n_room12019miniskirtpink", "name": "Mini Pink"},
    {"id": "skirt-n_room12019maxiskirtblue", "name": "Maxi Blue"},
    {"id": "skirt-n_room12019maxiskirtred", "name": "Maxi Red"},
    {"id": "skirt-n_room12019maxiskirtyellow", "name": "Maxi Yellow"},
    {"id": "skirt-n_room12019maxiskirtgreen", "name": "Maxi Green"},
    {"id": "skirt-n_room12019wrapskirtbrown", "name": "Wrap Brown"},
    {"id": "skirt-n_room12019wrapskirtblack", "name": "Wrap Black"},
    {"id": "skirt-n_room12019pencilskirtnavy", "name": "Pencil Navy"},
    {"id": "skirt-n_room12019pencilskirtblack", "name": "Pencil Black"},
]

SHOES = [
    {"id": "shoes-n_whitedans", "name": "White Dans"},
    {"id": "shoes-n_starteritems2019flatswhite", "name": "White Flats"},
    {"id": "shoes-n_starteritems2018conversewhite", "name": "White Converse"},
    {"id": "shoes-n_converse_black", "name": "Black Converse"},
    {"id": "shoes-n_room12019sneakerswhite", "name": "Sneakers White"},
    {"id": "shoes-n_room12019sneakersblack", "name": "Sneakers Black"},
    {"id": "shoes-n_room12019sneakersred", "name": "Sneakers Red"},
    {"id": "shoes-n_room12019sneakersblue", "name": "Sneakers Blue"},
    {"id": "shoes-n_room12019loafersbrown", "name": "Loafers Brown"},
    {"id": "shoes-n_room12019loafersblack", "name": "Loafers Black"},
    {"id": "shoes-n_room12019bootsbrown", "name": "Boots Brown"},
    {"id": "shoes-n_room12019bootsblack", "name": "Boots Black"},
    {"id": "shoes-n_room12019heelswhite", "name": "Heels White"},
    {"id": "shoes-n_room12019heelsblack", "name": "Heels Black"},
    {"id": "shoes-n_room12019heelsred", "name": "Heels Red"},
    {"id": "shoes-n_room12019sandalsbrown", "name": "Sandals Brown"},
    {"id": "shoes-n_room12019sandalsblack", "name": "Sandals Black"},
]

SOCKS = [
    {"id": "socks-n_starteritems2019sockswhite", "name": "Socks White"},
    {"id": "socks-n_starteritems2019socksblack", "name": "Socks Black"},
    {"id": "socks-n_room12019stripedsocksblue", "name": "Striped Blue"},
    {"id": "socks-n_room12019stripedsocksred", "name": "Striped Red"},
    {"id": "socks-n_room12019patternedsocks", "name": "Patterned"},
]

GLASSES = [
    {"id": "glasses-n_starteritems201roundframesbrown", "name": "Round Frames - Brown"},
    {"id": "glasses-n_starteritems2019squareframesblack", "name": "Square Frames - Black"},
    {"id": "glasses-n_room12019circleframes", "name": "Circular Frames"},
    {"id": "glasses-n_room12019aviatorsgold", "name": "Aviators Gold"},
    {"id": "glasses-n_room12019aviatorssilver", "name": "Aviators Silver"},
    {"id": "glasses-n_room12019catseyesblack", "name": "Cat Eyes Black"},
    {"id": "glasses-n_room12019catseyesred", "name": "Cat Eyes Red"},
    {"id": "glasses-n_room12019heartshapedpink", "name": "Heart Pink"},
    {"id": "glasses-n_room12019starframesgold", "name": "Star Gold"},
    {"id": "glasses-n_room12019sunglassesblack", "name": "Sunglasses Black"},
    {"id": "glasses-n_room12019sunglassesbrown", "name": "Sunglasses Brown"},
    {"id": "glasses-n_room12019nerdglassesblack", "name": "Nerd Glasses"},
    {"id": "glasses-n_room12019monocleblack", "name": "Monocle"},
]

BAG = [
    {"id": "bag-n_room12019backpackblue", "name": "Backpack Blue"},
    {"id": "bag-n_room12019backpackbrown", "name": "Backpack Brown"},
    {"id": "bag-n_room12019backpackblack", "name": "Backpack Black"},
    {"id": "bag-n_room12019shoulderbagbrown", "name": "Shoulder Bag"},
    {"id": "bag-n_room12019messengerbagbrown", "name": "Messenger Bag"},
    {"id": "bag-n_room12019drawstringbagwhite", "name": "Drawstring"},
]

EARRINGS = [
    {"id": "earrings-n_room12019studsilver", "name": "Stud Silver"},
    {"id": "earrings-n_room12019studgold", "name": "Stud Gold"},
    {"id": "earrings-n_room12019hoopsilver", "name": "Hoops Silver"},
    {"id": "earrings-n_room12019hoopgold", "name": "Hoops Gold"},
    {"id": "earrings-n_room12019dangleearringssilver", "name": "Dangle Silver"},
    {"id": "earrings-n_room12019dangleearringsgold", "name": "Dangle Gold"},
    {"id": "earrings-n_room12019earcuffsilver", "name": "Earcuff Silver"},
    {"id": "earrings-n_room12019earcuffgold", "name": "Earcuff Gold"},
]

NECKLACE = [
    {"id": "necklace-n_room12019chaingold", "name": "Gold Chain"},
    {"id": "necklace-n_room12019chainsilver", "name": "Silver Chain"},
    {"id": "necklace-n_room12019pendantgold", "name": "Pendant Gold"},
    {"id": "necklace-n_room12019pendantsilver", "name": "Pendant Silver"},
    {"id": "necklace-n_room12019pearlnecklace", "name": "Pearl"},
    {"id": "necklace-n_room12019beadednecklaceblue", "name": "Beaded Blue"},
    {"id": "necklace-n_room12019chokerblack", "name": "Choker"},
    {"id": "necklace-n_room12019chokerred", "name": "Choker Red"},
]

WATCH = [
    {"id": "watch-n_room12019watchsilver", "name": "Watch Silver"},
    {"id": "watch-n_room12019watchgold", "name": "Watch Gold"},
    {"id": "watch-n_room12019watchblack", "name": "Watch Black"},
    {"id": "watch-n_room12019smartwatchblack", "name": "Smartwatch"},
    {"id": "watch-n_room12019fitnessbandblack", "name": "Fitness Band"},
]

HANDBAG = [
    {"id": "handbag-n_room12019totehandbagbrown", "name": "Tote Brown"},
    {"id": "handbag-n_room12019totehandbagblack", "name": "Tote Black"},
    {"id": "handbag-n_room12019clutchhandbagblack", "name": "Clutch Black"},
    {"id": "handbag-n_room12019satchelhandbagbrown", "name": "Satchel Brown"},
    {"id": "handbag-n_room12019hoboshandbagbrown", "name": "Hobo Brown"},
]

FRECKLE = [
    {"id": "freckle-n_room12019freckles", "name": "Freckles"},
    {"id": "blush-n_room12019blush", "name": "Blush"},
    {"id": "blush-n_room12019rosycheeks", "name": "Rosy Cheeks"},
    {"id": "blush-n_room12019highlighter", "name": "Highlighter"},
    {"id": "blush-n_room12019contour", "name": "Contour"},
]

# Базовая одежда (обязательные части)
BASE_BODY = [
    {"id": "body-flesh", "name": "Body", "active_palette": 27},
]

BASE_FACE = [
    {"id": "eye-n_basic2018malesquaresleepy", "name": "Eyes", "active_palette": 7},
    {"id": "eyebrow-n_basic2018newbrows07", "name": "Eyebrows", "active_palette": 0},
    {"id": "nose-n_basic2018newnose05", "name": "Nose", "active_palette": 0},
    {"id": "mouth-basic2018chippermouth", "name": "Mouth", "active_palette": -1},
]

# Категории для команд
CLOTHING_CATEGORIES = {
    "причёска": HAIR_FRONT,
    "волосы": HAIR_FRONT,
    "hair": HAIR_FRONT,
    "hair_back": HAIR_BACK,
    "волосы_сзади": HAIR_BACK,
    "борода": FACE_HAIR,
    "face_hair": FACE_HAIR,
    "усы": FACE_HAIR,
    "брови": EYEBROW,
    "eyebrow": EYEBROW,
    "глаза": EYE,
    "eye": EYE,
    "нос": NOSE,
    "nose": NOSE,
    "рот": MOUTH,
    "mouth": MOUTH,
    "штаны": PANTS,
    "pants": PANTS,
    "юбка": SKIRTS,
    "skirt": SKIRTS,
    "рубашка": SHIRT,
    "shirt": SHIRT,
    "обувь": SHOES,
    "shoes": SHOES,
    "носки": SOCKS,
    "socks": SOCKS,
    "очки": GLASSES,
    "glasses": GLASSES,
    "сумка": BAG,
    "bag": BAG,
    "серьги": EARRINGS,
    "earrings": EARRINGS,
    "ожерелье": NECKLACE,
    "necklace": NECKLACE,
    "часы": WATCH,
    "watch": WATCH,
    "клатч": HANDBAG,
    "handbag": HANDBAG,
    "румяна": FRECKLE,
    "freckle": FRECKLE,
    "бьюти": FRECKLE,
}


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
        
        reconnect_delay = 5
        
        while True:
            try:
                token = os.environ.get("HIGHRISE_API_TOKEN") or os.environ.get("BEARER_TOKEN")
                room_id = os.environ.get("HIGHRISE_ROOM_ID") or os.environ.get("ROOM_ID")
                
                if not token or not room_id:
                    raise ValueError("HIGHRISE_API_TOKEN and HIGHRISE_ROOM_ID required")
                
                print("[Bot] Connecting to Highrise...")
                client = Highrise(token=token, room_id=room_id)
                client.run(self)
                
                # Если run() завершился, значит соединение закрылось
                print("[Bot] Connection closed, reconnecting...")
            except Exception as e:
                print(f"[Bot] Error: {e}")
                print(f"[Bot] Reconnecting in {reconnect_delay} seconds...")
            
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, 60)  # max 60 seconds
    
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
    
    async def send_random_dance(self):
        """Отправить случайный танец для всех в комнате"""
        try:
            import random
            emote_id = random.choice(DANCE_EMOTES)
            em_name = emote_id.replace('dance-', '').replace('-', ' ').title()
            await self.highrise.chat(f"💃 Давайте станцуем! {em_name}!")
            await self.send_emote_to_all(emote_id, em_name)
        except Exception as e:
            print(f"[Debug] Error in send_random_dance: {e}")
    
    async def send_emote_to_all(self, emote_id: str, em_name: str = ""):
        """Отправить анимацию всем пользователям в комнате"""
        try:
            print(f"[Debug] Getting room users for emote {emote_id}...")
            response = await self.highrise.get_room_users()
            print(f"[Debug] get_room_users response type: {type(response)}")
            
            # Получаем список пользователей из response.content
            users = []
            if hasattr(response, 'content') and response.content:
                # content содержит список кортежей (User, Position)
                for item in response.content:
                    if isinstance(item, tuple) and len(item) > 0:
                        user = item[0]
                        if hasattr(user, 'id'):
                            users.append(item)
            elif hasattr(response, 'users') and response.users:
                users = response.users
            elif isinstance(response, tuple):
                users = response[0] if len(response) > 0 else []
            elif isinstance(response, list):
                users = response
            
            print(f"[Debug] Found {len(users)} users in room")
            
            count = 0
            for room_user, position in users:
                try:
                    print(f"[Debug] Sending {emote_id} to {room_user.id}...")
                    await self.highrise.send_emote(emote_id, room_user.id)
                    count += 1
                    print(f"[Debug] Sent to {count} users")
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"[Debug] Error sending to user: {e}")
            
            if count > 0:
                print(f"[Debug] Sent {em_name} to {count} users")
            else:
                print(f"[Debug] No users received emote")
        except Exception as e:
            print(f"[Debug] Error in send_emote_to_all: {e}")
    
    async def handle_teleport(self, user: User, message: str):
        """Обработка команды /tp [ник] preset|x,y,z"""
        try:
            # Проверка VIP для телепорта других игроков
            parts = message.split()
            teleport_others = len(parts) >= 3
            
            if teleport_others:
                # Телепорт другого — только VIP/модератор
                is_vip_or_mod = await self.is_vip(user.id) or await self.is_moderator(user.id)
                if not is_vip_or_mod:
                    await self.highrise.chat(f"@{user.username} ❌ Телепорт других игроков только для VIP!")
                    return
            
            # Проверяем что передано
            if len(parts) == 2:
                # /tp center — телепортировать себя
                target_name = user.username.lower()
                coordinate = parts[1].lower()
            elif len(parts) >= 3:
                # /tp Cyyka center — телепортировать другого
                target_name = parts[1].lower()
                coordinate = parts[2].lower()
            else:
                presets = ", ".join(TELEPORT_PRESETS.keys())
                await self.highrise.chat(f"@{user.username} Формат: /tp <preset|x,y,z> или /tp <ник> <preset|x,y,z>")
                return
            
            # Получаем позицию
            dest = None
            if coordinate in TELEPORT_PRESETS:
                dest = TELEPORT_PRESETS[coordinate]
                coord_str = coordinate
            else:
                try:
                    x, y, z = coordinate.split(",")
                    dest = Position(float(x), float(y), float(z))
                    coord_str = coordinate
                except:
                    presets = ", ".join(TELEPORT_PRESETS.keys())
                    await self.highrise.chat(f"@{user.username} Используй: /tp <{presets}|x,y,z>")
                    return
            
            # Ищем пользователя в комнате
            room_users = await self.highrise.get_room_users()
            users_list = room_users.content if hasattr(room_users, 'content') else []
            
            target_user_id = None
            for room_user, pos in users_list:
                if room_user.username.lower() == target_name:
                    target_user_id = room_user.id
                    break
            
            if not target_user_id:
                await self.highrise.chat(f"@{user.username} Пользователь '{target_name}' не найден")
                return
            
            # Телепортируем
            await self.highrise.teleport(user_id=target_user_id, dest=dest)
            
            if target_name == user.username.lower():
                await self.highrise.chat(f"@{user.username} Телепортировал тебя в {coord_str}")
            else:
                await self.highrise.chat(f"@{user.username} Телепортировал {target_name} → {coord_str}")
            
        except Exception as e:
            print(f"[Debug] Teleport error: {e}")
            await self.highrise.chat(f"@{user.username} Ошибка: {e}")
    
    async def show_user_position(self, user: User):
        """Показать координаты пользователя"""
        try:
            room_users = await self.highrise.get_room_users()
            users_list = room_users.content if hasattr(room_users, 'content') else []
            
            for room_user, pos in users_list:
                if room_user.id == user.id:
                    await self.highrise.send_whisper(
                        user.id,
                        f"📍 Твои координаты:\n"
                        f"x = {pos.x}\n"
                        f"y = {pos.y}\n"
                        f"z = {pos.z}\n"
                        f"facing = {pos.facing}"
                    )
                    return
            
            await self.highrise.send_whisper(user.id, "Не удалось найти тебя в комнате")
        except Exception as e:
            print(f"[Debug] Show position error: {e}")
            await self.highrise.send_whisper(user.id, f"Ошибка: {e}")
    
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
            presets = ", ".join(TELEPORT_PRESETS.keys())
            await self.highrise.chat(
                f"✅ Бот онлайн. Команды: 1-{len(timed_emotes)} — анимки | 0 — стоп | ping — проверка | танцы — танец всем | все X — анимация всем | тп — телепорт | позиция — мои координаты | одежда — список одежды | причёска 3 — надеть причёску"
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
        print(f"[Debug] User joined: {user.username}")
        try:
            await self.highrise.send_whisper(
                user.id,
                f"👋 @{user.username}\n"
                f"Команды: 1-{len(timed_emotes)} — анимки | 0 — стоп | танцы | все X\n"
                f"тп центр|spawn | позиция | одежда | ping"
            )
            print(f"[Debug] Whisper sent to {user.username}")
            await asyncio.sleep(0.5)
            print(f"[Debug] Trying to send reaction/emote to {user.username}")
            # Попробуем разные варианты реакций
            try:
                await self.highrise.react("heart", user.id)
                print(f"[Debug] Reaction heart sent")
            except Exception as e:
                print(f"[Debug] react heart failed: {e}")
                try:
                    await self.highrise.react("fire", user.id)
                    print(f"[Debug] Reaction fire sent")
                except Exception as e2:
                    print(f"[Debug] react fire failed: {e2}")
                    try:
                        await self.highrise.send_emote("emote-wave", user.id)
                        print(f"[Debug] Emote sent")
                    except Exception as e3:
                        print(f"[Debug] All reactions failed: {e3}")
        except Exception as e:
            print(f"[Debug] Error in on_user_join: {e}")
    
    async def on_tip(self, sender: User, receiver: User, tip: 'CurrencyItem | Item', **kwargs):
        """Обработка получения tip'а - покупка VIP"""
        try:
            # Проверяем что tip пришёл боту
            if receiver.id != self.highrise.my_id:
                return
            
            # Получаем сумму
            if hasattr(tip, 'amount'):
                amount = tip.amount
            else:
                return
            
            print(f"[VIP] {sender.username} отправил {amount} голды")
            
            # Проверяем цену
            days = None
            for price, d in VIP_PRICES.items():
                if amount >= price:
                    days = d
                    break
            
            if days is None:
                # Недостаточная сумма
                await self.highrise.send_whisper(
                    sender.id,
                    f"💰 Спасибо за {amount} голды!\n"
                    f"\nДоступные пакеты VIP:\n"
                    f"50 голды = 3 дня VIP\n"
                    f"100 голды = 7 дней VIP\n"
                    f"200 голды = 15 дней VIP\n"
                    f"400 голды = 30 дней VIP\n"
                    f"\nНапиши /вип_цены для подробностей"
                )
                return
            
            # Выдаём VIP
            import time
            expiration = time.time() + (days * 24 * 60 * 60)  # days in seconds
            VIP_USERS[sender.id] = expiration
            save_vip_users(VIP_USERS)  # Сохраняем в файл
            
            await self.highrise.send_whisper(
                sender.id,
                f"✅ Спасибо за {amount} голды!\n"
                f"🎉 Тебе выдан VIP на {days} дней!\n"
                f"\nДоступные команды:\n"
                f"• /тп ник центр — телепорт других\n"
                f"• /все 5 — анимация всем\n"
                f"• /танцы — танец для комнаты"
            )
            
            await self.highrise.chat(f"🌟 {sender.username} стал VIP на {days} дней!")
            
        except Exception as e:
            print(f"[Debug] Error in on_tip: {e}")
    
    # ===== МЕТОДЫ ДЛЯ ОДЕЖДЫ =====
    
    async def get_current_outfit(self) -> list:
        """Получить текущий аутфит бота"""
        try:
            response = await self.highrise.get_my_outfit()
            if hasattr(response, 'outfit'):
                return response.outfit
            return []
        except Exception as e:
            print(f"[Debug] Get outfit error: {e}")
            return []
    
    async def equip_item_by_id(self, user: User, item_id: str):
        """Одеть вещь по ID (любая категория)"""
        try:
            # Получаем текущий аутфит
            outfit = await self.get_current_outfit()
            
            # Определяем категорию по ID
            category = item_id.split("-")[0]
            
            # Удаляем старые вещи этой категории
            new_outfit = [item for item in outfit if not item.id.startswith(category)]
            
            # Добавляем новую вещь
            new_item = Item(
                type="clothing",
                amount=1,
                id=item_id,
                account_bound=False,
                active_palette=0
            )
            new_outfit.append(new_item)
            
            # Одеваем
            await self.highrise.set_outfit(new_outfit)
            await self.highrise.send_whisper(user.id, f"✅ Одел: {item_id}")
            
        except Exception as e:
            print(f"[Debug] Equip error: {e}")
            await self.highrise.send_whisper(user.id, f"❌ Ошибка: {e}")
    
    async def unequip_item(self, user: User, category: str):
        """Снять вещь по категории"""
        try:
            # Получаем текущий аутфит
            outfit = await self.get_current_outfit()
            
            # Категории для снятия
            category_map = {
                "очки": "glasses",
                "glasses": "glasses",
                "сумка": "bag",
                "bag": "bag",
                "серьги": "earrings",
                "earrings": "earrings",
                "ожерелье": "necklace",
                "necklace": "necklace",
                "часы": "watch",
                "watch": "watch",
                "клатч": "handbag",
                "handbag": "handbag",
                "румяна": "freckle",
                "freckle": "freckle",
                "бьюти": "freckle",
                "борода": "face_hair",
                "face_hair": "face_hair",
                "усы": "face_hair",
                "брови": "eyebrow",
                "eyebrow": "eyebrow",
                "глаза": "eye",
                "eye": "eye",
                "нос": "nose",
                "nose": "nose",
                "рот": "mouth",
                "mouth": "mouth",
                "причёска": "hair_front",
                "волосы": "hair_front",
                "hair": "hair_front",
                "рубашка": "shirt",
                "shirt": "shirt",
                "штаны": "pants",
                "pants": "pants",
                "юбка": "skirt",
                "skirt": "skirt",
                "обувь": "shoes",
                "shoes": "shoes",
                "носки": "socks",
                "socks": "socks",
            }
            
            cat_key = category.lower()
            if cat_key not in category_map:
                await self.highrise.send_whisper(user.id, f"❌ Неизвестная категория: {category}")
                return
            
            cat_prefix = category_map[cat_key]
            cat_name = category
            
            # Удаляем вещи этой категории
            new_outfit = [item for item in outfit if not item.id.startswith(cat_prefix)]
            
            # Если нечего снимать
            if len(new_outfit) == len(outfit):
                await self.highrise.send_whisper(user.id, f"ℹ️ На тебе нет {cat_name}")
                return
            
            # Сохраняем базовые части лица если это лицо
            if cat_prefix in ["eye", "eyebrow", "nose", "mouth"]:
                # Добавляем базовые части лица обратно
                base_face_items = [
                    Item(type="clothing", amount=1, id="eye-n_basic2018malesquaresleepy", account_bound=False, active_palette=7),
                    Item(type="clothing", amount=1, id="eyebrow-n_basic2018newbrows07", account_bound=False, active_palette=0),
                    Item(type="clothing", amount=1, id="nose-n_basic2018newnose05", account_bound=False, active_palette=0),
                    Item(type="clothing", amount=1, id="mouth-basic2018chippermouth", account_bound=False, active_palette=-1),
                ]
                for base_item in base_face_items:
                    if not any(item.id.startswith(base_item.id.split("-")[0]) for item in new_outfit):
                        new_outfit.append(base_item)
            
            # Одеваем без снятой вещи
            await self.highrise.set_outfit(new_outfit)
            await self.highrise.send_whisper(user.id, f"✅ Снял {cat_name}")
            
        except Exception as e:
            print(f"[Debug] Unequip error: {e}")
            await self.highrise.send_whisper(user.id, f"❌ Ошибка: {e}")
    
    async def equip_item_by_number(self, user: User, category_name: str, num: int):
        """Одеть вещь по номеру из категории"""
        try:
            # Нормализуем название категории
            category_name = category_name.lower()
            
            # Получаем список категории
            if category_name in ["причёска", "волосы", "hair"]:
                item_list = HAIR_FRONT
                cat_display = "причёска"
            elif category_name in ["hair_back", "волосы_сзади"]:
                item_list = HAIR_BACK
                cat_display = "волосы сзади"
            elif category_name in ["борода", "face_hair", "усы"]:
                item_list = FACE_HAIR
                cat_display = "борода/усы"
            elif category_name in ["брови", "eyebrow"]:
                item_list = EYEBROW
                cat_display = "брови"
            elif category_name in ["глаза", "eye"]:
                item_list = EYE
                cat_display = "глаза"
            elif category_name in ["нос", "nose"]:
                item_list = NOSE
                cat_display = "нос"
            elif category_name in ["рот", "mouth"]:
                item_list = MOUTH
                cat_display = "рот"
            elif category_name in ["штаны", "pants"]:
                item_list = PANTS
                cat_display = "штаны"
            elif category_name in ["юбка", "skirt"]:
                item_list = SKIRTS
                cat_display = "юбка"
            elif category_name in ["рубашка", "shirt"]:
                item_list = SHIRT
                cat_display = "рубашка"
            elif category_name in ["обувь", "shoes"]:
                item_list = SHOES
                cat_display = "обувь"
            elif category_name in ["носки", "socks"]:
                item_list = SOCKS
                cat_display = "носки"
            elif category_name in ["очки", "glasses"]:
                item_list = GLASSES
                cat_display = "очки"
            elif category_name in ["сумка", "bag"]:
                item_list = BAG
                cat_display = "сумка"
            elif category_name in ["серьги", "earrings"]:
                item_list = EARRINGS
                cat_display = "серьги"
            elif category_name in ["ожерелье", "necklace"]:
                item_list = NECKLACE
                cat_display = "ожерелье"
            elif category_name in ["часы", "watch"]:
                item_list = WATCH
                cat_display = "часы"
            elif category_name in ["клатч", "handbag"]:
                item_list = HANDBAG
                cat_display = "клатч"
            elif category_name in ["румяна", "freckle", "бьюти"]:
                item_list = FRECKLE
                cat_display = "бьюти"
            else:
                await self.highrise.send_whisper(user.id, f"❌ Неизвестная категория: {category_name}")
                return
            
            # Проверяем номер
            if num < 1 or num > len(item_list):
                await self.highrise.send_whisper(user.id, f"❌ Номер должен быть от 1 до {len(item_list)}")
                return
            
            # Получаем item_id
            item = item_list[num - 1]
            item_id = item["id"]
            
            # Одеваем
            await self.equip_item_by_id(user, item_id)
            await self.highrise.send_whisper(user.id, f"✅ {cat_display} #{num}: {item['name']}")
            
        except Exception as e:
            print(f"[Debug] Equip by number error: {e}")
            await self.highrise.send_whisper(user.id, f"❌ Ошибка: {e}")
    
    async def is_vip(self, user_id: str) -> bool:
        """Проверить является ли пользователь VIP (купленный или официальный)"""
        try:
            import time
            # Сначала проверяем купленный VIP
            if user_id in VIP_USERS:
                expiration = VIP_USERS[user_id]
                if time.time() < expiration:
                    return True
                else:
                    # VIP истёк, удаляем
                    del VIP_USERS[user_id]
                    save_vip_users(VIP_USERS)
            
            # Проверяем официальный VIP
            privileges = await self.highrise.get_room_privilege(user_id)
            return privileges.vip == True
        except:
            return False
    
    async def is_moderator(self, user_id: str) -> bool:
        """Проверить является ли пользователь модератором"""
        try:
            privileges = await self.highrise.get_room_privilege(user_id)
            return privileges.moderator == True
        except:
            return False
    
    async def get_vip_expiration(self, user_id: str) -> int | None:
        """Получить время окончания VIP в днях"""
        try:
            import time
            if user_id in VIP_USERS:
                expiration = VIP_USERS[user_id]
                remaining = int(expiration - time.time())
                if remaining > 0:
                    return remaining // (24 * 60 * 60)
            return None
        except:
            return None
    
    async def show_vip_prices(self, user: User):
        """Показать цены на VIP"""
        lines = [
            "💰 **Цены на VIP**",
            "",
            "Отправь мне tip чтобы купить VIP:",
            "",
        ]
        for price, days in VIP_PRICES.items():
            lines.append(f"{price} голды = **{days} дней** VIP")
        lines.extend(["", "Напиши /мой_вип для проверки"])
        await self.highrise.send_whisper(user.id, "\n".join(lines))
    
    async def show_clothing_list(self, user: User, category_name: str, page: int = 1):
        """Показать список одежды категории"""
        try:
            category_name = category_name.lower()
            
            if category_name in ["причёска", "волосы", "hair"]:
                item_list = HAIR_FRONT
                cat_display = "Причёски"
            elif category_name in ["hair_back", "волосы_сзади"]:
                item_list = HAIR_BACK
                cat_display = "Волосы сзади"
            elif category_name in ["борода", "face_hair", "усы"]:
                item_list = FACE_HAIR
                cat_display = "Борода/Усы"
            elif category_name in ["брови", "eyebrow"]:
                item_list = EYEBROW
                cat_display = "Брови"
            elif category_name in ["глаза", "eye"]:
                item_list = EYE
                cat_display = "Глаза"
            elif category_name in ["нос", "nose"]:
                item_list = NOSE
                cat_display = "Нос"
            elif category_name in ["рот", "mouth"]:
                item_list = MOUTH
                cat_display = "Рот"
            elif category_name in ["штаны", "pants"]:
                item_list = PANTS
                cat_display = "Штаны"
            elif category_name in ["юбка", "skirt"]:
                item_list = SKIRTS
                cat_display = "Юбки"
            elif category_name in ["рубашка", "shirt"]:
                item_list = SHIRT
                cat_display = "Рубашки"
            elif category_name in ["обувь", "shoes"]:
                item_list = SHOES
                cat_display = "Обувь"
            elif category_name in ["носки", "socks"]:
                item_list = SOCKS
                cat_display = "Носки"
            elif category_name in ["очки", "glasses"]:
                item_list = GLASSES
                cat_display = "Очки"
            elif category_name in ["сумка", "bag"]:
                item_list = BAG
                cat_display = "Сумки"
            elif category_name in ["серьги", "earrings"]:
                item_list = EARRINGS
                cat_display = "Серьги"
            elif category_name in ["ожерелье", "necklace"]:
                item_list = NECKLACE
                cat_display = "Ожерелья"
            elif category_name in ["часы", "watch"]:
                item_list = WATCH
                cat_display = "Часы"
            elif category_name in ["клатч", "handbag"]:
                item_list = HANDBAG
                cat_display = "Клатчи"
            elif category_name in ["румяна", "freckle", "бьюти"]:
                item_list = FRECKLE
                cat_display = "Бьюти"
            else:
                await self.highrise.send_whisper(user.id, f"❌ Неизвестная категория: {category_name}")
                return
            
            PAGE_SIZE = 5
            total_pages = (len(item_list) + PAGE_SIZE - 1) // PAGE_SIZE
            page = max(1, min(page, total_pages))
            
            start = (page - 1) * PAGE_SIZE
            end = start + PAGE_SIZE
            
            lines = [f"🎽 {cat_display} — страница {page}/{total_pages}"]
            for i, item in enumerate(item_list[start:end], start=start + 1):
                lines.append(f"{i} — {item['name']}")
            
            lines.append(f"\n👉 /причёска 3 — надеть причёску #3")
            if page < total_pages:
                lines.append(f"📄 /одежда {category_name} {page+1} — следующая")
            else:
                lines.append("✅ Конец списка")
            
            await self.highrise.send_whisper(user.id, "\n".join(lines))
            
        except Exception as e:
            print(f"[Debug] Show clothing list error: {e}")
    
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
        
        # ===== VIP PRICES (/вип_цены) =====
        if msg == "/вип_цены" or msg == "/vip_prices" or msg == "вип_цены":
            await self.show_vip_prices(user)
            return
        
        # ===== MY VIP STATUS (/мой_вип) =====
        if msg == "/мой_вип" or msg == "/my_vip" or msg == "мой_вип":
            is_vip_status = await self.is_vip(user.id)
            is_mod = await self.is_moderator(user.id)
            
            if is_mod:
                await self.highrise.send_whisper(user.id, "⭐ Ты модератор - все команды доступны!")
            elif is_vip_status:
                days_left = await self.get_vip_expiration(user.id)
                if days_left:
                    await self.highrise.send_whisper(user.id, f"🌟 VIP - осталось {days_left} дней")
                else:
                    await self.highrise.send_whisper(user.id, "🌟 VIP - навсегда")
            else:
                await self.highrise.send_whisper(user.id, "💔 VIP нет\n\nНапиши /вип_цены чтобы узнать как купить!")
            return
        
        # ===== DANCE (/dance или /танцы или просто "танцы") =====
        if msg == "/dance" or msg == "/танцы" or msg == "танцы":
            # Проверка VIP
            is_vip_or_mod = await self.is_vip(user.id) or await self.is_moderator(user.id)
            if not is_vip_or_mod:
                await self.highrise.chat(f"@{user.username} ❌ Танцы только для VIP!")
                return
            await self.send_random_dance()
            return
        
        # ===== TELEPORT (/tp, /тп, /телепорт или "тп") =====
        if msg.startswith("/tp ") or msg.startswith("/тп ") or msg.startswith("/телепорт ") or msg.startswith("тп "):
            # Normalize message to use /тп prefix
            if msg.startswith("тп "):
                message = "/тп " + msg[3:]
            await self.handle_teleport(user, message)
            return
        
        # Also handle "тп центр", "тп спавн" (without second argument) - teleport self
        if msg == "тп" or msg == "тп центр" or msg == "тп спавн":
            target = msg.replace("тп", "").strip()
            if not target:
                target = "center"  # default
            await self.handle_teleport(user, f"/тп {user.username.lower()} {target}")
            return
        
        # ===== MY POS (/pos, /позиция, /координаты или просто "позиция") =====
        if msg == "/pos" or msg == "/позиция" or msg == "/координаты" or msg == "позиция" or msg == "координаты":
            await self.show_user_position(user)
            return
        
        # ===== CLOTHING (/одевать item_id) =====
        if msg.startswith("/одевать ") or msg.startswith("/wear ") or msg.startswith("одевать "):
            parts = msg.replace("/одевать ", "").replace("/wear ", "").replace("одевать ", "").strip()
            if parts:
                await self.equip_item_by_id(user, parts)
            return
        
        # ===== CLOTHING BY NUMBER (/причёска 3, /штаны 4) =====
        clothing_commands = {
            "причёска": "причёска",
            "прическа": "причёска",
            "волосы": "волосы",
            "hair": "hair",
            "hair_back": "hair_back",
            "волосы_сзади": "hair_back",
            "борода": "борода",
            "face_hair": "борода",
            "усы": "борода",
            "брови": "брови",
            "eyebrow": "брови",
            "глаза": "глаза",
            "eye": "глаза",
            "нос": "нос",
            "nose": "нос",
            "рот": "рот",
            "mouth": "рот",
            "штаны": "штаны",
            "pants": "pants",
            "юбка": "юбка",
            "skirt": "юбка",
            "рубашка": "рубашка",
            "shirt": "рубашка",
            "обувь": "обувь",
            "shoes": "обувь",
            "носки": "носки",
            "socks": "носки",
            "очки": "очки",
            "glasses": "очки",
            "сумка": "сумка",
            "bag": "сумка",
            "серьги": "серьги",
            "earrings": "серьги",
            "ожерелье": "ожерелье",
            "necklace": "ожерелье",
            "часы": "часы",
            "watch": "часы",
            "клатч": "клатч",
            "handbag": "клатч",
            "румяна": "румяна",
            "freckle": "румяна",
            "бьюти": "румяна",
        }
        
        for cmd, category in clothing_commands.items():
            if msg.startswith(f"{cmd} ") or msg == cmd:
                if msg == cmd:
                    # Показать список если просто название категории
                    await self.show_clothing_list(user, category)
                else:
                    # Надеть по номеру
                    parts = msg.replace(cmd, "").strip()
                    if parts.isdigit():
                        await self.equip_item_by_number(user, category, int(parts))
                    else:
                        await self.show_clothing_list(user, category)
                return
        
        # ===== CLOTHING LIST (/одежда причёска) =====
        if msg.startswith("/одежда ") or msg.startswith("/clothing "):
            parts = msg.replace("/одежда ", "").replace("/clothing ", "").strip().split()
            if parts:
                category = parts[0]
                page = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                await self.show_clothing_list(user, category, page)
            return
        
        # ===== UNEQUIP (/снять очки, /снять сумку) =====
        if msg.startswith("/снять ") or msg.startswith("/unequip ") or msg.startswith("снять "):
            parts = msg.replace("/снять ", "").replace("/unequip ", "").replace("снять ", "").strip()
            if parts:
                await self.unequip_item(user, parts)
            else:
                await self.highrise.send_whisper(user.id, "ℹ️ Использование: /снять очки | /снять сумку | /снять борода")
            return
        
        # ===== ALL (все X) =====
        if msg.startswith("все ") or msg.startswith("all "):
            try:
                # Проверка VIP
                is_vip_or_mod = await self.is_vip(user.id) or await self.is_moderator(user.id)
                if not is_vip_or_mod:
                    await self.highrise.chat(f"@{user.username} ❌ Команда /все только для VIP!")
                    return
                
                # Извлекаем номер из сообщения
                parts = msg.replace("все ", "").replace("all ", "").strip()
                if parts.isdigit():
                    idx = int(parts) - 1
                    if 0 <= idx < len(timed_emotes):
                        em = timed_emotes[idx]
                        emote_id = em.get("value")
                        em_name = em.get("text")
                        await self.highrise.chat(f"✨ {em_name} для всех!")
                        await self.send_emote_to_all(emote_id, em_name)
                        return
            except Exception as e:
                print(f"[Debug] Error in 'all' command: {e}")
        
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
