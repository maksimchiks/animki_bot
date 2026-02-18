"""
Auto-reconnect script for Highrise bot
"""
from highrise.__main__ import *
import time
import os
import sys

def main_loop():
    # Get credentials from environment variables
    bot_file_name = "bot"
    bot_class_name = "Bot"
    room_id = os.environ.get("HIGHRISE_ROOM_ID") or os.environ.get("ROOM_ID")
    bot_token = os.environ.get("HIGHRISE_API_TOKEN") or os.environ.get("BEARER_TOKEN")
    
    if not room_id or not bot_token:
        print("ERROR: Missing HIGHRISE_ROOM_ID or HIGHRISE_API_TOKEN")
        return False
    
    print(f"[Reconnect] Starting bot for room: {room_id}")
    
    my_bot = BotDefinition(
        getattr(import_module(bot_file_name), bot_class_name)(), 
        room_id, 
        bot_token
    )
    
    while True:
        try:
            print("[Reconnect] Connecting to Highrise...")
            definitions = [my_bot]
            arun(main(definitions))
            print("[Reconnect] Connection ended, retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("[Reconnect] Bot stopped by user")
            return False
        except BaseException as e:
            print(f"[Reconnect] Exception: {e}")
            print(f"[Reconnect] Restarting in 5 seconds...")
            time.sleep(5)
            # Создаём новый экземпляр бота при каждом перезапуске
            my_bot = BotDefinition(
                getattr(import_module(bot_file_name), bot_class_name)(), 
                room_id, 
                bot_token
            )

if __name__ == "__main__":
    while True:
        if not main_loop():
            break
