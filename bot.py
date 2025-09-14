import os
import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# ---------------- Config ----------------
API_ID = int(os.environ.get("5047271"))
API_HASH = os.environ.get("047d9ed308172e637d4265e1d9ef0c2")
BOT_TOKEN = os.environ.get("8464050626:AAFjoldNU_A5jHEzSspCDDNUy5__WyEFfms")
# ---------------------------------------

app = Client("fb_insta_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inline buttons stacked vertically
buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://t.me/deweni2")],
    [InlineKeyboardButton("Support Group", url="https://t.me/slmusicmania")]
])

# Start command
@app.on_message(filters.command(["start"]) & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "Hi! Send me a Facebook or Instagram link and I will download the video/photo for you.",
        reply_markup=buttons
    )

# Regex to detect FB or IG links
URL_REGEX = r"(https?://(?:www\.)?(facebook|fb|instagram|insta)\.com/[^\s]+)"

@app.on_message(filters.text & filters.private)
async def link_handler(client, message):
    urls = re.findall(URL_REGEX, message.text)
    if not urls:
        await message.reply_text("❌ No valid Facebook or Instagram link found!")
        return

    url = urls[0][0]
    await message.reply_text("⏳ Downloading your video/photo...")

    # Setup yt-dlp
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
    }

    try:
        os.makedirs("downloads", exist_ok=True)

        # Extract info & download
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: download_media(url,_
