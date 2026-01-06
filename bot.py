# -*- coding: utf-8 -*-
"""
Telegram Video Downloader Bot
Professional bot with ads system
"""

import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config import (
    BOT_TOKEN, ADS_ENABLED, ADMIN_IDS, 
    SUPPORTED_PLATFORMS, FORCE_CHANNEL, FORCE_CHANNEL_USERNAME
)
from ads_manager import AdsManager
from downloader import VideoDownloader

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize managers
ads_manager = AdsManager()
downloader = VideoDownloader()

# Rate limiting
user_last_request = {}
RATE_LIMIT_SECONDS = 3

# ============== Helper Functions ==============

def is_rate_limited(user_id: int) -> bool:
    """Check if user is rate limited"""
    now = datetime.now()
    if user_id in user_last_request:
        diff = (now - user_last_request[user_id]).total_seconds()
        if diff < RATE_LIMIT_SECONDS:
            return True
    user_last_request[user_id] = now
    return False

def get_main_keyboard():
    """Get main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Platforms", callback_data="platforms"),
            InlineKeyboardButton("📊 My Stats", callback_data="my_stats")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("📢 Channel", url="https://t.me/your_channel")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_user_level(downloads: int) -> tuple:
    """Get user level based on downloads"""
    levels = [
        (0, "🌱 Beginner", "Bronze"),
        (10, "🥉 Bronze", "Bronze"),
        (50, "🥈 Silver", "Silver"),
        (100, "🥇 Gold", "Gold"),
        (500, "💎 Diamond", "Diamond")
    ]
    
    current_level = levels[0]
    for threshold, name, tier in levels:
        if downloads >= threshold:
            current_level = (threshold, name, tier)
    
    return current_level

# ============== Command Handlers ==============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    
    # Register user
    ads_manager.register_user(user_id, user.first_name)
    
    welcome_text = f"""
🎬 Welcome {user.first_name}!

Welcome to the Professional Video Downloader Bot! 🚀

✨ What I can do:
• Download videos from 20+ platforms
• Support YouTube, TikTok, Instagram & more
• High quality up to 4K
• Super fast download speed

📝 How to use:
Just send me any video link and I'll download it for you!

⬇️ Try now - Send a video link!
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
❓ User Guide

📌 Available Commands:
• /start - Start the bot
• /help - Show help
• /platforms - Supported platforms
• /stats - Your statistics

📥 How to download:
1️⃣ Copy the video link
2️⃣ Send it to the bot
3️⃣ Wait for download
4️⃣ Receive your video!

⚠️ Notes:
• Max file size: 50MB
• Some videos are protected
• Quality depends on availability

📞 Support: @your_support
"""
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            help_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]])
        )
    else:
        await update.message.reply_text(help_text)

async def platforms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /platforms command"""
    platforms_text = """
📋 Supported Platforms

🎬 Video Platforms:
• 🔴 YouTube - Videos & Shorts
• 📺 Vimeo - Professional videos
• 📹 Dailymotion - Various videos

📱 Social Media:
• 📷 Instagram - Reels & videos
• 🎵 TikTok - Short videos
• 🐦 Twitter/X - Tweet videos
• 📘 Facebook - Videos & reels
• 💬 Telegram - Channel videos

🎮 Other Platforms:
• 🎮 Twitch - Clips & highlights
• 🔗 Reddit - Post videos
• 🎵 SoundCloud - Audio clips
• 📌 Pinterest - Videos

✅ And many more!
"""
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            platforms_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]])
        )
    else:
        await update.message.reply_text(platforms_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id
    stats = ads_manager.get_user_stats(user_id)
    
    downloads = stats.get('downloads', 0)
    level_info = get_user_level(downloads)
    
    stats_text = f"""
📊 Your Statistics

👤 User: {update.effective_user.first_name}
🏆 Level: {level_info[1]}

📥 Downloads: {downloads}
📅 Joined: {stats.get('joined', 'Unknown')}

💡 Keep downloading to level up!
"""
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            stats_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]])
        )
    else:
        await update.message.reply_text(stats_text)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ You are not authorized!")
        return
    
    report = ads_manager.get_admin_report()
    
    admin_text = f"""
🔐 Admin Panel

📊 General Statistics:
👥 Total Users: {report['total_users']}
📥 Total Downloads: {report['total_downloads']}
📈 Active Today: {report['active_today']}

🎯 Ad Statistics:
👁️ Views: {report['ad_views']}
🖱️ Clicks: {report['ad_clicks']}
📊 CTR: {report['ctr']}%

⏰ Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    await update.message.reply_text(admin_text)

# ============== Video Download Handler ==============

async def handle_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video URL messages"""
    user_id = update.effective_user.id
    url = update.message.text.strip()
    
    # Rate limiting
    if is_rate_limited(user_id):
        await update.message.reply_text("⏳ Please wait before next request...")
        return
    
    # Check if URL is valid
    if not any(platform in url.lower() for platform in ['youtube', 'youtu.be', 'tiktok', 'instagram', 
                                                         'twitter', 'x.com', 'facebook', 'fb.', 
                                                         'vimeo', 'dailymotion', 'twitch', 'reddit',
                                                         'pinterest', 'soundcloud', 'telegram', 't.me']):
        await update.message.reply_text(
            "❌ Unsupported link!\n\n"
            "📋 Use /platforms to see supported platforms."
        )
        return
    
    # Send processing message
    status_msg = await update.message.reply_text(
        "⏳ Downloading...\n\n"
        "🔄 Please wait..."
    )
    
    try:
        # Show typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
        
        # Download video
        result = await downloader.download_video(url, user_id)
        
        if result['success']:
            file_path = result['file_path']
            
            # Update status
            await status_msg.edit_text("📤 Sending video...")
            
            # Send video
            with open(file_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ Downloaded successfully!\n\n🎬 {result.get('title', 'Video')}"
                )
            
            # Delete status message
            await status_msg.delete()
            
            # Record download
            ads_manager.record_download(user_id)
            
            # Show ad if enabled
            if ADS_ENABLED:
                ad = ads_manager.get_smart_ad(user_id)
                if ad:
                    ad_keyboard = InlineKeyboardMarkup([[
                        InlineKeyboardButton(ad['button_text'], url=ad['url'])
                    ]])
                    await update.message.reply_text(
                        ad['text'],
                        reply_markup=ad_keyboard,
                        disable_web_page_preview=True
                    )
            
            # Cleanup
            try:
                os.remove(file_path)
            except:
                pass
                
        else:
            await status_msg.edit_text(
                f"❌ Download failed!\n\n"
                f"Reason: {result.get('error', 'Unknown error')}\n\n"
                f"💡 Try another link or check the URL."
            )
            
    except asyncio.TimeoutError:
        await status_msg.edit_text(
            "⏰ Download timeout!\n\n"
            "💡 Video is too large or server is slow."
        )
    except Exception as e:
        logger.error(f"Download error: {e}")
        await status_msg.edit_text(
            "❌ Unexpected error!\n\n"
            "💡 Please try again later."
        )

# ============== Callback Handler ==============

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "platforms":
        await platforms_command(update, context)
    elif data == "my_stats":
        await stats_command(update, context)
    elif data == "help":
        await help_command(update, context)
    elif data == "back_main":
        welcome_text = """
🎬 Main Menu

📥 Send a video link to download

✨ Supported Platforms:
YouTube, TikTok, Instagram, Twitter, Facebook & more!
"""
        await query.message.edit_text(
            welcome_text,
            reply_markup=get_main_keyboard()
        )
    elif data.startswith("ad_click_"):
        ads_manager.record_ad_click(query.from_user.id)

# ============== Main ==============

def main():
    """Main function"""
    print("=" * 50)
    print("Video Downloader Pro Bot")
    print("=" * 50)
    print("Starting...")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("platforms", platforms_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("admin", admin_command))
    
    # Callback handler
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    # URL handler
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'https?://'),
        handle_video_url
    ))
    
    print("Bot is ready!")
    print("-" * 50)
    print("Commands: /start /help /platforms /stats /admin")
    print("-" * 50)
    print("Bot is running... (Ctrl+C to stop)")
    
    # Run bot
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
