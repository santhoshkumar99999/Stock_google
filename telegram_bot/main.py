import os
import re
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# 1. Get these from https://my.telegram.org
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# 2. The source channel name (or username, or ID)
# Make sure your Telegram account has joined this channel!
SOURCE_CHANNEL = "NIFTY STOCK TRADES SEBI Reg.RA" 

# 3. Bot Configuration
# Get bot token from BotFather (https://t.me/botfather)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The Chat ID where the bot should send the signals.
# You can get your chat ID by messaging @userinfobot or adding your bot to a channel.
TARGET_CHAT = os.getenv("TARGET_CHAT")

# Initialize the user client (to read messages from the channel)
# This requires your personal phone number login the first time.
user_client = TelegramClient('user_session', API_ID, API_HASH)

# Initialize the bot client (to send messages)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

def is_trading_signal(text):
    """
    Checks if a message contains buy/sell signals for Nifty/Bank Nifty.
    Customize the keywords based on the exact format of the channel.
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Keywords to look for
    action_keywords = ['buy', 'sell', 'long', 'short', 'call', 'put', 'ce', 'pe']
    asset_keywords = ['nifty', 'banknifty', 'bank nifty', 'finnifty', 'sensex']
    
    has_action = any(keyword in text_lower for keyword in action_keywords)
    has_asset = any(keyword in text_lower for keyword in asset_keywords)
    
    return has_action and has_asset

@user_client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def new_message_handler(event):
    """
    Listens for new messages in the source channel.
    """
    message_text = event.message.message
    
    # Check if the message matches our signal criteria
    if is_trading_signal(message_text):
        print(f"✅ Fast Signal Detected!\n{message_text}\n")
        
        # Format the message to look automated and clean
        formatted_message = f"🚀 **AUTOMATED TRADING SIGNAL** 🚀\n\n{message_text}\n\n🤖 _Forwarded by your fast bot_"
        
        try:
            # Send the message using the Bot Client to your target chat
            await bot_client.send_message(int(TARGET_CHAT), formatted_message)
            print("➡️ Successfully sent to destination bot!")
        except Exception as e:
            print(f"❌ Error sending message: {e}")

async def main():
    print("Starting Telegram clients...")
    
    # Start the bot client
    await bot_client.start(bot_token=BOT_TOKEN)
    
    # Start the user client (will prompt for phone number/code on first run)
    await user_client.start()
    
    print(f"📡 Listening for signals in '{SOURCE_CHANNEL}'...")
    print(f"🎯 Target Chat ID: {TARGET_CHAT}")
    print("Press Ctrl+C to stop.\n")
    
    # Keep the script running
    await user_client.run_until_disconnected()

if __name__ == '__main__':
    # Run the async main loop
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    if not all([API_ID, API_HASH, BOT_TOKEN, TARGET_CHAT]):
        print("⚠️ ERROR: Missing environment variables.")
        print("Please ensure API_ID, API_HASH, BOT_TOKEN, and TARGET_CHAT are set in the .env file.")
    else:
        asyncio.run(main())
