import os
import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# ---------------- Config ----------------
API_ID = 5047271
API_HASH = "047d9ed308172e637d4265e1d9ef0c27"
BOT_TOKEN = "8464050626:AAFjoldNU_A5jHEzSspCDDNUy5__WyEFfms"
# ---------------------------------------

app = Client("fb_insta_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inline buttons stacked vertically
buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://t.me/deweni2")],
    [InlineKeyboardButton("Support Group", url="https://t.me/slmusicmania")]
])

# ---------------- Start Command ----------------
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "Hi! Send me a Facebook or Instagram link and I will download the video/photo for you.",
        reply_markup=buttons
    )

# ---------------- Link Detection & Download ----------------
URL_REGEX = r"(https?://(?:www\.)?(facebook|fb|instagram|insta)\.com/[^\s]+)"

def sanitize_filename(name: str) -> str:
    """Remove invalid characters for filenames."""
    return re.sub(r'[\\/:"*?<>|]+', "", name)

def download_media(url, opts):
    """Download media and return info with safe file path."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    # Sanitize filename
    safe_title = sanitize_filename(info['title'])
    safe_file = os.path.join("downloads", f"{safe_title}.{info['ext']}")
    original_file = os.path.join("downloads", f"{info['title']}.{info['ext']}")
    if original_file != safe_file:
        os.rename(original_file, safe_file)
    info['safe_file'] = safe_file
    return info

@app.on_message(filters.text & filters.private)
async def link_handler(client, message):
    urls = re.findall(URL_REGEX, message.text)
    if not urls:
        await message.reply_text("❌ No valid Facebook or Instagram link found!")
        return

    url = urls[0][0]
    await message.reply_text("⏳ Downloading your video/photo...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
    }

    try:
        os.makedirs("downloads", exist_ok=True)
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: download_media(url, ydl_opts))

        downloaded_file = info['safe_file']
        duration = int(info.get("duration", 0))
        size_mb = round(os.path.getsize(downloaded_file) / (1024 * 1024), 2)
        metadata = f"🎬 Title: {info['title']}\n⏱ Duration: {duration} sec\n💾 Size: {size_mb} MB"

        await message.reply_document(downloaded_file, caption=f"{metadata}\n✅ Download completed!", reply_markup=buttons)
        os.remove(downloaded_file)

    except Exception as e:
        await message.reply_text(f"❌ Failed to download.\nError: {e}")

# ---------------- Run Bot ----------------
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
