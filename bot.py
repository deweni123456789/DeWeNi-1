import os
import re
import asyncio
from datetime import datetime, timezone, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# ---------------- Config ----------------
API_ID = 5047271
API_HASH = "047d9ed308172e637d4265e1d9ef0c27"
BOT_TOKEN = "8464050626:AAFjoldNU_A5jHEzSspCDDNUy5__WyEFfms"
DOWNLOAD_FOLDER = "downloads"
# ---------------------------------------

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app = Client("fb_insta_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inline buttons
buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://t.me/deweni2")],
    [InlineKeyboardButton("Support Group", url="https://t.me/slmusicmania")]
])

# ---------------- Start Command ----------------
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "Hi! Send me a Facebook or Instagram link and I will download it for you.",
        reply_markup=buttons
    )

# ---------------- Helpers ----------------
URL_REGEX = r"(https?://(?:www\.)?(facebook|fb|instagram|insta)\.com/[^\s]+)"

def sanitize_filename(name: str) -> str:
    """Remove invalid characters and extra spaces."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)  # remove illegal chars
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized

def download_media(url, opts):
    """Download media and return safe file path."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # Sanitize filename
    safe_title = sanitize_filename(info['title'])
    ext = info.get('ext', 'mp4')
    safe_file = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.{ext}")

    # Rename if original file contains unsafe characters
    original_file = os.path.join(DOWNLOAD_FOLDER, f"{info['title']}.{ext}")
    if os.path.exists(original_file) and original_file != safe_file:
        try:
            os.rename(original_file, safe_file)
        except FileNotFoundError:
            pass  # fallback to safe_file

    info['safe_file'] = safe_file
    return info

# ---------------- Link Handler ----------------
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
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
    }

    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: download_media(url, ydl_opts))

        downloaded_file = info['safe_file']
        size_mb = round(os.path.getsize(downloaded_file) / (1024 * 1024), 2)

        # Uploaded time in Sri Lanka timezone (UTC+5:30)
        sri_lanka_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        uploaded_time = sri_lanka_time.strftime("%Y-%m-%d %H:%M:%S")

        requester = message.from_user.mention
        caption = f"💾 Size: {size_mb} MB\n🕒 Uploaded: {uploaded_time}\n👤 Requested by: {requester}"

        await message.reply_document(downloaded_file, caption=caption, reply_markup=buttons)

        os.remove(downloaded_file)

    except Exception as e:
        await message.reply_text(f"❌ Failed to download.\nError: {e}")

# ---------------- Run Bot ----------------
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
