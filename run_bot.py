"""
Auto-reconnect script for Highrise bot
Based on: https://itzvini.notion.site/Auto-Reconnect-efe354a932114337a07949670ab70aa7
"""
from highrise.__main__ import *
import time
import os

# Get credentials from environment variables
bot_file_name = "bot"
bot_class_name = "Bot"
room_id = os.environ.get("HIGHRISE_ROOM_ID") or os.environ.get("ROOM_ID")
bot_token = os.environ.get("HIGHRISE_API_TOKEN") or os.environ.get("BEARER_TOKEN")

if not room_id or not bot_token:
    print("ERROR: Missing HIGHRISE_ROOM_ID or HIGHRISE_API_TOKEN")
    exit(1)

print(f"[Reconnect] Starting bot for room: {room_id}")

my_bot = BotDefinition(
    getattr(import_module(bot_file_name), bot_class_name)(), 
    room_id, 
    bot_token
)

while True:
    try:
        definitions = [my_bot]
        arun(main(definitions))
    except Exception as e:
        print(f"[Reconnect] Exception occurred: {e}")
        print(f"[Reconnect] Reconnecting in 5 seconds...")
        time.sleep(5)
