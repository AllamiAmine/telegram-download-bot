# âš™ï¸ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Bot Ø§Ù„Ù…ØªÙ‚Ø¯Ù…
# ================================
# ðŸš€ Ø£ÙØ¶Ù„ Bot Ù„ØªØ­Ù…ÙŠÙ„ Ø§Ù„ÙÙŠØ¯ÙŠÙˆÙ‡Ø§Øª Ù…Ø¹ Ù†Ø¸Ø§Ù… Ø¥Ø¹Ù„Ø§Ù†Ø§Øª Ø°ÙƒÙŠ

# ðŸ”‘ Token Ø¯ÙŠØ§Ù„ Bot (Ø¬ÙŠØ¨Ùˆ Ù…Ù† @BotFather)
BOT_TOKEN = "8121760517:AAEBIBGmbtBjQOCrtq2pG1wu4osKL-lkxeo"

# ðŸ‘‘ Ù…Ø¹Ø±Ù Ø§Ù„Ù…Ø´Ø±Ù (Ø¶Ø¹ Ø§Ù„Ù€ ID Ø¯ÙŠØ§Ù„Ùƒ Ù‡Ù†Ø§)
ADMIN_IDS = []  # Ù…Ø«Ø§Ù„: [123456789, 987654321]

# ðŸ“¢ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ø¥Ø¹Ù„Ø§Ù†Ø§Øª
ADS_ENABLED = True
SHOW_AD_AFTER_DOWNLOADS = 1  # Ø¥Ø¸Ù‡Ø§Ø± Ø¥Ø¹Ù„Ø§Ù† Ø¨Ø¹Ø¯ ÙƒÙ„ X ØªØ­Ù…ÙŠÙ„

# ðŸŽ¯ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø¥Ø¹Ù„Ø§Ù†Ø§Øª Ø§Ù„Ù…ØªÙ‚Ø¯Ù…Ø©
ADS_LIST = [
    {
        "id": "vpn_ad",
        "text": """ðŸ”¥ **Ø¹Ø±Ø¶ Ø®Ø§Øµ!**

ðŸš€ VPN Ø³Ø±ÙŠØ¹ ÙˆØ¢Ù…Ù† Ù„Ù„ØªØ­Ù…ÙŠÙ„ Ø¨Ø¯ÙˆÙ† Ø­Ø¯ÙˆØ¯!
ðŸ“± ÙŠØ¹Ù…Ù„ Ø¹Ù„Ù‰ Ø¬Ù…ÙŠØ¹ Ø§Ù„Ø£Ø¬Ù‡Ø²Ø©
ðŸŽ **3 Ø£ÙŠØ§Ù… Ù…Ø¬Ø§Ù†Ø§Ù‹**
âš¡ Ø³Ø±Ø¹Ø© ÙØ§Ø¦Ù‚Ø© + Ø­Ù…Ø§ÙŠØ© ÙƒØ§Ù…Ù„Ø©

ðŸ‘‡ Ø§Ø¶ØºØ· Ø§Ù„Ø²Ø± Ù„Ù„ØªØ­Ù…ÙŠÙ„""",
        "button_text": "ðŸ“¥ Ø§Ø­ØµÙ„ Ø¹Ù„Ù‰ VPN Ù…Ø¬Ø§Ù†Ø§Ù‹",
        "button_url": "https://your-affiliate-link.com/vpn",
        "image": None,
        "priority": 1,
        "active": True,
        "category": "vpn"
    },
    {
        "id": "app_ad",
        "text": """ðŸ“± **ØªØ·Ø¨ÙŠÙ‚ Ø±Ù‡ÙŠØ¨ Ù„Ù„ØªØ­Ù…ÙŠÙ„!**

ðŸŽ¬ Ø­Ù…Ù‘Ù„ ÙÙŠØ¯ÙŠÙˆÙ‡Ø§Øª Ø¨Ø¬ÙˆØ¯Ø© 4K
âš¡ Ø£Ø³Ø±Ø¹ Ù…Ù† Ø£ÙŠ ØªØ·Ø¨ÙŠÙ‚ Ø¢Ø®Ø±
ðŸ’¾ Ø­ÙØ¸ Ù…Ø¨Ø§Ø´Ø± ÙÙŠ Ø§Ù„Ø¬Ù‡Ø§Ø²
ðŸ”¥ **Ù…Ø¬Ø§Ù†ÙŠ 100%**

ðŸ‘‡ Ø­Ù…Ù‘Ù„Ù‡ Ø§Ù„Ø¢Ù†""",
        "button_text": "ðŸ“² ØªØ­Ù…ÙŠÙ„ Ø§Ù„ØªØ·Ø¨ÙŠÙ‚",
        "button_url": "https://your-affiliate-link.com/app",
        "image": None,
        "priority": 2,
        "active": True,
        "category": "app"
    },
    {
        "id": "channel_ad",
        "text": """ðŸ“¢ **Ø§Ù†Ø¶Ù… Ù„Ù‚Ù†Ø§ØªÙ†Ø§ Ø§Ù„Ø­ØµØ±ÙŠØ©!**

ðŸŽ¥ ÙÙŠØ¯ÙŠÙˆÙ‡Ø§Øª ÙŠÙˆÙ…ÙŠØ© Ù…Ù…ÙŠØ²Ø©
ðŸ”¥ Ù…Ø­ØªÙˆÙ‰ Ø­ØµØ±ÙŠ
ðŸ’¡ Ù†ØµØ§Ø¦Ø­ ØªÙ‚Ù†ÙŠØ©
ðŸŽ Ù…Ø³Ø§Ø¨Ù‚Ø§Øª ÙˆØ¬ÙˆØ§Ø¦Ø²

ðŸ‘‡ Ø§Ù†Ø¶Ù… Ø§Ù„Ø¢Ù† - Ù…Ø¬Ø§Ù†Ø§Ù‹!""",
        "button_text": "ðŸ“¢ Ø§Ù†Ø¶Ù… Ù„Ù„Ù‚Ù†Ø§Ø©",
        "button_url": "https://t.me/YourChannel",
        "image": None,
        "priority": 3,
        "active": True,
        "category": "channel"
    }
]

# â° Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ù…ÙƒØ§ÙØ­Ø© Spam (Ø°ÙƒÙŠØ©)
MIN_AD_INTERVAL = 1
MAX_ADS_PER_USER_DAILY = 15
COOLDOWN_SECONDS = 3

# ðŸ“Š Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªØªØ¨Ø¹ ÙˆØ§Ù„Ø¥Ø­ØµØ§Ø¦ÙŠØ§Øª
TRACK_CLICKS = True
STATS_FILE = "stats.json"
USERS_FILE = "users.json"

# ðŸŽ¬ Ø§Ù„Ù…Ù†ØµØ§Øª Ø§Ù„Ù…Ø¯Ø¹ÙˆÙ…Ø© Ù„Ù„ØªØ­Ù…ÙŠÙ„ (Ù…ÙˆØ³Ù‘Ø¹Ø©)
SUPPORTED_PLATFORMS = [
    # YouTube
    "youtube.com", "youtu.be", "youtube-nocookie.com",
    # TikTok
    "tiktok.com", "vm.tiktok.com", "vt.tiktok.com",
    # Instagram
    "instagram.com", "instagr.am",
    # Twitter/X
    "twitter.com", "x.com", "t.co",
    # Facebook
    "facebook.com", "fb.watch", "fb.com",
    # Reddit
    "reddit.com", "redd.it",
    # Pinterest
    "pinterest.com", "pin.it",
    # Vimeo
    "vimeo.com",
    # Dailymotion
    "dailymotion.com", "dai.ly",
    # Twitch
    "twitch.tv", "clips.twitch.tv",
    # Snapchat
    "snapchat.com",
]

# ðŸŽ¨ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Bot
BOT_NAME = "ðŸŽ¬ Video Downloader Pro"

# ðŸ“£ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ø¥Ø¬Ø¨Ø§Ø±ÙŠØ© (Ø§Ø®ØªÙŠØ§Ø±ÙŠ)
FORCE_CHANNEL = False
FORCE_CHANNEL_USERNAME = "@YourChannel"
FORCE_CHANNEL_URL = "https://t.me/YourChannel"

# ðŸ”’ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ø£Ù…Ø§Ù†
RATE_LIMIT_ENABLED = True
MAX_REQUESTS_PER_MINUTE = 10

# ðŸ“¦ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªØ­Ù…ÙŠÙ„
MAX_FILE_SIZE_MB = 50
DOWNLOAD_TIMEOUT = 300

