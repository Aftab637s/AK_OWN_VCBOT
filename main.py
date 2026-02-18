import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("MusicAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call_py = PyTgCalls(user)

def get_audio_url(query):
    # Change: 'bestaudio/best' ka matlab hai "Jo bhi mile utha lo"
    opts = {
        'format': 'bestaudio/best', 
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
        'cookiefile': 'cookies.txt',
        'source_address': '0.0.0.0',
    }
    
    if not query.startswith("http"):
        query = f"ytsearch:{query}"

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
        except Exception:
            # Fallback agar pehla fail ho jaye
            opts['format'] = 'worstaudio'
            with yt_dlp.YoutubeDL(opts) as ydl_backup:
                info = ydl_backup.extract_info(query, download=False)
        
        if 'entries' in info:
            info = info['entries'][0]
            
        return info['url'], info.get('title', 'Unknown Song')

@bot.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
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

async def start_bot():
    print("--- STARTING BOT... ---")
    await bot.start()
    await user.start()
    await call_py.start()
    print("--- BOT ONLINE ---")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
