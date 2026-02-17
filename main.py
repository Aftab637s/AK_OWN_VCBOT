# --- Smart Downloader (Fix for Format Error) ---
def get_audio_url(query):
    opts = {
        'format': 'bestaudio',      # <--- Change: Sirf 'bestaudio' rakha hai
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
        'cookiefile': 'cookies.txt',
        'source_address': '0.0.0.0',
    }
    
    # Agar Link nahi hai, toh YouTube par Search karo
    if not query.startswith("http"):
        query = f"ytsearch:{query}"

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
        except Exception:
            # Agar bestaudio fail ho jaye, toh worst try karo (backup)
            opts['format'] = 'worstaudio'
            with yt_dlp.YoutubeDL(opts) as ydl_backup:
                info = ydl_backup.extract_info(query, download=False)
        
        if 'entries' in info:
            info = info['entries'][0]
            
        return info['url'], info.get('title', 'Unknown Song')
