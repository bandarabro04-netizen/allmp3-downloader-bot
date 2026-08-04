"""
Social Media MP3 Downloader — Telegram Bot
-------------------------------------------
Send this bot any link (YouTube, Instagram, TikTok, Facebook, Twitter/X,
SoundCloud, and most other sites yt-dlp supports) and it replies with
the audio as an MP3 file.

Setup:
    1. pip install -r requirements.txt
    2. Install ffmpeg on your system (see README.md)
    3. Set your bot token as an environment variable:
           export BOT_TOKEN="123456:ABC-your-telegram-bot-token"
    4. Run:
           python bot.py
"""

import os
import re
import logging
import tempfile
import shutil
from pathlib import Path

import yt_dlp
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Fallback: if BOT_TOKEN isn't set as an environment variable, read it from
# a token.txt file placed next to this script (one line, just the token).
if not BOT_TOKEN:
    _token_file = Path(__file__).resolve().parent / "token.txt"
    if _token_file.exists():
        BOT_TOKEN = _token_file.read_text(encoding="utf-8").strip()

# Telegram bots can only send files up to this size via the normal Bot API.
MAX_TELEGRAM_FILE_MB = 50

URL_REGEX = re.compile(r"https?://\S+")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("mp3_bot")


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hi! Send me a link from YouTube, Instagram, TikTok, Facebook, "
        "Twitter/X, SoundCloud, etc. and I'll send you back the audio as MP3.\n\n"
        "Just paste the link here 🔗"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "How to use:\n"
        "1. Copy a video/audio link from any supported site.\n"
        "2. Paste it here in the chat.\n"
        "3. Wait a bit — I'll download and send the MP3.\n\n"
        f"Note: Telegram bots can only send files up to {MAX_TELEGRAM_FILE_MB}MB."
    )


def _extract_url(text: str) -> str | None:
    match = URL_REGEX.search(text or "")
    return match.group(0) if match else None


def _download_audio(url: str, out_dir: str) -> str:
    """Downloads best audio from `url` and converts it to mp3 inside out_dir.
    Returns the path to the resulting mp3 file."""
    outtmpl = str(Path(out_dir) / "%(title).100s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # After the postprocessor runs, the extension becomes mp3
        base = ydl.prepare_filename(info)
        mp3_path = str(Path(base).with_suffix(".mp3"))

    if not os.path.exists(mp3_path):
        # Fallback: find any mp3 that got created in out_dir
        mp3_files = list(Path(out_dir).glob("*.mp3"))
        if mp3_files:
            mp3_path = str(mp3_files[0])
        else:
            raise FileNotFoundError("MP3 conversion failed — no output file found.")

    return mp3_path


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    url = _extract_url(text)

    if not url:
        await update.message.reply_text(
            "That doesn't look like a link 🤔 Send me a URL from a supported site."
        )
        return

    status_msg = await update.message.reply_text("⏳ Downloading & converting to MP3...")
    await update.effective_chat.send_action(ChatAction.UPLOAD_VOICE)

    tmp_dir = tempfile.mkdtemp(prefix="mp3bot_")
    try:
        mp3_path = _download_audio(url, tmp_dir)

        size_mb = os.path.getsize(mp3_path) / (1024 * 1024)
        if size_mb > MAX_TELEGRAM_FILE_MB:
            await status_msg.edit_text(
                f"⚠️ The audio is {size_mb:.1f}MB, which is over Telegram's "
                f"{MAX_TELEGRAM_FILE_MB}MB bot upload limit, so I can't send it."
            )
            return

        title = Path(mp3_path).stem
        with open(mp3_path, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=title,
                filename=f"{title}.mp3",
            )
        await status_msg.delete()

    except yt_dlp.utils.DownloadError as e:
        logger.warning("Download error for %s: %s", url, e)
        await status_msg.edit_text(
            "❌ Couldn't download that link. It might be private, unsupported, "
            "or removed."
        )
    except Exception as e:
        logger.exception("Unexpected error for %s", url)
        await status_msg.edit_text(f"❌ Something went wrong: {e}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN environment variable is not set.\n"
            "Get a token from @BotFather on Telegram, then run:\n"
            '  export BOT_TOKEN="your-token-here"'
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
