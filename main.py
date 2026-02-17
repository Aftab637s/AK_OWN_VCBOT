import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# --- 1. Clients Setup ---
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("MusicAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call_py = PyTgCalls(user)

# --- 2. Direct YouTube Downloader (No API) ---
def get_audio_url(link):
    opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
        # Agar cookies file hai to yahan path dena padega future mein
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(link, download=False)
        return info['url'], info.get('title', 'Unknown Song')

# --- 3. Play Command (/play link) ---
@bot.on_message(filters.command("play") & filters.group)
async def play_music(client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Bhai link to de! Example: /play https://youtube.com/...")

    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    await message.reply_text(f"🔍 **Searching:** `{query}`")

    try:
        # Link nikal rahe hain (Direct)
        stream_url, title = get_audio_url(query)
        
        await message.reply_text(f"▶️ **Playing:** {title}")

        # Call join kar rahe hain
        await call_py.play(
            chat_id,
            MediaStream(
                stream_url,
            )
        )
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {e}")

# --- 4. Start Bot ---
async def start_bot():
    print("Bot Starting...")
    await bot.start()
    await user.start()
    await call_py.start()
    print("Bot is Online! 🎵")
    await idle()

if __name__ == "__main__":
    from pyrogram import idle
    bot.run(start_bot())
