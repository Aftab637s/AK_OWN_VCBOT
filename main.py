import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# --- Clients Setup ---
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("MusicAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call_py = PyTgCalls(user)

# --- Smart Downloader (Link ya Search dono chalega) ---
def get_audio_url(query):
    opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
    }
    
    # Agar Link nahi hai, toh YouTube par Search karo
    if not query.startswith("http"):
        query = f"ytsearch:{query}"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        
        # Agar search result hai, toh pehla video uthao
        if 'entries' in info:
            info = info['entries'][0]
            
        return info['url'], info.get('title', 'Unknown Song')

# --- Play Command ---
@bot.on_message(filters.command("play") & filters.group)
async def play_music(client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Example: /play Believer")

    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    msg = await message.reply_text(f"🔍 **Searching:** `{query}`")

    try:
        stream_url, title = get_audio_url(query)
        
        await msg.edit_text(f"▶️ **Playing:** {title}")

        await call_py.play(
            chat_id,
            MediaStream(stream_url)
        )
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {e}")

# --- Start Bot ---
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
