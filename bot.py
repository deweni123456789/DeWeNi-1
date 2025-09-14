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

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "Hi! Send me a Facebook or Instagram link and I will dow
