import json
import os
import datetime
import asyncio
import logging
import requests
import io
import html
import re
import base64
from typing import Dict, List, Optional, Union
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    BotCommand,
    Audio,
    Video
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.error import TelegramError

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= CONFIG =================
BOT_TOKEN = "8400631140:AAEEyl7sYKZGbuQgfm82Kg6yN9exhKfe8jo"
ADMIN_ID = 7998441787
BOT_USERNAME = "SynaxOsnitBot"  # Replace with your bot username

# File paths
USERS_FILE = "users.json"
PAYMENTS_FILE = "payments.json"
COUPONS_FILE = "coupons.json"
CREDIT_COSTS_FILE = "credit_costs.json"
BANNED_USERS_FILE = "banned_users.json"
SETTINGS_FILE = "settings.json"
STATS_FILE = "stats.json"  # New file for detailed statistics

# API Configuration
API_KEY = "anshapi"  # Updated API key
API_URL = "https://sh1vam-api-num.netlify.app/.netlify/functions/numberinfo?num="  # Updated API URL
VEHICLE_API_URL = "https://revangevichelinfo.vercel.app/api/rc"
# Face Swap API
FACE_SWAP_API_URL = "https://ab-faceswap.vercel.app/swap"
# Pincode API
PINCODE_API_URL = "https://api.postalpincode.in/pincode"
# IP Info API
IP_INFO_API_URL = "https://ab-ipinfoapi.vercel.app/ipinfo"
# Number to Name API
NUM_NAME_API_URL = "https://abbas-apis.vercel.app/api/num-name"
# Spotify API
SPOTIFY_API_URL = "https://py-today-spotify-api.vercel.app/api/spotify?song="
SPOTIFY_URL_API_URL = "https://py-today-spotify-api.vercel.app/api/spotify?url="  # New URL for Spotify URL download
# Instagram API
INSTAGRAM_API_URL = "https://synax-id-info.synaxbots.workers.dev/info?username="
# Instagram Reel Downloader API
INSTAGRAM_REEL_API_URL = "https://insta-dl.hazex.workers.dev/?url="
# Free Fire API
FREEFIRE_API_URL = "https://info-strikerxyash.vercel.app/player-info?uid="
# Text to Voice API
TEXT_TO_VOICE_API_URL = "https://api.hazex.sbs/tts"
# YouTube Downloader API
YOUTUBE_API_URL = "https://tele-social.vercel.app/down?url="
# GST Lookup API
GST_API_URL = "https://gstlookup.hideme.eu.org/?gstNumber="

# Payment Configuration
UPI_ID = "SynaxBots@ybl"
PAYMENT_QR_URL = "https://i.ibb.co/nsfk7Vx0/20260112-051110.jpg"  # Replace with your QR code image

# Images
WELCOME_IMAGE = "https://i.ibb.co/gbhKxbjX/file-00000000458472079c0d45d8f85c8d23.png"
ACCOUNT_IMAGE = "https://i.ibb.co/cSV8Z7Cg/file-0000000028b47208bbbd1c5150d14056.png"
PAYMENT_IMAGE = PAYMENT_QR_URL
INFO_IMAGE = "https://i.ibb.co/B56xdY6f/file-00000000525c71fa8b601089f6bdc213.png"
REFERRAL_IMAGE = "https://i.ibb.co/rGcTz9R2/file-0000000037ac72088f94dd30e9aff061.png"
SEARCH_IMAGE = "https://i.ibb.co/Mk0NLsyV/Picsart-26-01-13-13-13-23-499.jpg"
SEARCH_RESULT_IMAGE = "https://i.ibb.co/Mk0NLsyV/Picsart-26-01-13-13-13-23-499.jpg"
VEHICLE_SEARCH_IMAGE = "https://i.ibb.co/sv7Wh7Jj/Picsart-26-01-13-13-18-04-129.jpg"
FACE_SWAP_IMAGE = "https://i.ibb.co/1tgJqxQR/Picsart-26-01-13-13-14-47-137.jpg"  # Image for face swap feature
PINCODE_SEARCH_IMAGE = "https://i.ibb.co/396ZRbw6/Picsart-26-01-13-13-17-29-807.jpg"  # Image for pincode search
IP_INFO_SEARCH_IMAGE = "https://i.ibb.co/b5bkJ0DH/Picsart-26-01-13-13-16-18-728.jpg"  # Image for IP info search
NUM_NAME_SEARCH_IMAGE = "https://i.ibb.co/WvCvvFP4/Picsart-26-01-13-13-15-40-246.jpg"  # Image for number to name search
SPOTIFY_SEARCH_IMAGE = "https://i.ibb.co/yn6kGsjg/file-000000004be87207bbc4d85e8782b51a.png"  # Image for Spotify search
INSTAGRAM_SEARCH_IMAGE = "https://i.ibb.co/bjBWTR9f/Picsart-26-01-13-13-14-14-775.jpg"  # Image for Instagram search
INSTAGRAM_REEL_IMAGE = "https://i.ibb.co/zTP1JS1F/file-0000000075c47209ab090a68d4b985c2.png"  # Image for Instagram Reel Downloader
FREEFIRE_SEARCH_IMAGE = "https://i.ibb.co/Q3r3pf2Q/Picsart-26-01-13-12-58-22-693.jpg"  # Image for Free Fire search
TEXT_TO_VOICE_IMAGE = "https://i.ibb.co/bgmR332v/file-0000000063d07206a5b74d72573170d7.png"  # Image for Text to Voice
YOUTUBE_SEARCH_IMAGE = "https://i.ibb.co/rR3Prhqs/file-00000000509c71fd95db30c2f2e988f6.png"  # Image for YouTube Downloader
JOIN_IMAGE = "https://i.ibb.co/sdrfRLJd/file-00000000cb987208926a77979a9c0338.png"  # Image for join channel screen
MAINTENANCE_IMAGE = "https://i.ibb.co/twKv01yL/71-Ugwa-C4-Dj-L-AC-UF1000-1000-QL80.jpg"  # Maintenance mode image
GST_SEARCH_IMAGE = "https://i.ibb.co/W4gzyjWq/file-00000000832c71f89eced99428ebf79b.png"  # Image for GST Number Lookup
STYLISH_TEXT_IMAGE = "https://i.ibb.co/gFttkZyy/file-000000009f2c7209b00cf7aecaa187a6-1.png"  # Image for Stylish Text Generator

# Force Join Channels (Hardcoded) - CHANGE THESE TO YOUR CHANNELS
FORCE_JOIN_CHANNELS = [
    {"id": -1003750507861, "link": "https://t.me/SynaxBotz", "name": "𝘽𝙤𝙩𝙨 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💚"},
    {"id": -1002682084939, "link": "https://t.me/Synaxchatgroup", "name": "𝘾𝙝𝙖𝙩 𝙂𝙧𝙤𝙪𝙥 💛"}
]

# Conversation states
PAYMENT_PLAN, PAYMENT_SCREENSHOT = range(2)
BROADCAST_TYPE, BROADCAST_CONTENT = range(2)
COUPON_CREATE = range(3)
COUPON_GEN_DETAILS = range(1)  # For advanced coupon generation
FACE_SWAP_SOURCE, FACE_SWAP_TARGET = range(2)  # For face swap conversation
CREDIT_COST_EDIT = range(1)  # For editing credit costs
BAN_USER, BAN_REASON = range(2)  # For banning users
STYLISH_TEXT_MODE = range(1)  # For stylish text generation mode

# ==========================================

# ================= STYLISH TEXT GENERATOR =================
# Font mapping for stylish text
FONT_MAP = {
    "a":"ᴧ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"є","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ",
    "j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ϻ","n":"η","o":"σ","p":"ᴘ","q":"ǫ","r":"ꝛ",
    "s":"s","t":"ᴛ","u":"υ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ",
    
    "A":"𝐀‌","B":"𝐁‌","C":"𝐂‌","D":"𝐃‌","E":"𝐄‌","F":"𝐅‌","G":"𝐆‌",
    "H":"𝐇‌","I":"𝐈‌","J":"𝐉‌","K":"𝐊‌","L":"𝐋‌","M":"𝐌‌","N":"𝐍‌",
    "O":"𝐎‌","P":"𝐏‌","Q":"𝐐‌","R":"𝐑‌","S":"𝐒‌","T":"𝐓‌","U":"𝐔‌",
    "V":"𝐕‌","W":"𝐖‌","X":"𝐗‌","Y":"𝐘‌","Z":"𝐙‌",
}

def convert_to_stylish(text: str) -> str:
    """Convert text to stylish font using FONT_MAP"""
    return "".join(FONT_MAP.get(ch, ch) for ch in text)

# List of style pairs (prefix, suffix) - All styles from the provided code
STYLES = [
    ("𓂃❛ ⟶", "❜ 🌙⤹🌸"),
    ("❍⏤●", "●───♫▷"),
    ("🤍 ⍣⃪ ᶦ ᵃᵐ⛦⃕", "❛𝆺𝅥⤹࿗𓆪ꪾ™"),
    ("𓆰𝅃🔥", "⃪⍣꯭꯭𓆪꯭🝐"),
    ("◄❥❥⃝⃪⃕🦚⟵᷽᷍", "˚◡⃝🐬᪳𔘓❁❍•:➛"),
    ("➺꯭꯭꯭𝅥𝆬🦋⃪꯭─⃛┼", "🥵⃝⃝ᬽ⃪꯭꯭➺꯭⎯⎯᪵᪳"),
    ("◄⏤🝛꯭𝐈𝛕ᷟ𝚣⃪ꙴ🥀⃝⃪", "⃝☠⎯꯭𓆩♡꧂"),
    ("🦋⃟≛⃝⋆⋆≛⃞", "𝄟🦋⃟≛⃝≛"),
    ("𐏓𓆩❤🔥𓆪𝆺꯭𝅥༎ࠫ⛧", "ࠫ༎𝆺𝅥𓆩⍣꯭⃟🍷༎᪵⛧"),
    ("𓄂𝆺𝅥⃝🥀⃪⃪꯭ᷟ⃜𖥫꯭꯭꯭𝆺꯭꯭𝅥", "𝆺꯭𝅥🎭🌹꯭"),
    ("𓄂─⃛𓆩🫧𝆺𝅥⃝𐏓", "㋛𓆪꯭⵿٭🍃"),
    ("◄⏤⃪⃝⃪𐏓🝛꯭", "⸙ꠋꠋꠋꠋꠋ⛦⃪⃪🝛꯭••➤"),
    ("🎡𓆩᪵🌸⃝۫𝞄⃕𝖋𝖋꯭ᜊ𝆺𝅥⃝", "┼⃖ꭗ🦋¦🌺--🎋"),
    ("⛦⃕𝄟•๋๋๋๋๋๋๋๋๋๋๋๋๋๋๋🦋⃟⃟⃟≛⃝💖", "🦋•๋๋๋๋๋๋๋๋๋๋๋๋๋๋๋𝄟"),
    ("••ᯓ❥๋๋๋๋๋๋๋๋๋๋๋๋๋๋๋ꗝ༎꯭ࠫ🤍𝆺꯭𝅥", "𝆺꯭𝅥༎ࠫ◡⃝𑲭"),
    ("𝐈𝛕ᷟ𝚣⃪ꙴ⋆†།┼⃖•🔥⃞⃪⃜", "🔥⃞⃪⃜𓆪🦋✿"),
    ("❍─⃜𓆩〭⃛〬🤍𓆪˹", ".⍣⃪ꭗ𝆺𝅥𔘓🪽"),
    ("𝆺𝅥اـ꯭ـ꯭𝞂⃕𝝲𝝴꯭•⚚•𝆺꯭𝅥", "𝆺꯭𝅥ꀭ‧₊𝁾⟶🍃˚"),
    ("◄⏤🔥⃝⃪🐼𓆩꯭❛", "❜꯭𓆪⎯⟶"),
    ("❍─⃜𓆩〭⃛〬👒𓆪⃪꯭", "🤍᪳𝆺꯭𝅥⎯⎯"),
    ("◄⏤❥≛⃝", "🍁⃝➤🕊⃝🝐"),
    ("°ꗝؖ༎꯭ࠫᜊ𝆺꯭𝅥🔥⃝❥༎ࠫ𝆺꯭𝅥", "༎ࠫ٭⃪꯭꯭⃜ꬑ�"),
    ("◄⏤🫧⃝⃪🦋꯭", "◡⃝ا۬🌸᪳𝆺꯭𝅥⎯꯭"),
    ("◄ᯓ❥≛⃝🌸꯭", "💗⃝꯭꯭❥꯭꯭✿꯭꯭࿐"),
    ("❝ .𝁘ໍ ", "🍷𐏓𝟑 ༗ آ‌⃖𝄤𝅃"),
    ("𓍼 ໋݊ ", " ⌯ ™| 💗"),
    ("𝄟🦋⃟≛⃝ ", "🦋⃟❤"),
    ("ᯓ𓆰 𝅃꯭꯭꯭꯭꯭❛-", "-֟፝…𓆪᭄ꪾ"),
    ("⛦⃕𝄟•๋๋๋๋๋๋🦋⃟⃟⃟≛⃝💖", "🦋•๋๋๋๋๋๋𝄟⛦⃕"),
    ("𓆩🔥⃝⃪❥༎꯭ࠫ", "꯭༎ࠫ❥⃪⃝🔥𓆪"),
    ("••ᯓ❥๋๋๋๋๋ꗝ༎꯭ࠫ🤍𝆺꯭𝅥", "𝆺꯭𝅥༎ࠫ◡⃝𑲭"),
    ("𐏓𓆩❤🔥𓆪𝆺꯭𝅥༎ࠫ⛧", "⛧༎ࠫ𝆺꯭𝅥𓆩🍷𓆪"),
    ("🎡𓆩᪵🌸⃝۫𝞄⃕𝖋𝖋꯭ᜊ𝆺𝅥⃝", "┼⃖ꭗ🦋¦🌺--🎋"),
    ("𓄂𝆺𝅥⃝🥀⃪⃪꯭ᷟ⃜𖥫꯭꯭꯭𝆺꯭꯭𝅥", "𝆺꯭𝅥🎭🌹꯭"),
    ("◄⏤⃪⃝⃪𐏓🝛꯭𝐈𝛕ᷟ𝚣ꙴ", "⸙ꠋꠋꠋꠋꠋ⛦⃪⃪🝛꯭"),
    ("𓂃⃝💞⃪𓆩🦋⃟≛⃝", "⃝≛⃟🦋𓆪⃪💞⃝𓂃"),
    ("❍─⃜𓆩〭⃛〬🤍𓆪˹", ".⍣⃪ꭗ𝆺𝅥𔘓🪽"),
    ("𓆩🧿⃝🦋⃪⛦⃕", "⛦⃪⃕🦋⃝🧿𓆪"),
    ("◄⏤🔥⃝⃪🐼𓆩꯭❛", "❜꯭𓆪🐼⃪⃝🔥⏤►"),
    ("°ꗝؖ༎꯭ࠫᜊ𝆺꯭𝅥🔥⃝❥༎ࠫ𝆺꯭𝅥", "༎ࠫ٭⃪꯭꯭⃜ꬑ�"),
    ("𓆰⃝🔥𝆺꯭꯭꯭𝅥𓆩❥", "❥𓆪꯭꯭꯭𝆺𝅥🔥⃝𓆰"),
    ("◄ᯓ❥≛⃝🌸꯭", "💗⃝꯭꯭❥꯭꯭✿꯭꯭࿐"),
    ("𓆩💀⃝🖤⃪☠", "☠⃪🖤⃝💀𓆪"),
    ("⛧⃝🔥⃪𓆩👑", "👑𓆪⃪🔥⃝⛧"),
    ("𓂀⃝🦋⃪⛦⃕💫", "💫⃕⛦⃪🦋⃝𓂀"),
    ("◄⏤🎭⃝⃪𓆩", "𓆪⃪⃝🎭⏤►"),
    ("𓆩⚡⃝🔥⃪💥", "💥⃪🔥⃝⚡𓆪"),
    ("✦⃝💫⃪𓆩🌌", "🌌𓆪⃪💫⃝✦"),
    ("𓆩🍷⃝✨⃪⛧", "⛧⃪✨⃝🍷𓆪"),
    ("❛⃝🌑⃪𓆩☠", "☠𓆪⃪🌑⃝❛"),
    ("◄ᯓ🖤⃝⃪💀", "💀⃪⃝🖤ᯓ►"),
    ("𓆩🎀⃝💖⃪⛦", "⛦⃪💖⃝🎀𓆪"),
    ("✧⃝🌺⃪𓆩🦋", "🦋𓆪⃪🌺⃝✧"),
    ("𓆩🔥⃝⚔⃪👑", "👑⃪⚔⃝🔥𓆪"),
    ("◄⏤🌪⃝⃪💫", "💫⃪⃝🌪⏤►"),
    ("𓆩🕯⃝🌑⃪☠", "☠⃪🌑⃝🕯𓆪"),
    ("⛦⃕⃝🔥⃪𓆩💎", "💎𓆪⃪🔥⃝⛦⃕"),
]

# ==========================================

# ================= DATA HANDLERS =================
def load_json_file(filename: str) -> dict:
    """Load data from JSON file with error handling"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
    return {}

def save_json_file(filename: str, data: dict) -> bool:
    """Save data to JSON file with error handling"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving {filename}: {e}")
        return False

def load_users() -> dict:
    return load_json_file(USERS_FILE)

def save_users(data: dict) -> bool:
    return save_json_file(USERS_FILE, data)

def load_payments() -> dict:
    return load_json_file(PAYMENTS_FILE)

def save_payments(data: dict) -> bool:
    return save_json_file(PAYMENTS_FILE, data)

def load_coupons() -> dict:
    return load_json_file(COUPONS_FILE)

def save_coupons(data: dict) -> bool:
    return save_json_file(COUPONS_FILE, data)

def load_credit_costs() -> dict:
    """Load credit costs configuration"""
    costs = load_json_file(CREDIT_COSTS_FILE)
    
    # Default costs if file doesn't exist or is empty
    if not costs:
        costs = {
            "number_search": 1,
            "vehicle_search": 2,
            "face_swap": 5,
            "pincode_search": 1,
            "ip_info_search": 2,
            "num_name_search": 1,
            "spotify_search": 2,  # Spotify search by name
            "spotify_url_search": 2,  # Spotify search by URL
            "instagram_search": 2,  # Instagram username search
            "instagram_reel_download": 3,  # Instagram Reel Downloader
            "freefire_search": 2,  # Free Fire UID search
            "text_to_voice": 1,  # Text to Voice
            "youtube_download": 3,  # YouTube video download
            "gst_search": 2,  # GST Number Lookup
            "stylish_text": 1  # Stylish Text Generator
        }
        save_credit_costs(costs)
    
    return costs

def save_credit_costs(data: dict) -> bool:
    """Save credit costs configuration"""
    return save_json_file(CREDIT_COSTS_FILE, data)

def get_credit_cost(feature: str) -> int:
    """Get credit cost for a specific feature"""
    costs = load_credit_costs()
    return costs.get(feature, 1)  # Default to 1 if not found

def load_banned_users() -> dict:
    """Load banned users list"""
    return load_json_file(BANNED_USERS_FILE)

def save_banned_users(data: dict) -> bool:
    """Save banned users list"""
    return save_json_file(BANNED_USERS_FILE, data)

def load_settings() -> dict:
    """Load bot settings"""
    settings = load_json_file(SETTINGS_FILE)
    
    # Default settings if file doesn't exist or is empty
    if not settings:
        settings = {
            "maintenance_mode": False,
            "maintenance_message": "🔧 Bot is under maintenance. Please try again later.",
            "broadcast_message": None,
            "broadcast_sent": False
        }
        save_settings(settings)
    
    return settings

def save_settings(data: dict) -> bool:
    """Save bot settings"""
    return save_json_file(SETTINGS_FILE, data)

def load_stats() -> dict:
    """Load detailed statistics"""
    stats = load_json_file(STATS_FILE)
    
    # Default stats if file doesn't exist or is empty
    if not stats:
        stats = {
            "total_searches": {
                "number_search": 0,
                "vehicle_search": 0,
                "face_swap": 0,
                "pincode_search": 0,
                "ip_info_search": 0,
                "num_name_search": 0,
                "spotify_search": 0,
                "spotify_url_search": 0,
                "instagram_search": 0,
                "instagram_reel_download": 0,
                "freefire_search": 0,
                "text_to_voice": 0,
                "youtube_download": 0,
                "gst_search": 0,
                "stylish_text": 0
            },
            "daily_searches": {},
            "monthly_searches": {},
            "total_revenue": 0,
            "credits_spent": 0,
            "premium_purchases": 0,
            "coupon_redemptions": 0
        }
        save_stats(stats)
    
    return stats

def save_stats(data: dict) -> bool:
    """Save detailed statistics"""
    return save_json_file(STATS_FILE, data)

def update_search_stats(feature: str, credits_used: int = 0):
    """Update search statistics"""
    try:
        stats = load_stats()
        
        # Update total searches
        if feature not in stats["total_searches"]:
            stats["total_searches"][feature] = 0
        stats["total_searches"][feature] += 1
        
        # Update daily searches
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today not in stats["daily_searches"]:
            stats["daily_searches"][today] = {}
        if feature not in stats["daily_searches"][today]:
            stats["daily_searches"][today][feature] = 0
        stats["daily_searches"][today][feature] += 1
        
        # Update monthly searches
        this_month = datetime.datetime.now().strftime("%Y-%m")
        if this_month not in stats["monthly_searches"]:
            stats["monthly_searches"][this_month] = {}
        if feature not in stats["monthly_searches"][this_month]:
            stats["monthly_searches"][this_month][feature] = 0
        stats["monthly_searches"][this_month][feature] += 1
        
        # Update credits spent and revenue
        stats["credits_spent"] += credits_used
        stats["total_revenue"] += credits_used * 0.1  # Assuming 1 credit = ₹0.1
        
        save_stats(stats)
    except Exception as e:
        logger.error(f"Error updating search stats: {e}")

def update_payment_stats(plan_type: str, amount: int):
    """Update payment statistics"""
    try:
        stats = load_stats()
        
        if plan_type == "premium":
            stats["premium_purchases"] += 1
            stats["total_revenue"] += amount * 2  # Assuming average premium price
        else:
            stats["total_revenue"] += amount * 0.1  # Assuming 1 credit = ₹0.1
        
        save_stats(stats)
    except Exception as e:
        logger.error(f"Error updating payment stats: {e}")

def update_coupon_stats():
    """Update coupon redemption statistics"""
    try:
        stats = load_stats()
        stats["coupon_redemptions"] += 1
        save_stats(stats)
    except Exception as e:
        logger.error(f"Error updating coupon stats: {e}")

# ==========================================

# ================= USER MANAGEMENT =================
def get_user(user_id: str) -> dict:
    """Get or create user data"""
    users = load_users()
    if user_id not in users:
        users[user_id] = {
            "balance": 5,  # Starting bonus
            "premium": False,
            "premium_expiry": None,
            "referrals": 0,
            "referral_earnings": 0,
            "referred_by": None,
            "joined_at": datetime.datetime.now().isoformat()
        }
        save_users(users)
    return users[user_id]

def update_user(user_id: str, data: dict) -> bool:
    """Update user data"""
    users = load_users()
    if user_id in users:
        users[user_id].update(data)
        return save_users(users)
    return False

def add_credits(user_id: str, amount: int) -> bool:
    """Add credits to user"""
    try:
        user = get_user(user_id)
        user["balance"] += amount
        return update_user(user_id, user)
    except Exception as e:
        logger.error(f"Error adding credits: {e}")
        return False

def remove_credits(user_id: str, amount: int) -> bool:
    """Remove credits from user"""
    try:
        user = get_user(user_id)
        user["balance"] = max(0, user["balance"] - amount)
        return update_user(user_id, user)
    except Exception as e:
        logger.error(f"Error removing credits: {e}")
        return False

def add_premium(user_id: str, days: int) -> bool:
    """Add premium days to user"""
    try:
        user = get_user(user_id)
        current_expiry = None
        
        if user["premium_expiry"]:
            try:
                current_expiry = datetime.datetime.fromisoformat(user["premium_expiry"])
            except:
                pass
        
        if current_expiry and current_expiry > datetime.datetime.now():
            new_expiry = current_expiry + datetime.timedelta(days=days)
        else:
            new_expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        
        user["premium"] = True
        user["premium_expiry"] = new_expiry.isoformat()
        return update_user(user_id, user)
    except Exception as e:
        logger.error(f"Error adding premium: {e}")
        return False

def remove_premium(user_id: str) -> bool:
    """Remove premium from user"""
    try:
        user = get_user(user_id)
        user["premium"] = False
        user["premium_expiry"] = None
        return update_user(user_id, user)
    except Exception as e:
        logger.error(f"Error removing premium: {e}")
        return False

def check_premium_expiry():
    """Check and remove expired premium"""
    try:
        users = load_users()
        current_time = datetime.datetime.now()
        updated = False
        
        for user_id, user_data in users.items():
            if user_data.get("premium") and user_data.get("premium_expiry"):
                try:
                    expiry = datetime.datetime.fromisoformat(user_data["premium_expiry"])
                    if expiry < current_time:
                        user_data["premium"] = False
                        user_data["premium_expiry"] = None
                        updated = True
                except:
                    pass
        
        if updated:
            save_users(users)
    except Exception as e:
        logger.error(f"Error checking premium expiry: {e}")

def is_premium_user(user_id: str) -> bool:
    """Check if user has active premium"""
    try:
        user = get_user(user_id)
        
        # Check if user has premium
        if not user.get("premium", False):
            return False
        
        # Check if premium has expired
        if user.get("premium_expiry"):
            try:
                expiry = datetime.datetime.fromisoformat(user["premium_expiry"])
                if expiry < datetime.datetime.now():
                    # Premium has expired, update user data
                    user["premium"] = False
                    user["premium_expiry"] = None
                    update_user(user_id, user)
                    return False
                return True
            except:
                # If there's an error parsing the expiry date, consider premium invalid
                user["premium"] = False
                user["premium_expiry"] = None
                update_user(user_id, user)
                return False
        
        # If no expiry date is set, consider premium valid
        return True
    except Exception as e:
        logger.error(f"Error checking premium status: {e}")
        return False

# ==========================================

# ================= BAN SYSTEM =================
def is_user_banned(user_id: str) -> bool:
    """Check if user is banned"""
    try:
        banned_users = load_banned_users()
        return user_id in banned_users
    except Exception as e:
        logger.error(f"Error checking ban status: {e}")
        return False

def ban_user(user_id: str, reason: str = "No reason provided") -> bool:
    """Ban a user"""
    try:
        banned_users = load_banned_users()
        banned_users[user_id] = {
            "reason": reason,
            "banned_at": datetime.datetime.now().isoformat()
        }
        return save_banned_users(banned_users)
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        return False

def unban_user(user_id: str) -> bool:
    """Unban a user"""
    try:
        banned_users = load_banned_users()
        if user_id in banned_users:
            del banned_users[user_id]
            return save_banned_users(banned_users)
        return False
    except Exception as e:
        logger.error(f"Error unbanning user: {e}")
        return False

def get_ban_info(user_id: str) -> Optional[dict]:
    """Get ban information for a user"""
    try:
        banned_users = load_banned_users()
        return banned_users.get(user_id)
    except Exception as e:
        logger.error(f"Error getting ban info: {e}")
        return None

# ==========================================

# ================= MAINTENANCE SYSTEM =================
def is_maintenance_mode() -> bool:
    """Check if maintenance mode is active"""
    try:
        settings = load_settings()
        return settings.get("maintenance_mode", False)
    except Exception as e:
        logger.error(f"Error checking maintenance mode: {e}")
        return False

def set_maintenance_mode(enabled: bool, message: str = None) -> bool:
    """Enable or disable maintenance mode"""
    try:
        settings = load_settings()
        settings["maintenance_mode"] = enabled
        if message:
            settings["maintenance_message"] = message
        return save_settings(settings)
    except Exception as e:
        logger.error(f"Error setting maintenance mode: {e}")
        return False

def get_maintenance_message() -> str:
    """Get maintenance message"""
    try:
        settings = load_settings()
        return settings.get("maintenance_message", "🔧 Bot is under maintenance. Please try again later.")
    except Exception as e:
        logger.error(f"Error getting maintenance message: {e}")
        return "🔧 Bot is under maintenance. Please try again later."

# ==========================================

# ================= SERVICE STATE MANAGEMENT =================
def clear_service_states(context: ContextTypes.DEFAULT_TYPE):
    """Clear all service states in context"""
    service_states = [
        "awaiting_number", "awaiting_vehicle", 
        "awaiting_pincode", "awaiting_ip", "awaiting_num_name", 
        "awaiting_coupon", "face_swap_state",
        "face_swap_source", "awaiting_spotify", "awaiting_spotify_url",  # Added both Spotify states
        "awaiting_instagram", "awaiting_instagram_reel",  # Added Instagram states
        "awaiting_freefire",  # Added Free Fire state
        "awaiting_text_to_voice",  # Added Text to Voice state
        "awaiting_youtube",  # Added YouTube state
        "awaiting_gst",  # Added GST state
        "awaiting_stylish_text",  # Added Stylish Text state
        "stylish_text_mode",  # Added for stylish text generation mode
        "ban_user_id", "ban_reason", "unban_user_id"
    ]
    
    for state in service_states:
        if state in context.user_data:
            del context.user_data[state]

# ==========================================

# ================= CHANNEL MANAGEMENT =================
def get_required_channels() -> List[dict]:
    """Get list of required channels"""
    return FORCE_JOIN_CHANNELS

async def check_channel_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE, retry_count: int = 0) -> bool:
    """Check if user is member of all required channels with retry mechanism"""
    required_channels = get_required_channels()
    
    if not required_channels:
        return True
    
    # Maximum number of retries
    max_retries = 2
    
    for channel in required_channels:
        try:
            member = await context.bot.get_chat_member(channel["id"], user_id)
            if member.status not in ["member", "administrator", "creator"]:
                # If not a member and we haven't reached max retries, try again after a delay
                if retry_count < max_retries:
                    await asyncio.sleep(1)  # Wait 1 second before retrying
                    return await check_channel_membership(user_id, context, retry_count + 1)
                return False
        except TelegramError as e:
            logger.error(f"Error checking channel membership: {e}")
            # If there's an error and we haven't reached max retries, try again
            if retry_count < max_retries:
                await asyncio.sleep(1)  # Wait 1 second before retrying
                return await check_channel_membership(user_id, context, retry_count + 1)
            return False
    
    return True

async def send_force_join_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send force join message with channel buttons"""
    required_channels = get_required_channels()
    
    if not required_channels:
        return True
    
    # Check which channels the user hasn't joined
    not_joined = []
    for channel in required_channels:
        try:
            member = await context.bot.get_chat_member(channel["id"], update.effective_user.id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except TelegramError as e:
            logger.error(f"Error checking channel membership: {e}")
            not_joined.append(channel)
    
    # If user has joined all channels, show main menu
    if not not_joined:
        await show_main_menu(update, context)
        return True
    
    # Create keyboard with channels not joined
    keyboard = []
    for channel in not_joined:
        keyboard.append([InlineKeyboardButton(f"📢 {channel['name']}", url=channel["link"])])
    
    keyboard.append([InlineKeyboardButton("✅ I've Joined All Channels", callback_data="check_joined")])
    keyboard.append([InlineKeyboardButton("🔄 Refresh Status", callback_data="refresh_join_status")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Count joined and total channels
    joined_count = len(required_channels) - len(not_joined)
    total_count = len(required_channels)
    
    await update.message.reply_photo(
        photo=JOIN_IMAGE,
        caption=(
            f"⚠️ *Mandatory Channels Required*\n\n"
            f"📊 Progress: {joined_count}/{total_count} channels joined\n\n"
            f"Please join all channels below to use the bot:\n\n"
            f"⚡ *Channels not joined:* {len(not_joined)}\n"
            f"✅ *Channels joined:* {joined_count}"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return False

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the main menu"""
    user_id = str(update.effective_user.id)
    user = get_user(user_id)
    
    # Clear any active service states when returning to main menu
    clear_service_states(context)
    
    # Create main menu
    keyboard = [
        [InlineKeyboardButton("💳 Buy Credits", callback_data="buy_credits"),InlineKeyboardButton("👑 Buy Premium", callback_data="buy_premium")],
        [InlineKeyboardButton("👤 My Account", callback_data="my_account")],
        [InlineKeyboardButton("🔗 Referral", callback_data="referral"),InlineKeyboardButton("🎫 Coupon Code", callback_data="coupon")],
        [InlineKeyboardButton("🔍 Search Number", callback_data="search_number"),InlineKeyboardButton("🚗 Vehicle RC Search", callback_data="vehicle_search")],
        [InlineKeyboardButton("🎭 Face Swap", callback_data="face_swap")],
        [InlineKeyboardButton("📍 Pincode Search", callback_data="pincode_search"),InlineKeyboardButton("🌐 IP Info Search", callback_data="ip_info_search")],
        [InlineKeyboardButton("📞 Number to Name", callback_data="num_name_search"),InlineKeyboardButton("📷 Instagram Info", callback_data="instagram_search")],
        [InlineKeyboardButton("🎵 Spotify Music", callback_data="spotify_menu"),InlineKeyboardButton("🔥 Free Fire Info", callback_data="freefire_search")],
        [InlineKeyboardButton("📹 Instagram Reel DL", callback_data="instagram_reel_download"),InlineKeyboardButton("🔊 Text to Voice", callback_data="text_to_voice")],
        [InlineKeyboardButton("📺 YouTube Downloader", callback_data="youtube_download"),InlineKeyboardButton("🧾 GST Number Lookup", callback_data="gst_search")],
        [InlineKeyboardButton("✨ Stylish Text", callback_data="stylish_text")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Get user stats for welcome message
    premium_status = "✅ Active" if is_premium_user(user_id) else "❌ Inactive"
    
    if update.message:
        # For message handlers
        await update.message.reply_photo(
            photo=WELCOME_IMAGE,
            caption=(
                f"*👋 Welcome to Synax Osnit*\n\npowerful all-in-one bot jo daily useful tools provide karta hai — fast, simple aur user-friendly.\n🔹 Mobile Number Lookup\n🔹 Vehicle Registration Search\n🔹 AI Face Swap\n🔹 Pincode Finder\n🔹 IP Address Lookup\n🔹 Number to Name\n🔹 Instagram Username Info\n🔹 Instagram Reel Downloader\n🔹 Spotify Music Downloader\n🔹 Free Fire Player Info\n🔹 Text to Voice Converter\n🔹 YouTube Video Downloader\n🔹 GST Number Lookup\n🔹 Stylish Text Generator\n\n⚡ Fast • Secure • Easy to Use\n📌 Sab features ek hi bot me\n— Made by @synaxnetwork —\n\n"
                f"👤 *User:* {update.effective_user.first_name}\n"
                f"💰 *Credits:* {user.get('balance', 0)}\n"
                f"👑 *Premium:* {premium_status}\n\n"
                f"Choose an option below to get started:"
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        # For callback query handlers
        query = update.callback_query
        try:
            await query.edit_message_media(
                media=InputMediaPhoto(
                    media=WELCOME_IMAGE,
                    caption=(
                        f"*👋 Welcome to Synax Osnit*\n\npowerful all-in-one bot jo daily useful tools provide karta hai — fast, simple aur user-friendly.\n🔹 Mobile Number Lookup\n🔹 Vehicle Registration Search\n🔹 AI Face Swap\n🔹 Pincode Finder\n🔹 IP Address Lookup\n🔹 Number to Name\n🔹 Instagram Username Info\n🔹 Instagram Reel Downloader\n🔹 Spotify Music Downloader\n🔹 Free Fire Player Info\n🔹 Text to Voice Converter\n🔹 YouTube Video Downloader\n🔹 GST Number Lookup\n🔹 Stylish Text Generator\n\n⚡ Fast • Secure • Easy to Use\n📌 Sab features ek hi bot me\n— Made by @synaxnetwork —\n\n"
                        f"👤 *User:* {query.from_user.first_name}\n"
                        f"💰 *Credits:* {user.get('balance', 0)}\n"
                        f"👑 *Premium:* {premium_status}\n\n"
                        f"Choose an option below to get started:"
                    ),
                    parse_mode="Markdown"
                ),
                reply_markup=reply_markup
            )
        except:
            # If edit fails, send new message
            await context.bot.send_photo(
                chat_id=query.from_user.id,
                photo=WELCOME_IMAGE,
                caption=(
                    f"*👋 Welcome to Synax Osnit*\n\npowerful all-in-one bot jo daily useful tools provide karta hai — fast, simple aur user-friendly.\n🔹 Mobile Number Lookup\n🔹 Vehicle Registration Search\n🔹 AI Face Swap\n🔹 Pincode Finder\n🔹 IP Address Lookup\n🔹 Number to Name\n🔹 Instagram Username Info\n🔹 Instagram Reel Downloader\n🔹 Spotify Music Downloader\n🔹 Free Fire Player Info\n🔹 Text to Voice Converter\n🔹 YouTube Video Downloader\n🔹 GST Number Lookup\n🔹 Stylish Text Generator\n\n⚡ Fast • Secure • Easy to Use\n📌 Sab features ek hi bot me\n— Made by @synaxnetwork —\n\n"
                    f"👤 *User:* {query.from_user.first_name}\n"
                    f"💰 *Credits:* {user.get('balance', 0)}\n"
                    f"👑 *Premium:* {premium_status}\n\n"
                    f"Choose an option below to get started:"
                ),
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

# ==========================================

# ================= REFERRAL SYSTEM =================
def process_referral(user_id: str, referrer_id: str) -> bool:
    """Process referral and give bonus"""
    try:
        users = load_users()
        bonus_credits = 3  # Referral bonus
        
        if user_id in users and referrer_id in users:
            if not users[user_id].get("referred_by"):
                users[user_id]["referred_by"] = referrer_id
                users[referrer_id]["referrals"] = users[referrer_id].get("referrals", 0) + 1
                users[referrer_id]["referral_earnings"] = users[referrer_id].get("referral_earnings", 0) + bonus_credits
                users[referrer_id]["balance"] = users[referrer_id].get("balance", 0) + bonus_credits
                save_users(users)
                return True
        return False
    except Exception as e:
        logger.error(f"Error processing referral: {e}")
        return False

def get_referral_link(user_id: str) -> str:
    """Generate referral link"""
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"

# ==========================================

# ================= COUPON SYSTEM =================
def create_coupon(code: str, reward_type: str, reward_value: int, max_uses: int, expiry_days: int) -> bool:
    """Create a new coupon"""
    try:
        coupons = load_coupons()
        
        if "coupons" not in coupons:
            coupons["coupons"] = {}
        
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=expiry_days)).isoformat()
        
        coupons["coupons"][code] = {
            "reward_type": reward_type,  # "credits" or "premium"
            "reward_value": reward_value,
            "max_uses": max_uses,
            "used": 0,
            "expiry": expiry_date,
            "created_at": datetime.datetime.now().isoformat(),
            "used_by": []
        }
        
        return save_coupons(coupons)
    except Exception as e:
        logger.error(f"Error creating coupon: {e}")
        return False

def validate_coupon(code: str) -> Optional[dict]:
    """Validate coupon and return details if valid"""
    try:
        coupons = load_coupons()
        
        if "coupons" not in coupons or code not in coupons["coupons"]:
            return None
        
        coupon = coupons["coupons"][code]
        
        # Check expiry
        try:
            expiry = datetime.datetime.fromisoformat(coupon["expiry"])
            if expiry < datetime.datetime.now():
                return None
        except:
            return None
        
        # Check usage limit
        if coupon["used"] >= coupon["max_uses"]:
            return None
        
        return coupon
    except Exception as e:
        logger.error(f"Error validating coupon: {e}")
        return None

def use_coupon(code: str, user_id: str) -> bool:
    """Mark coupon as used and apply reward"""
    try:
        coupons = load_coupons()
        
        if "coupons" not in coupons or code not in coupons["coupons"]:
            return False
        
        coupon = coupons["coupons"][code]
        
        # Check if already used by this user
        if user_id in coupon.get("used_by", []):
            return False
        
        # Apply reward
        if coupon["reward_type"] == "credits":
            add_credits(user_id, coupon["reward_value"])
        elif coupon["reward_type"] == "premium":
            add_premium(user_id, coupon["reward_value"])
        
        # Mark as used
        coupon["used"] += 1
        coupon["used_by"].append(user_id)
        
        # Update coupon stats
        update_coupon_stats()
        
        return save_coupons(coupons)
    except Exception as e:
        logger.error(f"Error using coupon: {e}")
        return False

def generate_coupon_code(length=8):
    """Generate a random coupon code"""
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_coupon_stats() -> dict:
    """Get coupon statistics"""
    try:
        coupons = load_coupons()
        stats = {
            "total": 0,
            "active": 0,
            "expired": 0,
            "used": 0,
            "unused": 0
        }
        
        current_time = datetime.datetime.now()
        
        for code, coupon in coupons.get("coupons", {}).items():
            stats["total"] += 1
            
            try:
                expiry = datetime.datetime.fromisoformat(coupon["expiry"])
                if expiry < current_time:
                    stats["expired"] += 1
                else:
                    stats["active"] += 1
            except:
                stats["expired"] += 1
            
            if coupon["used"] > 0:
                stats["used"] += 1
            else:
                stats["unused"] += 1
        
        return stats
    except Exception as e:
        logger.error(f"Error getting coupon stats: {e}")
        return {
            "total": 0,
            "active": 0,
            "expired": 0,
            "used": 0,
            "unused": 0
        }

# ==========================================

# ================= PAYMENT SYSTEM =================
def create_payment_request(user_id: str, plan_type: str, plan_details: dict) -> str:
    """Create payment request"""
    try:
        payments = load_payments()
        
        if "payments" not in payments:
            payments["payments"] = {}
        
        payment_id = f"pay_{user_id}_{int(datetime.datetime.now().timestamp())}"
        
        payments["payments"][payment_id] = {
            "user_id": user_id,
            "plan_type": plan_type,
            "plan_details": plan_details,
            "status": "pending",
            "created_at": datetime.datetime.now().isoformat()
        }
        
        save_payments(payments)
        return payment_id
    except Exception as e:
        logger.error(f"Error creating payment request: {e}")
        return ""

def get_payment(payment_id: str) -> Optional[dict]:
    """Get payment details"""
    try:
        payments = load_payments()
        return payments.get("payments", {}).get(payment_id)
    except Exception as e:
        logger.error(f"Error getting payment: {e}")
        return None

def update_payment(payment_id: str, status: str, **kwargs) -> bool:
    """Update payment status"""
    try:
        payments = load_payments()
        
        if "payments" in payments and payment_id in payments["payments"]:
            payments["payments"][payment_id]["status"] = status
            payments["payments"][payment_id].update(kwargs)
            return save_payments(payments)
        
        return False
    except Exception as e:
        logger.error(f"Error updating payment: {e}")
        return False

# ==========================================

# ================= INSTAGRAM HELPER FUNCTIONS =================
def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def format_instagram_data(data: dict) -> str:
    """Format Instagram data for display"""
    if not data:
        return "❌ Failed to fetch data. Please try again."
    
    # Extract data with defaults and escape HTML
    user_id = escape_html(data.get("id", "N/A"))
    username = escape_html(data.get("username", "N/A"))
    name = escape_html(data.get("name", "N/A"))
    bio = escape_html(data.get("bio", "N/A"))
    verified = "✅ Verified" if data.get("verified", False) else "❌ Not Verified"
    private = "🔒 Private" if data.get("private", False) else "🌐 Public"
    profile_pic = data.get("pic", "")
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    posts = data.get("posts", 0)
    recent_posts = data.get("recent", [])
    
    # Format message
    msg = f"""
📷 <b>INSTAGRAM PROFILE INFO</b>
━━━━━━━━━━━━━━━━━━━━

👤 <b>BASIC INFO</b>
🆔 User ID : <code>{user_id}</code>
🏷 Username : @{username}
👤 Name : {name}
📝 Bio : {bio}
{verified}
{private}

📊 <b>STATISTICS</b>
👥 Followers : {followers:,}
👤 Following : {following:,}
📸 Posts : {posts:,}

"""
    
    # Add recent posts if available
    if recent_posts and len(recent_posts) > 0:
        msg += "<b>RECENT POSTS</b>\n"
        for i, post in enumerate(recent_posts[:3]):  # Show only first 3 posts
            post_id = escape_html(post.get("id", "N/A"))
            post_code = escape_html(post.get("code", "N/A"))
            caption = escape_html(post.get("cap", "No caption"))
            
            # Truncate caption if too long
            if caption and len(caption) > 50:
                caption = caption[:50] + "..."
            
            msg += f"\n📸 Post {i+1}: <code>{post_code}</code>\n"
            msg += f"📝 Caption: {caption}\n"
    
    msg += "\n━━━━━━━━━━━━━━━━━━"
    msg += "\n⚡ <i>Powered by @synaxnetwork</i>"
    
    return msg

def format_instagram_post(post_data: dict, index: int) -> str:
    """Format individual Instagram post data"""
    post_id = escape_html(post_data.get("id", "N/A"))
    post_code = escape_html(post_data.get("code", "N/A"))
    post_img = post_data.get("img", "")
    caption = escape_html(post_data.get("cap", "No caption"))
    
    # Extract hashtags from caption
    hashtags = []
    if caption:
        words = caption.split()
        hashtags = [word for word in words if word.startswith('#')]
    
    # Format message
    msg = f"""
📸 <b>POST {index}</b>
━━━━━━━━━━━━━━━━━━━━

🆔 Post ID : <code>{post_id}</code>
🔗 Code : <code>{post_code}</code>

📝 <b>CAPTION</b>
{caption if caption else "No caption"}

"""
    
    # Add hashtags if any
    if hashtags:
        msg += "<b>HASHTAGS</b>\n"
        for tag in hashtags[:10]:  # Limit to first 10 hashtags
            msg += f"{tag} "
        msg += "\n"
    
    msg += "━━━━━━━━━━━━━━━━━━"
    
    return msg

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    if not text:
        return []
    
    words = text.split()
    hashtags = [word for word in words if word.startswith('#')]
    return hashtags

# ==========================================

# ================= FREE FIRE HELPER FUNCTIONS =================
def format_freefire_data(data: dict) -> str:
    """Format Free Fire data for display"""
    if not data:
        return "❌ Failed to fetch data. Please try again."
    
    # Extract basic info
    basic_info = data.get("basicinfo", {})
    account_id = basic_info.get("accountid", "N/A")
    nickname = basic_info.get("nickname", "N/A")
    region = basic_info.get("region", "N/A")
    level = basic_info.get("level", "N/A")
    exp = basic_info.get("exp", "N/A")
    rank = basic_info.get("rank", "N/A")
    ranking_points = basic_info.get("rankingpoints", "N/A")
    liked = basic_info.get("liked", "N/A")
    
    # Extract clan info
    clan_info = data.get("clanbasicinfo", {})
    clan_name = clan_info.get("clanname", "N/A")
    clan_level = clan_info.get("clanlevel", "N/A")
    member_num = clan_info.get("membernum", "N/A")
    
    # Extract pet info
    pet_info = data.get("petinfo", {})
    pet_name = pet_info.get("name", "N/A")
    pet_level = pet_info.get("level", "N/A")
    
    # Extract social info
    social_info = data.get("socialinfo", {})
    gender = social_info.get("gender", "N/A")
    language = social_info.get("language", "N/A")
    
    # Format message
    msg = (
        f"🔥 *Free Fire Player Info*\n\n"
        f"👤 *Basic Info*\n"
        f"🆔 Account ID: `{account_id}`\n"
        f"🏷 Nickname: {nickname}\n"
        f"🌍 Region: {region}\n"
        f"⭐ Level: {level}\n"
        f"💎 EXP: {exp}\n"
        f"🏆 Rank: {rank}\n"
        f"📊 Ranking Points: {ranking_points}\n"
        f"❤️ Likes: {liked}\n\n"
        f"🏰 *Clan Info*\n"
        f"🏷 Clan Name: {clan_name}\n"
        f"⭐ Clan Level: {clan_level}\n"
        f"👥 Members: {member_num}\n\n"
        f"🐾 *Pet Info*\n"
        f"🏷 Pet Name: {pet_name}\n"
        f"⭐ Pet Level: {pet_level}\n\n"
        f"🌐 *Social Info*\n"
        f"👤 Gender: {gender}\n"
        f"🗣️ Language: {language}\n\n"
    )
    
    return msg

# ==========================================

# ================= YOUTUBE HELPER FUNCTIONS =================
def format_youtube_data(data: dict) -> str:
    """Format YouTube data for display"""
    if not data:
        return "❌ Failed to fetch data. Please try again."
    
    # Extract data with defaults
    title = data.get("title", "N/A")
    channel = data.get("channel", "N/A")
    duration = data.get("duration", "N/A")
    views = data.get("views", "N/A")
    quality = data.get("quality", "N/A")
    description = data.get("desc", "N/A")
    
    # Truncate description if too long
    if description and len(description) > 200:
        description = description[:200] + "..."
    
    # Format message
    msg = (
        f"📺 *YouTube Video Info*\n\n"
        f"🎬 *Title:* {title}\n"
        f"📺 *Channel:* {channel}\n"
        f"⏱️ *Duration:* {duration}\n"
        f"👁️ *Views:* {views}\n"
        f"📊 *Quality:* {quality}\n\n"
        f"📝 *Description:* {description}\n\n"
    )
    
    return msg

def get_best_quality_video(formats: List[dict]) -> dict:
    """Find the best quality video format from a list of formats"""
    if not formats:
        return None
    
    # Filter for video-only formats (no audio)
    video_formats = [f for f in formats if f.get("isVideo", False) and not f.get("isAudio", False)]
    
    if not video_formats:
        return None
    
    # Sort by quality (higher is better)
    # We'll use a simple heuristic based on format tags
    # Higher itag numbers generally mean higher quality
    video_formats.sort(key=lambda x: x.get("itag", 0), reverse=True)
    
    # Return the highest quality format
    return video_formats[0]

def get_best_quality_audio(formats: List[dict]) -> dict:
    """Find the best quality audio format from a list of formats"""
    if not formats:
        return None
    
    # Filter for audio-only formats
    audio_formats = [f for f in formats if f.get("isAudio", False) and not f.get("isVideo", False)]
    
    if not audio_formats:
        return None
    
    # Sort by quality (higher is better)
    # We'll use a simple heuristic based on format tags
    # Higher itag numbers generally mean higher quality
    audio_formats.sort(key=lambda x: x.get("itag", 0), reverse=True)
    
    # Return the highest quality format
    return audio_formats[0]

# ==========================================

# ================= GST HELPER FUNCTIONS =================
def format_gst_data(data: dict) -> str:
    """Format GST data for display"""
    if not data:
        return "❌ Failed to fetch GST data. Please try again."
    
    # Extract data with defaults
    gstin = data.get("Gstin", "N/A")
    trade_name = data.get("TradeName", "N/A")
    legal_name = data.get("LegalName", "N/A")
    addr_bnm = data.get("AddrBnm", "N/A")
    addr_bno = data.get("AddrBno", "N/A")
    addr_flno = data.get("AddrFlno", "N/A")
    addr_st = data.get("AddrSt", "N/A")
    addr_loc = data.get("AddrLoc", "N/A")
    state_code = data.get("StateCode", "N/A")
    addr_pncd = data.get("AddrPncd", "N/A")
    txp_type = data.get("TxpType", "N/A")
    status = data.get("Status", "N/A")
    blk_status = data.get("BlkStatus", "N/A")
    dt_reg = data.get("DtReg", "N/A")
    dt_dreg = data.get("DtDReg", "N/A")
    join = data.get("join", "N/A")
    
    # Format message
    msg = (
        f"🧾 *GST Number Information*\n\n"
        f"📋 *GST Details*\n"
        f"🆔 GSTIN: `{gstin}`\n"
        f"🏢 Trade Name: {trade_name}\n"
        f"👤 Legal Name: {legal_name}\n"
        f"📊 Taxpayer Type: {txp_type}\n"
        f"✅ Status: {status}\n"
        f"🚫 Block Status: {blk_status}\n\n"
        f"📅 *Registration Details*\n"
        f"🗓️ Registration Date: {dt_reg}\n"
        f"🗓️ Cancellation Date: {dt_dreg}\n\n"
        f"📍 *Address Details*\n"
        f"🏢 Building Name: {addr_bnm}\n"
        f"🏠 Building Number: {addr_bno}\n"
        f"🏢 Floor Number: {addr_flno}\n"
        f"🛣️ Street: {addr_st}\n"
        f"🏘️ Location: {addr_loc}\n"
        f"🗺️ State Code: {state_code}\n"
        f"📮 Pincode: {addr_pncd}\n\n"
    )
    
    # Add Made by @SynaxNetwork instead of join info
    msg += f"ℹ️ *Made by @SynaxNetwork*\n\n"
    
    return msg

# ==========================================

# ================= STYLISH TEXT HELPER FUNCTIONS =================
def generate_stylish_text(text: str, style_index: int = None) -> str:
    """Generate stylish text with a specific style or all styles"""
    # Convert to stylish font
    stylish_text = convert_to_stylish(text)
    
    if style_index is not None:
        # Return text with specific style
        if 0 <= style_index < len(STYLES):
            prefix, suffix = STYLES[style_index]
            return f"{prefix}{stylish_text}{suffix}"
        else:
            return stylish_text
    else:
        # Return text with all styles
        result = ""
        for i, (prefix, suffix) in enumerate(STYLES):
            result += f"{prefix}{stylish_text}{suffix}\n\n"
        return result

# ==========================================

# ================= COMMAND HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = str(update.effective_user.id)
    
    # Check if user is banned
    if is_user_banned(user_id):
        ban_info = get_ban_info(user_id)
        await update.message.reply_photo(
            photo=INFO_IMAGE,
            caption=f"❌ *You are banned from using this bot*\n\nReason: {ban_info.get('reason', 'No reason provided')}\nBanned on: {ban_info.get('banned_at', 'N/A')}",
            parse_mode="Markdown"
        )
        return
    
    # Check maintenance mode
    if is_maintenance_mode() and update.effective_user.id != ADMIN_ID:
        await update.message.reply_photo(
            photo=MAINTENANCE_IMAGE,
            caption=get_maintenance_message(),
            parse_mode="Markdown"
        )
        return
    
    args = context.args
    
    # Process referral if present
    if args and args[0].isdigit():
        referrer_id = args[0]
        if referrer_id != user_id:
            if process_referral(user_id, referrer_id):
                await update.message.reply_text("🎉 Referral bonus added to your account!")
    
    # Initialize user if not exists
    get_user(user_id)
    
    # Clear any active service states
    clear_service_states(context)
    
    # Check channel membership with improved error handling
    try:
        is_member = await check_channel_membership(update.effective_user.id, context)
        if not is_member:
            await send_force_join_message(update, context)
            return
    except Exception as e:
        logger.error(f"Error checking channel membership in start: {e}")
        # If there's an error checking membership, try to show the main menu
        # This prevents users from getting stuck if there's a temporary API issue
        await show_main_menu(update, context)
        return
    
    # Show main menu
    await show_main_menu(update, context)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # Clear any previous admin action states
    if "admin_action" in context.user_data:
        del context.user_data["admin_action"]
    if "ban_user_id" in context.user_data:
        del context.user_data["ban_user_id"]
    if "ban_reason" in context.user_data:
        del context.user_data["ban_reason"]
    if "unban_user_id" in context.user_data:
        del context.user_data["unban_user_id"]
    
    settings = load_settings()
    maintenance_status = "🔴 ON" if settings.get("maintenance_mode", False) else "🟢 OFF"
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("➕ Add Credits", callback_data="admin_add_credits")],
        [InlineKeyboardButton("➖ Remove Credits", callback_data="admin_remove_credits")],
        [InlineKeyboardButton("👑 Add Premium", callback_data="admin_add_premium")],
        [InlineKeyboardButton("❌ Remove Premium", callback_data="admin_remove_premium")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🎫 Create Coupon", callback_data="admin_create_coupon")],
        [InlineKeyboardButton("🎟️ Generate Coupon", callback_data="admin_generate_coupon")],
        [InlineKeyboardButton("📋 Coupon Stats", callback_data="admin_coupon_stats")],
        [InlineKeyboardButton("💰 Credit Costs", callback_data="admin_credit_costs")],
        [InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban_user")],
        [InlineKeyboardButton("✅ Unban User", callback_data="admin_unban_user")],
        [InlineKeyboardButton(f"🔧 Maintenance: {maintenance_status}", callback_data="admin_maintenance")],
        [InlineKeyboardButton("📋 Banned Users", callback_data="admin_banned_users")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "*🛠️ Admin Panel*\n\nSelect an action:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def addcredit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addcredit command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        amount = int(context.args[1])
        
        if add_credits(user_id, amount):
            await update.message.reply_text(f"✅ Added {amount} credits to user {user_id}")
        else:
            await update.message.reply_text("❌ Failed to add credits")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /addcredit USERID AMOUNT")

async def removecredit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removecredit command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        amount = int(context.args[1])
        
        if remove_credits(user_id, amount):
            await update.message.reply_text(f"✅ Removed {amount} credits from user {user_id}")
        else:
            await update.message.reply_text("❌ Failed to remove credits")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /removecredit USERID AMOUNT")

async def addpremium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addpremium command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        days = int(context.args[1])
        
        if add_premium(user_id, days):
            await update.message.reply_text(f"✅ Added {days} days premium to user {user_id}")
        else:
            await update.message.reply_text("❌ Failed to add premium")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /addpremium USERID DAYS")

async def removepremium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removepremium command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        
        if remove_premium(user_id):
            await update.message.reply_text(f"✅ Removed premium from user {user_id}")
        else:
            await update.message.reply_text("❌ Failed to remove premium")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /removepremium USERID")

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        if ban_user(user_id, reason):
            await update.message.reply_text(f"✅ User {user_id} has been banned\nReason: {reason}")
            # Try to notify the banned user
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"❌ You have been banned from using this bot\nReason: {reason}"
                )
            except:
                pass
        else:
            await update.message.reply_text("❌ Failed to ban user")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /ban USERID [reason]")

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unban command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        user_id = context.args[0]
        
        if unban_user(user_id):
            await update.message.reply_text(f"✅ User {user_id} has been unbanned")
            # Try to notify the unbanned user
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="✅ You have been unbanned and can now use the bot again"
                )
            except:
                pass
        else:
            await update.message.reply_text("❌ Failed to unban user or user was not banned")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /unban USERID")

async def maintenance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /maintenance command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    if len(context.args) == 0:
        # Show current status
        status = "ON" if is_maintenance_mode() else "OFF"
        await update.message.reply_text(f"🔧 Maintenance mode is currently: {status}")
        return
    
    action = context.args[0].lower()
    message = " ".join(context.args[1:]) if len(context.args) > 1 else None
    
    if action == "on":
        if set_maintenance_mode(True, message):
            await update.message.reply_text("✅ Maintenance mode has been enabled")
        else:
            await update.message.reply_text("❌ Failed to enable maintenance mode")
    elif action == "off":
        if set_maintenance_mode(False):
            await update.message.reply_text("✅ Maintenance mode has been disabled")
        else:
            await update.message.reply_text("❌ Failed to disable maintenance mode")
    else:
        await update.message.reply_text("Usage: /maintenance on [message] OR /maintenance off")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    # Get comprehensive statistics
    stats_text = await get_comprehensive_stats()
    
    # Split message if too long
    if len(stats_text) > 4000:
        parts = [stats_text[i:i+4000] for i in range(0, len(stats_text), 4000)]
        for part in parts:
            await update.message.reply_text(part, parse_mode="Markdown")
    else:
        await update.message.reply_text(stats_text, parse_mode="Markdown")

async def get_comprehensive_stats() -> str:
    """Get comprehensive statistics"""
    try:
        users = load_users()
        stats = load_stats()
        payments = load_payments()
        coupons = load_coupons()
        banned_users = load_banned_users()
        
        # Basic user stats
        total_users = len(users)
        premium_users = sum(1 for u in users.values() if is_premium_user(u))
        total_credits = sum(u.get("balance", 0) for u in users.values())
        total_banned = len(banned_users)
        
        # Active users (joined in last 7 days)
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        active_users = sum(
            1 for u in users.values() 
            if 'joined_at' in u and datetime.datetime.fromisoformat(u['joined_at']) > seven_days_ago
        )
        
        # Today's active users
        today = datetime.datetime.now().date()
        today_active = sum(
            1 for u in users.values() 
            if 'joined_at' in u and datetime.datetime.fromisoformat(u['joined_at']).date() == today
        )
        
        # Payment stats
        total_payments = len(payments.get("payments", {}))
        approved_payments = sum(1 for p in payments.get("payments", {}).values() if p.get("status") == "approved")
        pending_payments = sum(1 for p in payments.get("payments", {}).values() if p.get("status") == "pending")
        
        # Revenue calculation
        total_revenue = stats.get("total_revenue", 0)
        credits_spent = stats.get("credits_spent", 0)
        
        # Today's stats
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_searches = 0
        if today_str in stats.get("daily_searches", {}):
            today_searches = sum(stats["daily_searches"][today_str].values())
        
        # This month's stats
        this_month = datetime.datetime.now().strftime("%Y-%m")
        month_searches = 0
        if this_month in stats.get("monthly_searches", {}):
            month_searches = sum(stats["monthly_searches"][this_month].values())
        
        # Top features
        total_searches = stats.get("total_searches", {})
        top_features = sorted(total_searches.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Format the statistics
        stats_text = (
            f"*📊 COMPREHENSIVE BOT STATISTICS*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"*👥 USER STATISTICS*\n"
            f"👤 Total Users: {total_users}\n"
            f"👑 Premium Users: {premium_users}\n"
            f"📊 Active Users (7 days): {active_users}\n"
            f"📈 Today's New Users: {today_active}\n"
            f"💳 Total Credits: {total_credits}\n"
            f"🚫 Banned Users: {total_banned}\n\n"
            f"*💰 REVENUE STATISTICS*\n"
            f"💵 Total Revenue: ₹{total_revenue:.2f}\n"
            f"🔥 Credits Spent: {credits_spent}\n"
            f"🎫 Coupon Redemptions: {stats.get('coupon_redemptions', 0)}\n"
            f"👑 Premium Purchases: {stats.get('premium_purchases', 0)}\n\n"
            f"*📈 USAGE STATISTICS*\n"
            f"🔍 Total Searches: {sum(total_searches.values())}\n"
            f"📅 Today's Searches: {today_searches}\n"
            f"📆 This Month's Searches: {month_searches}\n\n"
            f"*💳 PAYMENT STATISTICS*\n"
            f"📊 Total Payments: {total_payments}\n"
            f"✅ Approved: {approved_payments}\n"
            f"⏳ Pending: {pending_payments}\n\n"
        )
        
        # Add top features
        if top_features:
            stats_text += "*🔥 TOP FEATURES*\n"
            feature_names = {
                "number_search": "📱 Number Search",
                "vehicle_search": "🚗 Vehicle Search",
                "face_swap": "🎭 Face Swap",
                "pincode_search": "📍 Pincode Search",
                "ip_info_search": "🌐 IP Info",
                "num_name_search": "📞 Number to Name",
                "spotify_search": "🎵 Spotify (Name)",
                "spotify_url_search": "🎵 Spotify (URL)",
                "instagram_search": "📷 Instagram Info",
                "instagram_reel_download": "📹 Instagram Reel",
                "freefire_search": "🔥 Free Fire",
                "text_to_voice": "🔊 Text to Voice",
                "youtube_download": "📺 YouTube",
                "gst_search": "🧾 GST Lookup",
                "stylish_text": "✨ Stylish Text"
            }
            
            for i, (feature, count) in enumerate(top_features, 1):
                name = feature_names.get(feature, feature.replace('_', ' ').title())
                stats_text += f"{i}. {name}: {count}\n"
            
            stats_text += "\n"
        
        # Add coupon stats
        coupon_stats = get_coupon_stats()
        stats_text += (
            f"*🎫 COUPON STATISTICS*\n"
            f"🔢 Total Coupons: {coupon_stats['total']}\n"
            f"✅ Active: {coupon_stats['active']}\n"
            f"❌ Expired: {coupon_stats['expired']}\n"
            f"📈 Used: {coupon_stats['used']}\n"
            f"📉 Unused: {coupon_stats['unused']}\n\n"
        )
        
        stats_text += f"━━━━━━━━━━━━━━━━━━━━\n"
        stats_text += f"🕐 *Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        stats_text += f"⚡ *Powered by @synaxnetwork*"
        
        return stats_text
    except Exception as e:
        logger.error(f"Error getting comprehensive stats: {e}")
        return f"❌ Error loading statistics: {str(e)}"

# ==========================================

# ================= CALLBACK HANDLERS =================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    # Check if user is banned
    if is_user_banned(user_id):
        ban_info = get_ban_info(user_id)
        await query.message.reply_photo(
            photo=INFO_IMAGE,
            caption=f"❌ *You are banned from using this bot*\n\nReason: {ban_info.get('reason', 'No reason provided')}",
            parse_mode="Markdown"
        )
        return
    
    # Check maintenance mode
    if is_maintenance_mode() and query.from_user.id != ADMIN_ID:
        await query.message.reply_photo(
            photo=MAINTENANCE_IMAGE,
            caption=get_maintenance_message(),
            parse_mode="Markdown"
        )
        return
    
    # Handle channel join check callbacks
    if data in ["check_joined", "refresh_join_status"]:
        # Check which channels the user hasn't joined
        required_channels = get_required_channels()
        not_joined = []
        
        for channel in required_channels:
            try:
                member = await context.bot.get_chat_member(channel["id"], query.from_user.id)
                if member.status not in ["member", "administrator", "creator"]:
                    not_joined.append(channel)
            except TelegramError as e:
                logger.error(f"Error checking channel membership: {e}")
                not_joined.append(channel)
        
        # If user has joined all channels, show main menu
        if not not_joined:
            await query.answer("✅ Thank you for joining all channels!", show_alert=True)
            await show_main_menu(update, context)
            return
        else:
            await query.answer(f"❌ You haven't joined {len(not_joined)} channel(s) yet!", show_alert=True)
            # Update the join message
            await send_force_join_message(update, context)
            return
    
    # Check channel membership for most actions (with improved error handling)
    try:
        is_member = await check_channel_membership(query.from_user.id, context)
        if not is_member and data not in ["admin_", "maintenance_", "check_joined", "refresh_join_status"]:
            await send_force_join_message(update, context)
            return
    except Exception as e:
        logger.error(f"Error checking channel membership in callback: {e}")
        # If there's an error checking membership, allow the action to proceed
        # This prevents users from getting stuck if there's a temporary API issue
    
    if data == "copy_referral":
        # Copy referral link to clipboard
        user_id = str(query.from_user.id)
        referral_link = get_referral_link(user_id)
        
        await query.answer("📋 Referral link copied!", show_alert=True)
        
        # Send the referral link as a message for easy copying
        await query.message.reply_text(
            f"📋 *Your Referral Link*\n\n`{referral_link}`\n\nShare this link with your friends to earn 3 credits for each referral!",
            parse_mode="Markdown"
        )
    
    elif data.startswith("copy_coupon_"):
        # Copy coupon code to clipboard
        coupon_code = data.split("_", 2)[2]
        
        await query.answer("📋 Coupon code copied!", show_alert=True)
        
        # Send the coupon code as a message for easy copying
        await query.message.reply_text(
            f"📋 *Coupon Code*\n\n`{coupon_code}`\n\nShare this code with users to give them rewards!",
            parse_mode="Markdown"
        )
    
    elif data == "buy_credits":
        await show_credit_plans(query, context)
    
    elif data == "buy_premium":
        await show_premium_plans(query, context)
    
    elif data == "my_account":
        await show_my_account(query, context)
    
    elif data == "referral":
        await show_referral_info(query, context)
    
    elif data == "coupon":
        # Clear all service states before starting coupon redemption
        clear_service_states(context)
        await query.message.reply_photo(
            photo=INFO_IMAGE,
            caption="🎫 *Enter Coupon Code*\n\nPlease send the coupon code you want to redeem:",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_coupon"] = True
    
    elif data == "search_number":
        # Clear all service states before starting number search
        clear_service_states(context)
        context.user_data["awaiting_number"] = True
        await query.message.reply_photo(
            photo=SEARCH_IMAGE,
            caption="📱 *Enter Mobile Number*\n\nPlease send a 10-digit mobile number to search:",
            parse_mode="Markdown"
        )
    
    elif data == "vehicle_search":
        # Clear all service states before starting vehicle search
        clear_service_states(context)
        context.user_data["awaiting_vehicle"] = True
        await query.message.reply_photo(
            photo=VEHICLE_SEARCH_IMAGE,
            caption="🚗 *Enter Vehicle Number*\n\nPlease send a vehicle registration number to search (e.g., MH12AB1234):",
            parse_mode="Markdown"
        )
    
    elif data == "face_swap":
        # Clear all service states before starting face swap
        clear_service_states(context)
        # Start face swap conversation
        context.user_data["face_swap_state"] = FACE_SWAP_SOURCE
        await query.message.reply_photo(
            photo=FACE_SWAP_IMAGE,
            caption="🎭 *Face Swap*\n\n📸 Send the *SOURCE* image first (the face you want to use)\n\nThen send the *TARGET* image (where the face will be placed)",
            parse_mode="Markdown"
        )
    
    elif data == "pincode_search":
        # Clear all service states before starting pincode search
        clear_service_states(context)
        context.user_data["awaiting_pincode"] = True
        await query.message.reply_photo(
            photo=PINCODE_SEARCH_IMAGE,
            caption="📍 *Enter Pincode*\n\nPlease send a 6-digit Indian pincode to search (e.g., 110001):",
            parse_mode="Markdown"
        )
    
    elif data == "ip_info_search":
        # Clear all service states before starting IP info search
        clear_service_states(context)
        context.user_data["awaiting_ip"] = True
        await query.message.reply_photo(
            photo=IP_INFO_SEARCH_IMAGE,
            caption="🌐 *Enter IP Address*\n\nPlease send an IP address to get information (e.g., 8.8.8.8):",
            parse_mode="Markdown"
        )
    
    elif data == "num_name_search":
        # Clear all service states before starting number to name search
        clear_service_states(context)
        context.user_data["awaiting_num_name"] = True
        await query.message.reply_photo(
            photo=NUM_NAME_SEARCH_IMAGE,
            caption="📞 *Number to Name Search*\n\nPlease send a mobile number with country code (e.g., 919065146522):",
            parse_mode="Markdown"
        )
    
    elif data == "instagram_search":
        # Clear all service states before starting Instagram search
        clear_service_states(context)
        context.user_data["awaiting_instagram"] = True
        await query.message.reply_photo(
            photo=INSTAGRAM_SEARCH_IMAGE,
            caption="📷 *Instagram Username Info*\n\nPlease send an Instagram username (without @):\n\nExample: `maybe__abhii`",
            parse_mode="Markdown"
        )
    
    elif data == "instagram_reel_download":
        # Clear all service states before starting Instagram Reel download
        clear_service_states(context)
        context.user_data["awaiting_instagram_reel"] = True
        await query.message.reply_photo(
            photo=INSTAGRAM_REEL_IMAGE,
            caption="📹 *Instagram Reel Downloader*\n\nPlease send an Instagram Reel URL to download:\n\nExample: `https://www.instagram.com/reel/...`",
            parse_mode="Markdown"
        )
    
    elif data == "spotify_menu":
        # Show Spotify menu options
        await show_spotify_menu(query, context)
    
    elif data == "spotify_search":
        # Clear all service states before starting Spotify search
        clear_service_states(context)
        context.user_data["awaiting_spotify"] = True
        await query.message.reply_photo(
            photo=SPOTIFY_SEARCH_IMAGE,
            caption="🎵 *Spotify Music Downloader (by Name)*\n\nPlease send a song name to search and download:\n\nExample: `Shape of You`",
            parse_mode="Markdown"
        )
    
    elif data == "spotify_url_search":
        # Clear all service states before starting Spotify URL search
        clear_service_states(context)
        context.user_data["awaiting_spotify_url"] = True
        await query.message.reply_photo(
            photo=SPOTIFY_SEARCH_IMAGE,
            caption="🎵 *Spotify Music Downloader (by URL)*\n\nPlease send a Spotify URL to download:\n\nExample: `https://open.spotify.com/track/...`",
            parse_mode="Markdown"
        )
    
    elif data == "freefire_search":
        # Clear all service states before starting Free Fire search
        clear_service_states(context)
        context.user_data["awaiting_freefire"] = True
        await query.message.reply_photo(
            photo=FREEFIRE_SEARCH_IMAGE,
            caption="🔥 *Free Fire Player Info*\n\nPlease send a Free Fire UID to get player information:\n\nExample: `6662300192`",
            parse_mode="Markdown"
        )
    
    elif data == "text_to_voice":
        # Clear all service states before starting text to voice
        clear_service_states(context)
        context.user_data["awaiting_text_to_voice"] = True
        await query.message.reply_photo(
            photo=TEXT_TO_VOICE_IMAGE,
            caption="🔊 *Text to Voice*\n\nPlease send the text you want to convert to voice:\n\nExample: `Hello, this is a test message`",
            parse_mode="Markdown"
        )
    
    elif data == "youtube_download":
        # Clear all service states before starting YouTube download
        clear_service_states(context)
        context.user_data["awaiting_youtube"] = True
        await query.message.reply_photo(
            photo=YOUTUBE_SEARCH_IMAGE,
            caption="📺 *YouTube Video Downloader*\n\nPlease send a YouTube video URL to download:\n\nExample: `https://www.youtube.com/watch?v=...`",
            parse_mode="Markdown"
        )
    
    elif data == "gst_search":
        # Clear all service states before starting GST search
        clear_service_states(context)
        context.user_data["awaiting_gst"] = True
        await query.message.reply_photo(
            photo=GST_SEARCH_IMAGE,
            caption="🧾 *GST Number Lookup*\n\nPlease send a GST number to search:\n\nExample: `19BOKPS7056D1ZI`",
            parse_mode="Markdown"
        )
    
    elif data == "stylish_text":
        # Clear all service states before starting stylish text generation
        clear_service_states(context)
        context.user_data["stylish_text_mode"] = STYLISH_TEXT_MODE
        await query.message.reply_photo(
            photo=STYLISH_TEXT_IMAGE,
            caption="✨ *Stylish Text Generator*\n\nPlease send the text you want to convert to stylish text:\n\nExample: `Your Name`\n\nYou'll receive each style in a separate message for easy copying!",
            parse_mode="Markdown"
        )
    
    elif data == "back_to_menu":
        # Return to main menu
        await show_main_menu(update, context)
    
    # Admin callbacks
    elif data.startswith("admin_"):
        await handle_admin_callbacks(query, context, data)
    
    # Maintenance callbacks
    elif data.startswith("maintenance_"):
        await handle_maintenance_callbacks(query, context, data)
    
    # Credit plan selection
    elif data.startswith("credit_plan_"):
        plan_id = data.split("_")[-1]
        await process_credit_plan(query, context, plan_id)
    
    # Premium plan selection
    elif data.startswith("premium_plan_"):
        plan_id = data.split("_")[-1]
        await process_premium_plan(query, context, plan_id)
    
    # Payment approval
    elif data.startswith("payment_approve_"):
        payment_id = data.split("_", 2)[-1]
        await approve_payment(query, context, payment_id)
    
    elif data.startswith("payment_reject_"):
        payment_id = data.split("_", 2)[-1]
        await reject_payment(query, context, payment_id)
    
    # Payment pending - when user clicks "I've Paid"
    elif data.startswith("payment_pending_"):
        payment_id = data.split("_", 2)[-1]
        await handle_payment_pending(query, context, payment_id)
    
    # Coupon generation callbacks
    elif data.startswith("coupon_type_"):
        coupon_type = data.split("_")[-1]
        context.user_data["coupon_gen"]["type"] = coupon_type
        context.user_data["coupon_gen"]["step"] = 2
        
        await query.message.reply_text(
            f"*🎟️ Advanced Coupon Generator*\n\n"
            f"Reward type: {coupon_type}\n\n"
            f"Now send the reward value (credits or days):",
            parse_mode="Markdown"
        )
    
    elif data == "coupon_gen_cancel":
        if "coupon_gen" in context.user_data:
            del context.user_data["coupon_gen"]
        
        await query.message.reply_text(
            "❌ Coupon generation cancelled.",
            parse_mode="Markdown"
        )
    
    # Credit cost callbacks
    elif data.startswith("credit_cost_"):
        feature = data.split("_", 2)[-1]
        await show_credit_cost_edit(query, context, feature)
    
    elif data.startswith("edit_credit_cost_"):
        feature = data.split("_", 3)[-1]
        context.user_data["editing_credit_cost"] = feature
        await query.message.reply_text(
            f"*💰 Edit Credit Cost*\n\n"
            f"Current cost for {feature.replace('_', ' ').title()}: {get_credit_cost(feature)} credits\n\n"
            f"Please send the new credit cost (number):",
            parse_mode="Markdown"
        )

async def show_spotify_menu(query, context):
    """Show Spotify menu with options"""
    keyboard = [
        [InlineKeyboardButton("🎵 Search by Name", callback_data="spotify_search")],
        [InlineKeyboardButton("🔗 Download by URL", callback_data="spotify_url_search")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=SPOTIFY_SEARCH_IMAGE,
                caption=(
                    "*🎵 Spotify Music Downloader*\n\n"
                    "Choose a download method:"
                ),
                parse_mode="Markdown"
            ),
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_photo(
            photo=SPOTIFY_SEARCH_IMAGE,
            caption=(
                "*🎵 Spotify Music Downloader*\n\n"
                "Choose a download method:"
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_maintenance_callbacks(query, context, data):
    """Handle maintenance mode callbacks"""
    if query.from_user.id != ADMIN_ID:
        await query.answer("Unauthorized!", show_alert=True)
        return
    
    if data == "maintenance_on":
        # Enable maintenance mode
        if set_maintenance_mode(True):
            await query.answer("✅ Maintenance mode enabled!", show_alert=True)
            await show_maintenance_options(query, context)
        else:
            await query.answer("❌ Failed to enable maintenance mode!", show_alert=True)
    
    elif data == "maintenance_off":
        # Disable maintenance mode
        if set_maintenance_mode(False):
            await query.answer("✅ Maintenance mode disabled!", show_alert=True)
            await show_maintenance_options(query, context)
        else:
            await query.answer("❌ Failed to disable maintenance mode!", show_alert=True)
    
    elif data == "maintenance_edit_message":
        # Start editing maintenance message
        context.user_data["editing_maintenance_message"] = True
        await query.message.reply_text(
            "📝 *Edit Maintenance Message*\n\n"
            "Please send the new maintenance message:",
            parse_mode="Markdown"
        )

async def handle_payment_pending(query, context, payment_id):
    """Handle when user clicks 'I've Paid' button"""
    user_id = str(query.from_user.id)
    payment = get_payment(payment_id)
    
    if not payment or payment["user_id"] != user_id:
        await query.answer("Invalid payment session!", show_alert=True)
        return
    
    # Set user state to expect screenshot
    context.user_data["pending_payment"] = payment_id
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data="buy_credits" if payment["plan_type"] == "credits" else "buy_premium")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            f"*💳 Payment Confirmation*\n\n"
            f"Thank you for your payment!\n\n"
            f"Please send a screenshot of your payment to complete the process.\n\n"
            f"Plan: {payment['plan_type']}\n"
            f"Details: {payment['plan_details']}\n\n"
            f"⏳ Waiting for your payment screenshot...",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            f"*💳 Payment Confirmation*\n\n"
            f"Thank you for your payment!\n\n"
            f"Please send a screenshot of your payment to complete the process.\n\n"
            f"Plan: {payment['plan_type']}\n"
            f"Details: {payment['plan_details']}\n\n"
            f"⏳ Waiting for your payment screenshot...",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_credit_plans(query, context):
    """Show credit purchase plans"""
    keyboard = [
        [InlineKeyboardButton("💎 10 Credits - ₹10", callback_data="credit_plan_10")],
        [InlineKeyboardButton("💎 50 Credits - ₹30", callback_data="credit_plan_50")],
        [InlineKeyboardButton("💎 100 Credits - ₹50", callback_data="credit_plan_100")],
        [InlineKeyboardButton("💎 300 Credits - ₹100", callback_data="credit_plan_300")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=PAYMENT_IMAGE,
                caption=(
                    "*💳 Buy Credits*\n\n"
                    "Select a credit package below:\n"
                    "💳 UPI ID: `" + UPI_ID + "`\n\n"
                    "After payment, click 'I've Paid' and send the screenshot."
                ),
                parse_mode="Markdown"
            ),
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_photo(
            photo=PAYMENT_IMAGE,
            caption=(
                "*💳 Buy Credits*\n\n"
                "Select a credit package below:\n"
                "💳 UPI ID: `" + UPI_ID + "`\n\n"
                "After payment, click 'I've Paid' and send the screenshot."
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_premium_plans(query, context):
    """Show premium purchase plans"""
    keyboard = [
        [InlineKeyboardButton("👑 1 Day - ₹30", callback_data="premium_plan_1")],
        [InlineKeyboardButton("👑 3 Days - ₹70", callback_data="premium_plan_3")],
        [InlineKeyboardButton("👑 1 Week - ₹120", callback_data="premium_plan_7")],
        [InlineKeyboardButton("👑 1 Month - ₹200", callback_data="premium_plan_30")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=PAYMENT_IMAGE,
                caption=(
                    "*👑 Buy Premium*\n\n"
                    "Select a premium plan below:\n"
                    "💳 UPI ID: `" + UPI_ID + "`\n\n"
                    "After payment, click 'I've Paid' and send the screenshot."
                ),
                parse_mode="Markdown"
            ),
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_photo(
            photo=PAYMENT_IMAGE,
            caption=(
                "*👑 Buy Premium*\n\n"
                "Select a premium plan below:\n"
                "💳 UPI ID: `" + UPI_ID + "`\n\n"
                "After payment, click 'I've Paid' and send the screenshot."
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_my_account(query, context):
    """Show user account information"""
    user_id = str(query.from_user.id)
    user = get_user(user_id)
    
    premium_status = "✅ Active" if is_premium_user(user_id) else "❌ Inactive"
    premium_expiry = "N/A"
    
    if user.get("premium_expiry"):
        try:
            expiry = datetime.datetime.fromisoformat(user["premium_expiry"])
            premium_expiry = expiry.strftime("%d-%m-%Y %H:%M")
        except:
            pass
    
    account_text = (
        f"*👤 My Account*\n\n"
        f"🆔 User ID: `{user_id}`\n"
        f"👤 Username: @{query.from_user.username or 'N/A'}\n"
        f"💰 Credits: {user.get('balance', 0)}\n"
        f"👑 Premium: {premium_status}\n"
        f"⏰ Premium Expiry: {premium_expiry}\n"
        f"🔗 Referrals: {user.get('referrals', 0)}\n"
        f"💸 Referral Earnings: {user.get('referral_earnings', 0)} credits"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=ACCOUNT_IMAGE,
                caption=account_text,
                parse_mode="Markdown"
            ),
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_photo(
            photo=ACCOUNT_IMAGE,
            caption=account_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_referral_info(query, context):
    """Show referral information"""
    user_id = str(query.from_user.id)
    referral_link = get_referral_link(user_id)
    user = get_user(user_id)
    
    referral_text = (
        f"*🔗 Referral System*\n\n"
        f"📱 Your Referral Link:\n`{referral_link}`\n\n"
        f"👥 Total Referrals: {user.get('referrals', 0)}\n"
        f"💰 Earned Credits: {user.get('referral_earnings', 0)}\n\n"
        f"🎁 *Reward*: 3 credits for each referral!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 Copy Link", callback_data="copy_referral")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=REFERRAL_IMAGE,
                caption=referral_text,
                parse_mode="Markdown"
            ),
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_photo(
            photo=REFERRAL_IMAGE,
            caption=referral_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def process_credit_plan(query, context, plan_id):
    """Process credit plan selection"""
    plans = {
        "10": {"credits": 10, "price": "₹10"},
        "50": {"credits": 50, "price": "₹30"},
        "100": {"credits": 100, "price": "₹50"},
        "300": {"credits": 300, "price": "₹100"}
    }
    
    if plan_id not in plans:
        await query.answer("Invalid plan!", show_alert=True)
        return
    
    plan = plans[plan_id]
    user_id = str(query.from_user.id)
    
    # Create payment request
    payment_id = create_payment_request(
        user_id,
        "credits",
        {"credits": plan["credits"], "price": plan["price"]}
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 I've Paid", callback_data=f"payment_pending_{payment_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="buy_credits")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            f"*💳 Payment Details*\n\n"
            f"Plan: {plan['credits']} Credits\n"
            f"Price: {plan['price']}\n"
            f"UPI ID: `{UPI_ID}`\n\n"
            f"1. Pay the amount above\n"
            f"2. Click 'I've Paid'\n"
            f"3. Send payment screenshot",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            f"*💳 Payment Details*\n\n"
            f"Plan: {plan['credits']} Credits\n"
            f"Price: {plan['price']}\n"
            f"UPI ID: `{UPI_ID}`\n\n"
            f"1. Pay the amount above\n"
            f"2. Click 'I've Paid'\n"
            f"3. Send payment screenshot",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def process_premium_plan(query, context, plan_id):
    """Process premium plan selection"""
    plans = {
        "1": {"days": 1, "price": "₹30"},
        "3": {"days": 3, "price": "₹70"},
        "7": {"days": 7, "price": "₹120"},
        "30": {"days": 30, "price": "₹200"}
    }
    
    if plan_id not in plans:
        await query.answer("Invalid plan!", show_alert=True)
        return
    
    plan = plans[plan_id]
    user_id = str(query.from_user.id)
    
    # Create payment request
    payment_id = create_payment_request(
        user_id,
        "premium",
        {"days": plan["days"], "price": plan["price"]}
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 I've Paid", callback_data=f"payment_pending_{payment_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="buy_premium")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            f"*👑 Payment Details*\n\n"
            f"Plan: {plan['days']} Days Premium\n"
            f"Price: {plan['price']}\n"
            f"UPI ID: `{UPI_ID}`\n\n"
            f"1. Pay the amount above\n"
            f"2. Click 'I've Paid'\n"
            f"3. Send payment screenshot",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            f"*👑 Payment Details*\n\n"
            f"Plan: {plan['days']} Days Premium\n"
            f"Price: {plan['price']}\n"
            f"UPI ID: `{UPI_ID}`\n\n"
            f"1. Pay the amount above\n"
            f"2. Click 'I've Paid'\n"
            f"3. Send payment screenshot",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_admin_callbacks(query, context, data):
    """Handle admin panel callbacks"""
    if query.from_user.id != ADMIN_ID:
        await query.answer("Unauthorized!", show_alert=True)
        return
    
    # Clear any previous admin action state
    if "admin_action" in context.user_data:
        del context.user_data["admin_action"]
    
    if data == "admin_stats":
        # Get comprehensive statistics
        stats_text = await get_comprehensive_stats()
        
        # Split message if too long
        if len(stats_text) > 4000:
            parts = [stats_text[i:i+4000] for i in range(0, len(stats_text), 4000)]
            for part in parts:
                await query.message.reply_text(part, parse_mode="Markdown")
        else:
            await query.message.reply_text(stats_text, parse_mode="Markdown")
    
    elif data == "admin_add_credits":
        context.user_data["admin_action"] = "add_credits"
        await query.message.reply_text(
            "➕ *Add Credits*\n\nUse: /addcredit USERID AMOUNT\n\nExample: /addcredit 123456789 50",
            parse_mode="Markdown"
        )
    
    elif data == "admin_remove_credits":
        context.user_data["admin_action"] = "remove_credits"
        await query.message.reply_text(
            "➖ *Remove Credits*\n\nUse: /removecredit USERID AMOUNT\n\nExample: /removecredit 123456789 50",
            parse_mode="Markdown"
        )
    
    elif data == "admin_add_premium":
        context.user_data["admin_action"] = "add_premium"
        await query.message.reply_text(
            "👑 *Add Premium*\n\nUse: /addpremium USERID DAYS\n\nExample: /addpremium 123456789 7",
            parse_mode="Markdown"
        )
    
    elif data == "admin_remove_premium":
        context.user_data["admin_action"] = "remove_premium"
        await query.message.reply_text(
            "❌ *Remove Premium*\n\nUse: /removepremium USERID\n\nExample: /removepremium 123456789",
            parse_mode="Markdown"
        )
    
    elif data == "admin_broadcast":
        context.user_data["admin_action"] = "broadcast"
        await query.message.reply_text(
            "📢 *Broadcast System*\n\nSend the message you want to broadcast.\n"
            "Supported formats:\n"
            "• Text only\n"
            "• Photo + Caption\n\n"
            "Type /cancel to cancel.",
            parse_mode="Markdown"
        )
        context.user_data["broadcast_mode"] = True
    
    elif data == "admin_create_coupon":
        context.user_data["admin_action"] = "create_coupon"
        await query.message.reply_text(
            "🎫 *Create Coupon*\n\nSend coupon details in format:\n"
            "`CODE|TYPE|VALUE|MAX_USES|EXPIRY_DAYS`\n\n"
            "TYPE: credits or premium\n"
            "VALUE: credit amount or premium days\n\n"
            "Example: `WELCOME50|credits|50|100|30`",
            parse_mode="Markdown"
        )
        context.user_data["coupon_creation"] = True
    
    elif data == "admin_generate_coupon":
        context.user_data["admin_action"] = "generate_coupon"
        await start_coupon_generation(query, context)
    
    elif data == "admin_coupon_stats":
        context.user_data["admin_action"] = "coupon_stats"
        await show_coupon_stats(query, context)
    
    elif data == "admin_credit_costs":
        context.user_data["admin_action"] = "credit_costs"
        await show_credit_costs(query, context)
    
    elif data == "admin_ban_user":
        # Clear any previous ban states
        if "ban_user_id" in context.user_data:
            del context.user_data["ban_user_id"]
        if "ban_reason" in context.user_data:
            del context.user_data["ban_reason"]
        
        context.user_data["admin_action"] = "ban_user"
        await query.message.reply_text(
            "🚫 *Ban User*\n\nSend the User ID to ban:\n\n"
            "Example: `123456789`\n\n"
            "Or use: /ban USERID [reason]",
            parse_mode="Markdown"
        )
        context.user_data["ban_user_id"] = True
    
    elif data == "admin_unban_user":
        # Clear any previous unban state
        if "unban_user_id" in context.user_data:
            del context.user_data["unban_user_id"]
        
        context.user_data["admin_action"] = "unban_user"
        await query.message.reply_text(
            "✅ *Unban User*\n\nSend the User ID to unban:\n\n"
            "Example: `123456789`\n\n"
            "Or use: /unban USERID",
            parse_mode="Markdown"
        )
        context.user_data["unban_user_id"] = True
    
    elif data == "admin_banned_users":
        await show_banned_users(query, context)
    
    elif data == "admin_maintenance":
        await show_maintenance_options(query, context)

async def show_banned_users(query, context):
    """Show list of banned users"""
    banned_users = load_banned_users()
    
    if not banned_users:
        await query.message.reply_text(
            "📋 *Banned Users*\n\nNo users are currently banned.",
            parse_mode="Markdown"
        )
        return
    
    banned_text = "*📋 Banned Users*\n\n"
    
    for user_id, ban_info in banned_users.items():
        banned_text += (
            f"🆔 *User ID:* `{user_id}`\n"
            f"📝 *Reason:* {ban_info.get('reason', 'No reason')}\n"
            f"📅 *Banned on:* {ban_info.get('banned_at', 'N/A')}\n\n"
        )
    
    # Split message if too long
    if len(banned_text) > 4000:
        parts = [banned_text[i:i+4000] for i in range(0, len(banned_text), 4000)]
        for part in parts:
            await query.message.reply_text(part, parse_mode="Markdown")
    else:
        await query.message.reply_text(banned_text, parse_mode="Markdown")

async def show_maintenance_options(query, context):
    """Show maintenance mode options"""
    settings = load_settings()
    is_enabled = settings.get("maintenance_mode", False)
    current_message = settings.get("maintenance_message", "🔧 Bot is under maintenance. Please try again later.")
    
    status_text = "🔴 *ENABLED*" if is_enabled else "🟢 *DISABLED*"
    
    keyboard = [
        [InlineKeyboardButton("🔧 Turn ON", callback_data="maintenance_on")],
        [InlineKeyboardButton("✅ Turn OFF", callback_data="maintenance_off")],
        [InlineKeyboardButton("📝 Edit Message", callback_data="maintenance_edit_message")],
        [InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_stats")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    maintenance_text = (
        f"*🔧 Maintenance Mode*\n\n"
        f"Status: {status_text}\n\n"
        f"Current Message:\n{current_message}\n\n"
        f"Choose an action:"
    )
    
    try:
        await query.edit_message_text(
            maintenance_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            maintenance_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_credit_costs(query, context):
    """Show credit costs configuration"""
    costs = load_credit_costs()
    
    # Format the costs into a nice message
    cost_text = (
        "*💰 Credit Costs Configuration*\n\n"
        f"📱 Number Search: {costs.get('number_search', 1)} credits\n"
        f"🚗 Vehicle Search: {costs.get('vehicle_search', 2)} credits\n"
        f"🎭 Face Swap: {costs.get('face_swap', 5)} credits\n"
        f"📍 Pincode Search: {costs.get('pincode_search', 1)} credits\n"
        f"🌐 IP Info Search: {costs.get('ip_info_search', 2)} credits\n"
        f"📞 Number to Name: {costs.get('num_name_search', 1)} credits\n"
        f"📷 Instagram Info: {costs.get('instagram_search', 2)} credits\n"
        f"📹 Instagram Reel Download: {costs.get('instagram_reel_download', 3)} credits\n"
        f"🎵 Spotify Music (Name): {costs.get('spotify_search', 2)} credits\n"
        f"🎵 Spotify Music (URL): {costs.get('spotify_url_search', 2)} credits\n"
        f"🔥 Free Fire Info: {costs.get('freefire_search', 2)} credits\n"
        f"🔊 Text to Voice: {costs.get('text_to_voice', 1)} credits\n"
        f"📺 YouTube Download: {costs.get('youtube_download', 3)} credits\n"
        f"🧾 GST Number Lookup: {costs.get('gst_search', 2)} credits\n"
        f"✨ Stylish Text Generator: {costs.get('stylish_text', 1)} credits\n\n"
        "Click on any feature below to change its credit cost:"
    )
    
    # Create buttons for each feature
    keyboard = [
        [InlineKeyboardButton("📱 Number Search", callback_data="credit_cost_number_search")],
        [InlineKeyboardButton("🚗 Vehicle Search", callback_data="credit_cost_vehicle_search")],
        [InlineKeyboardButton("🎭 Face Swap", callback_data="credit_cost_face_swap")],
        [InlineKeyboardButton("📍 Pincode Search", callback_data="credit_cost_pincode_search")],
        [InlineKeyboardButton("🌐 IP Info Search", callback_data="credit_cost_ip_info_search")],
        [InlineKeyboardButton("📞 Number to Name", callback_data="credit_cost_num_name_search")],
        [InlineKeyboardButton("📷 Instagram Info", callback_data="credit_cost_instagram_search")],
        [InlineKeyboardButton("📹 Instagram Reel DL", callback_data="credit_cost_instagram_reel_download")],
        [InlineKeyboardButton("🎵 Spotify Music (Name)", callback_data="credit_cost_spotify_search")],
        [InlineKeyboardButton("🎵 Spotify Music (URL)", callback_data="credit_cost_spotify_url_search")],
        [InlineKeyboardButton("🔥 Free Fire Info", callback_data="credit_cost_freefire_search")],
        [InlineKeyboardButton("🔊 Text to Voice", callback_data="credit_cost_text_to_voice")],
        [InlineKeyboardButton("📺 YouTube Download", callback_data="credit_cost_youtube_download")],
        [InlineKeyboardButton("🧾 GST Number Lookup", callback_data="credit_cost_gst_search")],
        [InlineKeyboardButton("✨ Stylish Text", callback_data="credit_cost_stylish_text")],
        [InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_stats")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            cost_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            cost_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def show_credit_cost_edit(query, context, feature):
    """Show credit cost edit interface for a specific feature"""
    costs = load_credit_costs()
    current_cost = costs.get(feature, 1)
    
    # Format feature name for display
    feature_name = feature.replace('_', ' ').title()
    
    # Create the edit interface
    edit_text = (
        f"*💰 Edit Credit Cost*\n\n"
        f"Feature: {feature_name}\n"
        f"Current Cost: {current_cost} credits\n\n"
        "Please send the new credit cost (number between 0 and 100):"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Credit Costs", callback_data="admin_credit_costs")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            edit_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            edit_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    # Set the context to indicate we're editing this feature
    context.user_data["editing_credit_cost"] = feature

async def start_coupon_generation(query, context):
    """Start the advanced coupon generation process"""
    context.user_data["coupon_gen"] = {"step": 1}
    
    keyboard = [
        [InlineKeyboardButton("Credits", callback_data="coupon_type_credits")],
        [InlineKeyboardButton("Premium Days", callback_data="coupon_type_premium")],
        [InlineKeyboardButton("❌ Cancel", callback_data="coupon_gen_cancel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "*🎟️ Advanced Coupon Generator*\n\n"
        "Select coupon reward type:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def show_coupon_stats(query, context):
    """Show coupon statistics"""
    stats = get_coupon_stats()
    coupons = load_coupons()
    
    stats_text = (
        f"*📊 Coupon Statistics*\n\n"
        f"🔢 Total Coupons: {stats['total']}\n"
        f"✅ Active Coupons: {stats['active']}\n"
        f"❌ Expired Coupons: {stats['expired']}\n"
        f"📈 Used Coupons: {stats['used']}\n"
        f"📉 Unused Coupons: {stats['unused']}"
    )
    
    # Show recent coupons
    recent_coupons = []
    current_time = datetime.datetime.now()
    
    for code, coupon in coupons.get("coupons", {}).items():
        try:
            expiry = datetime.datetime.fromisoformat(coupon["expiry"])
            if expiry > current_time:  # Only active coupons
                recent_coupons.append((code, coupon))
        except:
            continue
    
    # Sort by creation date (newest first)
    recent_coupons.sort(key=lambda x: x[1].get("created_at", ""), reverse=True)
    
    if recent_coupons:
        stats_text += "\n\n*🔑 Recent Active Coupons:*\n"
        
        for code, coupon in recent_coupons[:5]:  # Show only 5 most recent
            reward_type = coupon.get("reward_type", "N/A")
            reward_value = coupon.get("reward_value", 0)
            used = coupon.get("used", 0)
            max_uses = coupon.get("max_uses", 0)
            
            stats_text += f"\n• `{code}`: {reward_value} {reward_type} ({used}/{max_uses} used)"
    
    await query.message.reply_text(stats_text, parse_mode="Markdown")

async def approve_payment(query, context, payment_id):
    """Handle payment approval"""
    if query.from_user.id != ADMIN_ID:
        return
    
    payment = get_payment(payment_id)
    if not payment:
        await query.answer("Payment not found!", show_alert=True)
        return
    
    # Ask for amount/credits
    await query.message.reply_text(
        f"*💳 Approve Payment*\n\n"
        f"User ID: {payment['user_id']}\n"
        f"Plan: {payment['plan_type']}\n"
        f"Details: {payment['plan_details']}\n\n"
        f"Send the amount to add (credits for credit plan, days for premium):",
        parse_mode="Markdown"
    )
    
    context.user_data["approving_payment"] = payment_id

async def reject_payment(query, context, payment_id):
    """Handle payment rejection"""
    if query.from_user.id != ADMIN_ID:
        return
    
    payment = get_payment(payment_id)
    if not payment:
        await query.answer("Payment not found!", show_alert=True)
        return
    
    update_payment(payment_id, "rejected")
    
    # Notify user
    try:
        await context.bot.send_message(
            payment["user_id"],
            "❌ Your payment has been rejected. Please contact admin for details."
        )
    except:
        pass
    
    await query.answer("Payment rejected!")
    await query.message.reply_text("✅ Payment rejected and user notified.")

# ==========================================

# ================= MESSAGE HANDLERS =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text and photo messages"""
    user_id = str(update.effective_user.id)
    text = update.message.text.strip() if update.message.text else ""
    
    # Check if user is banned
    if is_user_banned(user_id):
        ban_info = get_ban_info(user_id)
        await update.message.reply_photo(
            photo=INFO_IMAGE,
            caption=f"❌ *You are banned from using this bot*\n\nReason: {ban_info.get('reason', 'No reason provided')}",
            parse_mode="Markdown"
        )
        return
    
    # Check maintenance mode
    if is_maintenance_mode() and update.effective_user.id != ADMIN_ID:
        await update.message.reply_photo(
            photo=MAINTENANCE_IMAGE,
            caption=get_maintenance_message(),
            parse_mode="Markdown"
        )
        return
    
    # Handle credit cost editing
    if context.user_data.get("editing_credit_cost"):
        feature = context.user_data["editing_credit_cost"]
        del context.user_data["editing_credit_cost"]
        
        try:
            new_cost = int(text)
            if new_cost < 0 or new_cost > 100:
                await update.message.reply_text(
                    "❌ Invalid cost! Please send a number between 0 and 100.",
                    parse_mode="Markdown"
                )
                return
            
            # Update the credit cost
            costs = load_credit_costs()
            costs[feature] = new_cost
            save_credit_costs(costs)
            
            # Format feature name for display
            feature_name = feature.replace('_', ' ').title()
            
            await update.message.reply_text(
                f"✅ Credit cost for {feature_name} updated to {new_cost} credits!",
                parse_mode="Markdown"
            )
            
            # Show the updated credit costs
            await show_credit_costs(update.callback_query, context)
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid input! Please send a valid number.",
                parse_mode="Markdown"
            )
        return
    
    # Handle admin commands
    if update.effective_user.id == ADMIN_ID and context.user_data.get("admin_action"):
        action = context.user_data["admin_action"]
        
        if action == "broadcast" and context.user_data.get("broadcast_mode"):
            await process_broadcast(update, context)
            return
        
        if action == "create_coupon" and context.user_data.get("coupon_creation"):
            await process_coupon_creation(update, context)
            return
    
    # Handle maintenance message edit
    if context.user_data.get("editing_maintenance_message") and update.effective_user.id == ADMIN_ID:
        context.user_data["editing_maintenance_message"] = False
        
        if set_maintenance_mode(True, text):
            await update.message.reply_text(
                f"✅ Maintenance message updated:\n\n{text}"
            )
        else:
            await update.message.reply_text("❌ Failed to update maintenance message")
        return
    
    # Handle ban user
    if context.user_data.get("ban_user_id") and update.effective_user.id == ADMIN_ID:
        context.user_data["ban_user_id"] = False
        context.user_data["ban_reason"] = True
        
        context.user_data["pending_ban_user"] = text
        await update.message.reply_text(
            f"*🚫 Ban User*\n\n"
            f"User ID: `{text}`\n\n"
            f"Now send the ban reason:",
            parse_mode="Markdown"
        )
        return
    
    # Handle ban reason
    if context.user_data.get("ban_reason") and update.effective_user.id == ADMIN_ID:
        user_to_ban = context.user_data.get("pending_ban_user")
        context.user_data["ban_reason"] = False
        del context.user_data["pending_ban_user"]
        
        if ban_user(user_to_ban, text):
            await update.message.reply_text(
                f"✅ User {user_to_ban} has been banned\nReason: {text}"
            )
            # Try to notify the banned user
            try:
                await context.bot.send_message(
                    chat_id=user_to_ban,
                    text=f"❌ You have been banned from using this bot\nReason: {text}"
                )
            except:
                pass
        else:
            await update.message.reply_text("❌ Failed to ban user")
        return
    
    # Handle unban user
    if context.user_data.get("unban_user_id") and update.effective_user.id == ADMIN_ID:
        context.user_data["unban_user_id"] = False
        
        if unban_user(text):
            await update.message.reply_text(f"✅ User {text} has been unbanned")
            # Try to notify the unbanned user
            try:
                await context.bot.send_message(
                    chat_id=text,
                    text="✅ You have been unbanned and can now use the bot again"
                )
            except:
                pass
        else:
            await update.message.reply_text("❌ Failed to unban user or user was not banned")
        return
    
    # Handle coupon generation process
    if context.user_data.get("coupon_gen"):
        await handle_coupon_generation(update, context)
        return
    
    # Handle coupon redemption
    if context.user_data.get("awaiting_coupon"):
        context.user_data["awaiting_coupon"] = False
        
        coupon = validate_coupon(text.upper())
        if not coupon:
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption="❌ Invalid or expired coupon code!"
            )
            return
        
        if use_coupon(text.upper(), user_id):
            reward_text = f"{coupon['reward_value']} credits" if coupon["reward_type"] == "credits" else f"{coupon['reward_value']} days premium"
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption=f"✅ Coupon redeemed successfully! You received {reward_text}."
            )
        else:
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption="❌ You have already used this coupon!"
            )
        return
    
    # Handle number search
    if context.user_data.get("awaiting_number"):
        context.user_data["awaiting_number"] = False
        
        if not text.isdigit() or len(text) != 10:
            await update.message.reply_photo(
                photo=SEARCH_IMAGE,
                caption="❌ Invalid number! Please send a 10-digit mobile number."
            )
            return
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("number_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Number search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("number_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Updated response handling for new API format
                if result.get("success") and result.get("result"):
                    # Get the first result
                    data = result["result"][0]
                    
                    # Extract data with defaults
                    mobile = data.get("mobile", "N/A")
                    name = data.get("name", "N/A")
                    father_name = data.get("father_name", "N/A")
                    address = data.get("address", "N/A")
                    alt_mobile = data.get("alt_mobile", "N/A")
                    circle = data.get("circle", "N/A")
                    id_number = data.get("id_number", "N/A")
                    email = data.get("email", "N/A")
                    
                    result_text = (
                        f"✅ *Search Result*\n\n"
                        f"📱 Mobile: `{mobile}`\n"
                        f"👤 Name: {name}\n"
                        f"👨 Father: {father_name}\n"
                        f"🏠 Address: {address}\n"
                        f"📞 Alt Mobile: {alt_mobile}\n"
                        f"📡 Circle: {circle}\n"
                        f"🆔 ID: {id_number}\n"
                        f"📧 Email: {email}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        result_text += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        result_text += "👑 *Premium User - Unlimited Searches*"
                    
                    # Send search result with image
                    await update.message.reply_photo(
                        photo=SEARCH_RESULT_IMAGE,
                        caption=result_text,
                        parse_mode="Markdown"
                    )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=SEARCH_IMAGE,
                        caption="❌ No record found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Search error: {e}")
        return
    
    # Handle vehicle search
    if context.user_data.get("awaiting_vehicle"):
        context.user_data["awaiting_vehicle"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for `{text}`",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("vehicle_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=VEHICLE_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Vehicle search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credits
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("vehicle_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                VEHICLE_API_URL,
                params={"number": text},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract data with defaults
                rc = data.get("rc_number", "NA")
                owner = data.get("owner_name", "NA")
                father = data.get("father_name", "NA")
                serial = data.get("owner_serial_no", "NA")
                model = data.get("model_name", "NA")
                variant = data.get("maker_model", "NA")
                vclass = data.get("vehicle_class", "NA")
                fuel = data.get("fuel_type", "NA")
                norms = data.get("fuel_norms", "NA")
                regDate = data.get("registration_date", "NA")
                insurer = data.get("insurance_company", "NA")
                insExpiry = data.get("insurance_expiry", data.get("insurance_upto", "NA"))
                fitness = data.get("fitness_upto", "NA")
                puc = data.get("puc_upto", "NA")
                tax = data.get("tax_upto", "NA")
                rto = data.get("rto", "NA")
                city = data.get("city", "NA")
                address = data.get("address", "NA")
                phone = data.get("phone", "NA")
                
                # Format message
                msg = (
                    f"*🚘 Vehicle RC Information*\n\n"
                    f"🔢 *RC Number:* `{rc}`\n"
                    f"👤 *Owner:* `{owner}`\n"
                    f"👪 *Father's Name:* `{father}`\n"
                    f"🔁 *Owner Serial:* `{serial}`\n\n"
                    f"🏍️ *Model:* `{model}`\n"
                    f"🧩 *Variant:* `{variant}`\n"
                    f"🚦 *Vehicle Class:* `{vclass}`\n"
                    f"⛽ *Fuel Type:* `{fuel}`\n"
                    f"♻️ *Fuel Norms:* `{norms}`\n\n"
                    f"🗓️ *Registration Date:* `{regDate}`\n"
                    f"🛡️ *Insurance Company:* `{insurer}`\n"
                    f"📅 *Insurance Valid Till:* `{insExpiry}`\n"
                    f"🏋️ *Fitness Valid Till:* `{fitness}`\n"
                    f"📄 *PUC Valid Till:* `{puc}`\n"
                    f"💸 *Tax Paid Till:* `{tax}`\n\n"
                    f"📍 *RTO Office:* `{rto}`\n"
                    f"🏙️ *City:* `{city}`\n"
                    f"🏠 *Address:* `{address}`\n"
                    f"📞 *Phone:* `{phone}`\n\n"
                )
                
                if not is_premium_user(user_id):
                    msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                else:
                    msg += "👑 *Premium User - Unlimited Searches*"
                
                # Send with reply markup
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                ])
                
                await update.message.reply_photo(
                    photo=VEHICLE_SEARCH_IMAGE,
                    caption=msg,
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
            else:
                # Refund credits if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=VEHICLE_SEARCH_IMAGE,
                    caption="❌ No record found!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credits if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=VEHICLE_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credits refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Vehicle search error: {e}")
        return
    
    # Handle pincode search
    if context.user_data.get("awaiting_pincode"):
        context.user_data["awaiting_pincode"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for pincode `{text}`",
            parse_mode="Markdown"
        )
        
        # Validate pincode
        if not text.isdigit() or len(text) != 6:
            await update.message.reply_photo(
                photo=PINCODE_SEARCH_IMAGE,
                caption="❌ Invalid pincode! Please send a 6-digit Indian pincode."
            )
            return
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("pincode_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=PINCODE_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Pincode search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("pincode_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{PINCODE_API_URL}/{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0 and data[0].get("Status") == "Success":
                    result = data[0]
                    post_offices = result.get("PostOffice", [])
                    
                    if post_offices and len(post_offices) > 0:
                        # Format the result
                        msg = (
                            f"*📍 Pincode Information*\n\n"
                            f"🔢 *Pincode:* `{text}`\n"
                            f"📊 *Status:* {result.get('Status', 'N/A')}\n"
                            f"📝 *Message:* {result.get('Message', 'N/A')}\n\n"
                            f"🏢 *Found {len(post_offices)} Post Office(s):*\n"
                        )
                        
                        # Add details for each post office
                        for i, office in enumerate(post_offices[:3]):  # Limit to first 3 offices
                            msg += (
                                f"\n*📍 Location {i+1}:*\n"
                                f"🏢 *Name:* {office.get('Name', 'N/A')}\n"
                                f"🏭 *Branch Type:* {office.get('BranchType', 'N/A')}\n"
                                f"🚚 *Delivery Status:* {office.get('DeliveryStatus', 'N/A')}\n"
                                f"🗺️ *District:* {office.get('District', 'N/A')}\n"
                                f"🏛️ *State:* {office.get('State', 'N/A')}\n"
                            )
                        
                        if len(post_offices) > 3:
                            msg += f"\n\n*... and {len(post_offices) - 3} more post offices*"
                        
                        if not is_premium_user(user_id):
                            msg += f"\n\n💰 Remaining Credits: {get_user(user_id)['balance']}"
                        else:
                            msg += "\n\n👑 *Premium User - Unlimited Searches*"
                        
                        # Send with reply markup
                        reply_markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                        ])
                        
                        await update.message.reply_photo(
                            photo=PINCODE_SEARCH_IMAGE,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    else:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        await update.message.reply_photo(
                            photo=PINCODE_SEARCH_IMAGE,
                            caption="❌ No post offices found for this pincode!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=PINCODE_SEARCH_IMAGE,
                        caption="❌ Invalid pincode or no data found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=PINCODE_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=PINCODE_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Pincode search error: {e}")
        return
    
    # Handle IP info search
    if context.user_data.get("awaiting_ip"):
        context.user_data["awaiting_ip"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for IP `{text}`",
            parse_mode="Markdown"
        )
        
        # Validate IP address (basic validation)
        ip_parts = text.split('.')
        if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
            await update.message.reply_photo(
                photo=IP_INFO_SEARCH_IMAGE,
                caption="❌ Invalid IP address! Please send a valid IP address (e.g., 8.8.8.8)."
            )
            return
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("ip_info_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=IP_INFO_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! IP info search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credits
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("ip_info_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{IP_INFO_API_URL}?ip={text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract data with defaults
                ip = data.get("IP", "NA")
                asn = data.get("ASN", "NA")
                city = data.get("City", "NA")
                continent = data.get("Continent", "NA")
                country = data.get("Country", "NA")
                country_code = data.get("Country_Code", "NA")
                currency = data.get("Currency", "NA")
                currency_code = data.get("Currency_Code", "NA")
                currency_symbol = data.get("Currency_Symbol", "NA")
                domain = data.get("Domain", "NA")
                flag_emoji = data.get("Flag_Emoji", "NA")
                flag_image = data.get("Flag_Image", "NA")
                isp = data.get("ISP", "NA")
                languages = data.get("Languages", "NA")
                latitude = data.get("Latitude", "NA")
                location = data.get("Location", "NA")
                longitude = data.get("Longitude", "NA")
                org = data.get("ORG", "NA")
                postal = data.get("Postal", "NA")
                region = data.get("Region", "NA")
                timezone = data.get("Timezone", "NA")
                timezone_offset = data.get("Timezone_Offset", "NA")
                ip_type = data.get("Type", "NA")
                
                # Format message
                msg = (
                    f"*🌐 IP Information*\n\n"
                    f"🌍 *IP Address:* `{ip}`\n"
                    f"🔢 *Type:* {ip_type}\n"
                    f"🏢 *ISP:* {isp}\n"
                    f"🏭 *Organization:* {org}\n"
                    f"🔢 *ASN:* {asn}\n"
                    f"🌐 *Domain:* {domain}\n\n"
                    f"📍 *Location Details:*\n"
                    f"🏙️ *City:* {city}\n"
                    f"🗺️ *Region:* {region}\n"
                    f"🌍 *Country:* {country} {flag_emoji}\n"
                    f"🔤 *Country Code:* {country_code}\n"
                    f"🌎 *Continent:* {continent}\n"
                    f"📮 *Postal Code:* {postal}\n"
                    f"📍 *Coordinates:* {latitude}, {longitude}\n"
                    f"🗺️ *Location:* {location}\n\n"
                    f"💰 *Currency Details:*\n"
                    f"💵 *Currency:* {currency}\n"
                    f"💱 *Currency Code:* {currency_code}\n"
                    f"💴 *Currency Symbol:* {currency_symbol}\n\n"
                    f"⏰ *Timezone:* {timezone}\n"
                    f"🕐 *Timezone Offset:* {timezone_offset}\n"
                    f"🗣️ *Languages:* {languages}\n\n"
                )
                
                if not is_premium_user(user_id):
                    msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                else:
                    msg += "👑 *Premium User - Unlimited Searches*"
                
                # Send with reply markup
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                ])
                
                # Try to send flag image if available
                if flag_image != "NA":
                    try:
                        await update.message.reply_photo(
                            photo=flag_image,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    except:
                        # If flag image fails, send with default image
                        await update.message.reply_photo(
                            photo=IP_INFO_SEARCH_IMAGE,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                else:
                    await update.message.reply_photo(
                        photo=IP_INFO_SEARCH_IMAGE,
                        caption=msg,
                        parse_mode="Markdown",
                        reply_markup=reply_markup
                    )
            else:
                # Refund credits if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=IP_INFO_SEARCH_IMAGE,
                    caption="❌ No record found!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credits if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=IP_INFO_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credits refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"IP info search error: {e}")
        return
    
    # Handle number to name search
    if context.user_data.get("awaiting_num_name"):
        context.user_data["awaiting_num_name"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for number `{text}`",
            parse_mode="Markdown"
        )
        
        # Validate number (basic validation - should be numeric)
        if not text.isdigit():
            await update.message.reply_photo(
                photo=NUM_NAME_SEARCH_IMAGE,
                caption="❌ Invalid number! Please send a valid mobile number with country code (e.g., 919065146522)."
            )
            return
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("num_name_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=NUM_NAME_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Number to name search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("num_name_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{NUM_NAME_API_URL}?number={text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success") and result.get("data") and result["data"].get("success"):
                    data = result["data"]
                    
                    # Extract data
                    name = data.get("name", "N/A")
                    number = data.get("number", "N/A")
                    
                    # Format message
                    msg = (
                        f"*📞 Number to Name Result*\n\n"
                        f"📱 *Number:* `{number}`\n"
                        f"👤 *Name:* {name}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        msg += "👑 *Premium User - Unlimited Searches*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    await update.message.reply_photo(
                        photo=NUM_NAME_SEARCH_IMAGE,
                        caption=msg,
                        parse_mode="Markdown",
                        reply_markup=reply_markup
                    )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=NUM_NAME_SEARCH_IMAGE,
                        caption="❌ No record found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=NUM_NAME_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=NUM_NAME_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Number to name search error: {e}")
        return
    
    # Handle Instagram search
    if context.user_data.get("awaiting_instagram"):
        context.user_data["awaiting_instagram"] = False
        
        # Validate username (basic validation - should not contain @)
        if text.startswith("@"):
            text = text[1:]  # Remove @ if user included it
        
        if not text or len(text) < 1:
            await update.message.reply_photo(
                photo=INSTAGRAM_SEARCH_IMAGE,
                caption="❌ Invalid username! Please send a valid Instagram username (without @)."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for username `{text}`",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("instagram_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=INSTAGRAM_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Instagram info search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("instagram_search", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{INSTAGRAM_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data and "id" in data:
                    # First, send the profile information
                    profile_data = format_instagram_data(data)
                    
                    if not is_premium_user(user_id):
                        profile_data += f"\n💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        profile_data += "\n👑 *Premium User - Unlimited Searches*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    # Try to send with profile picture if available
                    profile_pic = data.get("pic", "")
                    if profile_pic:
                        try:
                            await update.message.reply_photo(
                                photo=profile_pic,
                                caption=profile_data,
                                parse_mode="HTML",
                                reply_markup=reply_markup
                            )
                        except:
                            # If profile picture fails, send with default image
                            await update.message.reply_photo(
                                photo=INSTAGRAM_SEARCH_IMAGE,
                                caption=profile_data,
                                parse_mode="HTML",
                                reply_markup=reply_markup
                            )
                    else:
                        await update.message.reply_photo(
                            photo=INSTAGRAM_SEARCH_IMAGE,
                            caption=profile_data,
                            parse_mode="HTML",
                            reply_markup=reply_markup
                        )
                    
                    # Now send the posts separately
                    recent_posts = data.get("recent", [])
                    if recent_posts and len(recent_posts) > 0:
                        # Send a message about posts
                        await update.message.reply_text(
                            f"📸 *Recent Posts*\n\nFound {len(recent_posts)} recent posts. Sending details...",
                            parse_mode="Markdown"
                        )
                        
                        # Send each post separately
                        for i, post in enumerate(recent_posts[:6]):  # Limit to first 6 posts
                            post_id = post.get("id", "N/A")
                            post_code = post.get("code", "N/A")
                            post_img = post.get("img", "")
                            caption = post.get("cap", "No caption")
                            
                            # Extract hashtags from caption
                            hashtags = extract_hashtags(caption) if caption else []
                            
                            # Format post message
                            post_msg = format_instagram_post(post, i+1)
                            
                            # Send with reply markup
                            post_reply_markup = InlineKeyboardMarkup([
                                [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                            ])
                            
                            # Send post image with caption
                            if post_img:
                                try:
                                    await update.message.reply_photo(
                                        photo=post_img,
                                        caption=post_msg,
                                        parse_mode="HTML",
                                        reply_markup=post_reply_markup
                                    )
                                except:
                                    # If image fails, send text only
                                    await update.message.reply_text(
                                        post_msg,
                                        parse_mode="HTML",
                                        reply_markup=post_reply_markup
                                    )
                            else:
                                await update.message.reply_text(
                                    post_msg,
                                    parse_mode="HTML",
                                    reply_markup=post_reply_markup
                                )
                            
                            # Add a small delay to avoid flooding
                            await asyncio.sleep(1)
                        
                        # If there are more posts, inform user
                        if len(recent_posts) > 6:
                            await update.message.reply_text(
                                f"📝 *Note*: Only showing first 6 posts. Total posts: {len(recent_posts)}",
                                parse_mode="Markdown"
                            )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=INSTAGRAM_SEARCH_IMAGE,
                        caption="❌ Profile not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=INSTAGRAM_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=INSTAGRAM_SEARCH_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Instagram search error: {e}")
        return
    
    # Handle Instagram Reel download
    if context.user_data.get("awaiting_instagram_reel"):
        context.user_data["awaiting_instagram_reel"] = False
        
        # Validate Instagram Reel URL
        if not text.startswith("https://www.instagram.com/reel/") and not text.startswith("https://instagram.com/reel/"):
            await update.message.reply_photo(
                photo=INSTAGRAM_REEL_IMAGE,
                caption="❌ Invalid Instagram Reel URL! Please send a valid Instagram Reel URL."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your Instagram Reel URL",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("instagram_reel_download")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=INSTAGRAM_REEL_IMAGE,
                    caption=f"❌ Insufficient credits! Instagram Reel download requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("instagram_reel_download", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{INSTAGRAM_REEL_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get("error") and data.get("result"):
                    result = data.get("result", {})
                    
                    # Extract data
                    duration = result.get("duration", 0)
                    quality = result.get("quality", "N/A")
                    extension = result.get("extension", "N/A")
                    size = result.get("size", 0)
                    formatted_size = result.get("formattedSize", "N/A")
                    download_url = result.get("url", "")
                    
                    # Format message
                    msg = (
                        f"*📹 Instagram Reel Download*\n\n"
                        f"⏱️ *Duration:* {duration} seconds\n"
                        f"📺 *Quality:* {quality}\n"
                        f"📁 *Format:* {extension}\n"
                        f"💾 *Size:* {formatted_size}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        msg += "👑 *Premium User - Unlimited Downloads*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    # Send the video
                    if download_url:
                        try:
                            await update.message.reply_video(
                                video=download_url,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                        except Exception as e:
                            logger.error(f"Error sending video: {e}")
                            await update.message.reply_text(
                                f"⚠️ Video download failed. You can download manually: {download_url}",
                                parse_mode="Markdown"
                            )
                    else:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        await update.message.reply_photo(
                            photo=INSTAGRAM_REEL_IMAGE,
                            caption="❌ Download URL not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=INSTAGRAM_REEL_IMAGE,
                        caption="❌ Reel not found or private!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=INSTAGRAM_REEL_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=INSTAGRAM_REEL_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Instagram Reel download error: {e}")
        return
    
    # Handle Spotify search by name
    if context.user_data.get("awaiting_spotify"):
        context.user_data["awaiting_spotify"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Searching for song: `{text}`",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("spotify_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=SPOTIFY_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Spotify music download requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("spotify_search", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{SPOTIFY_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status"):
                    metadata = data.get("metadata", {})
                    download = data.get("download", {})
                    
                    # Extract data
                    title = metadata.get("title", "N/A")
                    artists = metadata.get("artists", "N/A")
                    duration_ms = metadata.get("duration_ms", 0)
                    cover = metadata.get("cover", "")
                    download_url = download.get("mp3", "")
                    
                    # Convert duration to minutes:seconds
                    duration_min = duration_ms // 60000
                    duration_sec = (duration_ms % 60000) // 1000
                    duration = f"{duration_min}:{duration_sec:02d}"
                    
                    # Format message
                    msg = (
                        f"*🎵 Spotify Music Download (by Name)*\n\n"
                        f"🎶 *Title:* {title}\n"
                        f"👥 *Artists:* {artists}\n"
                        f"⏱️ *Duration:* {duration}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        msg += "👑 *Premium User - Unlimited Downloads*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    # Try to send with cover image if available
                    if cover:
                        try:
                            await update.message.reply_photo(
                                photo=cover,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                        except:
                            # If cover image fails, send with default image
                            await update.message.reply_photo(
                                photo=SPOTIFY_SEARCH_IMAGE,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                    else:
                        await update.message.reply_photo(
                            photo=SPOTIFY_SEARCH_IMAGE,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    
                    # Send the audio file
                    if download_url:
                        try:
                            await update.message.reply_audio(
                                audio=download_url,
                                title=title,
                                performer=artists,
                                caption=f"🎵 {title} - {artists}"
                            )
                        except Exception as e:
                            logger.error(f"Error sending audio: {e}")
                            await update.message.reply_text(
                                f"⚠️ Audio download failed. You can download manually: {download_url}"
                            )
                    else:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        await update.message.reply_text(
                            "❌ Download URL not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=SPOTIFY_SEARCH_IMAGE,
                        caption="❌ Song not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=SPOTIFY_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=SPOTIFY_SEARCH_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Spotify search error: {e}")
        return
    
    # Handle Spotify search by URL
    if context.user_data.get("awaiting_spotify_url"):
        context.user_data["awaiting_spotify_url"] = False
        
        # Validate Spotify URL
        if not text.startswith("https://open.spotify.com/track/"):
            await update.message.reply_photo(
                photo=SPOTIFY_SEARCH_IMAGE,
                caption="❌ Invalid Spotify URL! Please send a valid Spotify track URL."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your Spotify URL: `{text[:30]}...`",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("spotify_url_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=SPOTIFY_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Spotify URL download requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("spotify_url_search", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{SPOTIFY_URL_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status"):
                    metadata = data.get("metadata", {})
                    download = data.get("download", {})
                    
                    # Extract data
                    title = metadata.get("title", "N/A")
                    artists = metadata.get("artists", "N/A")
                    duration_ms = metadata.get("duration_ms", 0)
                    cover = metadata.get("cover", "")
                    download_url = download.get("mp3", "")
                    
                    # Convert duration to minutes:seconds
                    duration_min = duration_ms // 60000
                    duration_sec = (duration_ms % 60000) // 1000
                    duration = f"{duration_min}:{duration_sec:02d}"
                    
                    # Format message
                    msg = (
                        f"*🎵 Spotify Music Download (by URL)*\n\n"
                        f"🎶 *Title:* {title}\n"
                        f"👥 *Artists:* {artists}\n"
                        f"⏱️ *Duration:* {duration}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        msg += "👑 *Premium User - Unlimited Downloads*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    # Try to send with cover image if available
                    if cover:
                        try:
                            await update.message.reply_photo(
                                photo=cover,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                        except:
                            # If cover image fails, send with default image
                            await update.message.reply_photo(
                                photo=SPOTIFY_SEARCH_IMAGE,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                    else:
                        await update.message.reply_photo(
                            photo=SPOTIFY_SEARCH_IMAGE,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    
                    # Send the audio file
                    if download_url:
                        try:
                            await update.message.reply_audio(
                                audio=download_url,
                                title=title,
                                performer=artists,
                                caption=f"🎵 {title} - {artists}"
                            )
                        except Exception as e:
                            logger.error(f"Error sending audio: {e}")
                            await update.message.reply_text(
                                f"⚠️ Audio download failed. You can download manually: {download_url}"
                            )
                    else:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        await update.message.reply_text(
                            "❌ Download URL not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=SPOTIFY_SEARCH_IMAGE,
                        caption="❌ Song not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=SPOTIFY_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=SPOTIFY_SEARCH_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Spotify URL search error: {e}")
        return
    
    # Handle Free Fire search
    if context.user_data.get("awaiting_freefire"):
        context.user_data["awaiting_freefire"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for Free Fire UID `{text}`",
            parse_mode="Markdown"
        )
        
        # Validate UID (basic validation - should be numeric)
        if not text.isdigit():
            await update.message.reply_photo(
                photo=FREEFIRE_SEARCH_IMAGE,
                caption="❌ Invalid UID! Please send a valid Free Fire UID (numbers only)."
            )
            return
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("freefire_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=FREEFIRE_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! Free Fire info search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("freefire_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{FREEFIRE_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data and "basicinfo" in data:
                    # Format the result
                    result_text = format_freefire_data(data)
                    
                    if not is_premium_user(user_id):
                        result_text += f"\n💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        result_text += "\n👑 *Premium User - Unlimited Searches*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    await update.message.reply_photo(
                        photo=FREEFIRE_SEARCH_IMAGE,
                        caption=result_text,
                        parse_mode="Markdown",
                        reply_markup=reply_markup
                    )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=FREEFIRE_SEARCH_IMAGE,
                        caption="❌ No record found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=FREEFIRE_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=FREEFIRE_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credits refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Free Fire search error: {e}")
        return
    
    # Handle Text to Voice
    if context.user_data.get("awaiting_text_to_voice"):
        context.user_data["awaiting_text_to_voice"] = False
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Converting your text to voice...",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("text_to_voice")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=TEXT_TO_VOICE_IMAGE,
                    caption=f"❌ Insufficient credits! Text to voice requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("text_to_voice", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{TEXT_TO_VOICE_API_URL}?text={text}&voice=Emma",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get("error") and data.get("audio"):
                    # Extract audio data
                    audio_data = data.get("audio", "")
                    
                    # Decode base64 audio data
                    try:
                        # Remove data URL prefix if present
                        if audio_data.startswith("data:audio/mpeg;base64,"):
                            audio_data = audio_data.split(",", 1)[1]
                        
                        # Decode base64
                        audio_bytes = base64.b64decode(audio_data)
                        
                        # Create a file-like object
                        audio_io = io.BytesIO(audio_bytes)
                        audio_io.name = "voice.mp3"
                        
                        # Send the audio file
                        caption = f"🔊 *Text to Voice*\n\n"
                        if not is_premium_user(user_id):
                            caption += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                        else:
                            caption += "👑 *Premium User - Unlimited Conversions*"
                        
                        # Add Made by @synaxnetwork instead of API credits
                        caption += "\n\nMade by @synaxnetwork"
                        
                        # Send with reply markup
                        reply_markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                        ])
                        
                        await update.message.reply_audio(
                            audio=audio_io,
                            caption=caption,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    except Exception as e:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        logger.error(f"Error processing audio: {e}")
                        await update.message.reply_photo(
                            photo=TEXT_TO_VOICE_IMAGE,
                            caption="❌ Failed to process audio!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=TEXT_TO_VOICE_IMAGE,
                        caption="❌ Failed to convert text to voice!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=TEXT_TO_VOICE_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=TEXT_TO_VOICE_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"Text to voice error: {e}")
        return
    
    # Handle YouTube download
    if context.user_data.get("awaiting_youtube"):
        context.user_data["awaiting_youtube"] = False
        
        # Validate YouTube URL
        if not (text.startswith("https://www.youtube.com/watch?v=") or text.startswith("https://youtu.be/") or text.startswith("https://m.youtube.com/watch?v=")):
            await update.message.reply_photo(
                photo=YOUTUBE_SEARCH_IMAGE,
                caption="❌ Invalid YouTube URL! Please send a valid YouTube video URL."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your YouTube URL",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("youtube_download")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=YOUTUBE_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! YouTube download requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("youtube_download", credit_cost)
        
        try:
            # Make API request
            response = requests.get(
                f"{YOUTUBE_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") and data.get("video"):
                    # Extract data
                    title = data.get("title", "N/A")
                    channel = data.get("channel", "N/A")
                    duration = data.get("duration", "N/A")
                    views = data.get("views", "N/A")
                    quality = data.get("quality", "N/A")
                    thumb = data.get("thumb", "")
                    video_url = data.get("video", "")
                    video_hd_url = data.get("video_hd", "")
                    audio_url = data.get("audio", "")
                    formats = data.get("formats", [])
                    
                    # Format message
                    msg = (
                        f"*📺 YouTube Video Download*\n\n"
                        f"🎬 *Title:* {title}\n"
                        f"📺 *Channel:* {channel}\n"
                        f"⏱️ *Duration:* {duration}\n"
                        f"👁️ *Views:* {views}\n"
                        f"📊 *Quality:* {quality}\n\n"
                    )
                    
                    if not is_premium_user(user_id):
                        msg += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        msg += "👑 *Premium User - Unlimited Downloads*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    # Send video info with thumbnail
                    if thumb:
                        try:
                            await update.message.reply_photo(
                                photo=thumb,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                        except:
                            # If thumbnail fails, send with default image
                            await update.message.reply_photo(
                                photo=YOUTUBE_SEARCH_IMAGE,
                                caption=msg,
                                parse_mode="Markdown",
                                reply_markup=reply_markup
                            )
                    else:
                        await update.message.reply_photo(
                            photo=YOUTUBE_SEARCH_IMAGE,
                            caption=msg,
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                    
                    # Find the best quality video format
                    best_video = get_best_quality_video(formats)
                    
                    # Send the video (prefer HD if available)
                    video_to_send = video_hd_url if video_hd_url else video_url
                    
                    # If we have a better quality video from formats, use that
                    if best_video and best_video.get("url"):
                        video_to_send = best_video["url"]
                    
                    if video_to_send:
                        try:
                            # Try to send the video directly
                            await update.message.reply_video(
                                video=video_to_send,
                                caption=f"📺 {title}",
                                parse_mode="Markdown"
                            )
                        except Exception as e:
                            logger.error(f"Error sending video: {e}")
                            
                            # If direct video sending fails, try to download and send
                            try:
                                # Download the video
                                video_response = requests.get(video_to_send, stream=True, timeout=60)
                                video_response.raise_for_status()
                                
                                # Create a file-like object
                                video_io = io.BytesIO()
                                for chunk in video_response.iter_content(chunk_size=8192):
                                    video_io.write(chunk)
                                video_io.seek(0)
                                video_io.name = "video.mp4"
                                
                                # Send the downloaded video
                                await update.message.reply_video(
                                    video=video_io,
                                    caption=f"📺 {title}",
                                    parse_mode="Markdown"
                                )
                            except Exception as download_error:
                                logger.error(f"Error downloading video: {download_error}")
                                await update.message.reply_text(
                                    f"⚠️ Video download failed. You can download manually:\n\n"
                                    f"📹 *Video (SD):* [Download]({video_url})\n"
                                    f"📹 *Video (HD):* [Download]({video_hd_url})\n"
                                    f"🎵 *Audio Only:* [Download]({audio_url})",
                                    parse_mode="Markdown",
                                    disable_web_page_preview=True
                                )
                    else:
                        # Refund credit if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        await update.message.reply_text(
                            "❌ Download URL not found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=YOUTUBE_SEARCH_IMAGE,
                        caption="❌ Video not found or private!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=YOUTUBE_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=YOUTUBE_SEARCH_IMAGE,
                caption=f"❌ Error: {str(e)}" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"YouTube download error: {e}")
        return
    
    # Handle GST search
    if context.user_data.get("awaiting_gst"):
        context.user_data["awaiting_gst"] = False
        
        # Validate GST number (basic validation - should be 15 characters alphanumeric)
        if not text or len(text) != 15 or not text.isalnum():
            await update.message.reply_photo(
                photo=GST_SEARCH_IMAGE,
                caption="❌ Invalid GST number! Please send a valid 15-digit GST number (e.g., 19BOKPS7056D1ZI)."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"*Please Wait...* Processing your request for GST number `{text}`",
            parse_mode="Markdown"
        )
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("gst_search")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=GST_SEARCH_IMAGE,
                    caption=f"❌ Insufficient credits! GST search requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("gst_search", credit_cost)
        
        # Perform API search
        try:
            response = requests.get(
                f"{GST_API_URL}{text}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            # Delete processing message
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=processing_msg.message_id
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and data.get("data"):
                    gst_data = data.get("data", {})
                    
                    # Format the result
                    result_text = format_gst_data(gst_data)
                    
                    if not is_premium_user(user_id):
                        result_text += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                    else:
                        result_text += "\n👑 *Premium User - Unlimited Searches*"
                    
                    # Send with reply markup
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🝐꯭𓆩꯭꯭⍣⃪𝗢ᴡɴᴇʀ⃪⍣꯭꯭𓆪꯭🝐", url="https://t.me/synaxnetwork")]
                    ])
                    
                    await update.message.reply_photo(
                        photo=GST_SEARCH_IMAGE,
                        caption=result_text,
                        parse_mode="Markdown",
                        reply_markup=reply_markup
                    )
                else:
                    # Refund credit if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    await update.message.reply_photo(
                        photo=GST_SEARCH_IMAGE,
                        caption="❌ No record found!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                    )
            else:
                # Refund credit if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                await update.message.reply_photo(
                    photo=GST_SEARCH_IMAGE,
                    caption="❌ API error!" + (" Credit refunded." if not is_premium_user(user_id) else "")
                )
                
        except Exception as e:
            # Refund credit if not premium
            if not is_premium_user(user_id):
                add_credits(user_id, credit_cost)
            await update.message.reply_photo(
                photo=GST_SEARCH_IMAGE,
                caption="❌ Search failed!" + (" Credit refunded." if not is_premium_user(user_id) else "")
            )
            logger.error(f"GST search error: {e}")
        return
    
    # Handle Stylish Text Generator
    if context.user_data.get("stylish_text_mode") == STYLISH_TEXT_MODE:
        context.user_data["stylish_text_mode"] = None
        
        # Check if user is premium or has enough credits
        credit_cost = get_credit_cost("stylish_text")
        if not is_premium_user(user_id):
            user = get_user(user_id)
            if user["balance"] < credit_cost:
                await update.message.reply_photo(
                    photo=STYLISH_TEXT_IMAGE,
                    caption=f"❌ Insufficient credits! Stylish text generation requires {credit_cost} credits. Please buy more credits."
                )
                return
            
            # Deduct credit
            remove_credits(user_id, credit_cost)
            # Update statistics
            update_search_stats("stylish_text", credit_cost)
        
        # Convert text to stylish font
        stylish_text = convert_to_stylish(text)
        
        # Send initial message
        start_msg = await update.message.reply_text(
            f"✨ *Generating {len(STYLES)} stylish text variations for:* `{text}`\n\n"
            f"⏳ Please wait, each style will be sent in a separate message for easy copying..."
        )
        
        # Send each style as a separate message
        for i, (prefix, suffix) in enumerate(STYLES, 1):
            try:
                # Create the stylish name
                styled_name = f"{prefix}{stylish_text}{suffix}"
                
                # Send the message with progress
                await update.message.reply_text(
                    f"✨ *Style {i}/{len(STYLES)}*\n\n{styled_name}"
                )
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error sending style {i}: {e}")
                continue
        
        # Edit the initial message to show completion
        await start_msg.edit_text(
            f"✅ *Generated {len(STYLES)} stylish text variations for:* `{text}`\n\n"
            f"💰 Remaining Credits: {get_user(user_id)['balance']}" if not is_premium_user(user_id) else "👑 Premium User - Unlimited Generations"
        )
        return
    
    # Handle payment approval amount
    if context.user_data.get("approving_payment"):
        payment_id = context.user_data["approving_payment"]
        context.user_data["approving_payment"] = None
        
        try:
            amount = int(text)
            payment = get_payment(payment_id)
            
            if payment:
                if payment["plan_type"] == "credits":
                    add_credits(payment["user_id"], amount)
                elif payment["plan_type"] == "premium":
                    add_premium(payment["user_id"], amount)
                
                update_payment(payment_id, "approved", approved_amount=amount)
                # Update payment stats
                update_payment_stats(payment["plan_type"], amount)
                
                # Notify user
                try:
                    await context.bot.send_message(
                        payment["user_id"],
                        f"✅ Your payment has been approved! You received {amount} {'credits' if payment['plan_type'] == 'credits' else 'days premium'}."
                    )
                except:
                    pass
                
                await update.message.reply_text("✅ Payment approved successfully!")
            else:
                await update.message.reply_text("❌ Payment not found!")
        except ValueError:
            await update.message.reply_text("❌ Invalid amount! Please send a number.")
        return
    
    # Handle broadcast
    if context.user_data.get("broadcast_mode") and update.effective_user.id == ADMIN_ID:
        await process_broadcast(update, context)
        return
    
    # Handle coupon creation
    if context.user_data.get("coupon_creation") and update.effective_user.id == ADMIN_ID:
        await process_coupon_creation(update, context)
        return

async def handle_coupon_generation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the advanced coupon generation process"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    step = context.user_data["coupon_gen"]["step"]
    
    if step == 1:
        # This step is handled by callback buttons
        pass
    
    elif step == 2:
        # Step 2: Get reward value
        try:
            value = int(text)
            context.user_data["coupon_gen"]["value"] = value
            context.user_data["coupon_gen"]["step"] = 3
            
            await update.message.reply_text(
                f"*🎟️ Advanced Coupon Generator*\n\n"
                f"Reward type: {context.user_data['coupon_gen']['type']}\n\n"
                f"Now send the maximum number of uses for this coupon:",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid value! Please send a number.",
                parse_mode="Markdown"
            )
    
    elif step == 3:
        # Step 3: Get max uses
        try:
            max_uses = int(text)
            context.user_data["coupon_gen"]["max_uses"] = max_uses
            context.user_data["coupon_gen"]["step"] = 4
            
            await update.message.reply_text(
                f"*🎟️ Advanced Coupon Generator*\n\n"
                f"Reward type: {context.user_data['coupon_gen']['type']}\n"
                f"Reward value: {context.user_data['coupon_gen']['value']}\n"
                f"Max uses: {max_uses}\n\n"
                f"Now send the number of days until expiry (e.g., 30 for 30 days):",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid value! Please send a number.",
                parse_mode="Markdown"
            )
    
    elif step == 4:
        # Step 4: Get expiry days and generate coupon
        try:
            expiry_days = int(text)
            reward_type = context.user_data["coupon_gen"]["type"]
            reward_value = context.user_data["coupon_gen"]["value"]
            max_uses = context.user_data["coupon_gen"]["max_uses"]
            
            # Generate unique coupon code
            code = generate_coupon_code()
            
            # Create coupon
            if create_coupon(code, reward_type, reward_value, max_uses, expiry_days):
                # Get total users and credits
                users = load_users()
                total_users = len(users)
                total_credits = sum(u.get("balance", 0) for u in users.values())
                
                # Get coupon statistics
                coupon_stats = get_coupon_stats()
                
                # Calculate expiry date
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=expiry_days)
                expiry_formatted = expiry_date.strftime("%d-%m-%Y")
                
                # Send coupon details to admin in advanced format
                coupon_text = (
                    f"*🎟️ ADVANCED COUPON GENERATED*\n\n"
                    f"🔑 *Coupon Code:* `{code}`\n"
                    f"🎁 *Reward Type:* {reward_type.title()}\n"
                    f"💰 *Reward Value:* {reward_value} {'credits' if reward_type == 'credits' else 'days premium'}\n"
                    f"👥 *Max Uses:* {max_uses}\n"
                    f"📅 *Expiry Date:* {expiry_formatted}\n"
                    f"📊 *Redeem Status:* 0/{max_uses} redeemed\n\n"
                    f"📈 *SYSTEM STATISTICS*\n"
                    f"👥 *Total Users:* {total_users}\n"
                    f"💳 *Total Credits:* {total_credits}\n"
                    f"🔢 *Total Coupons:* {coupon_stats['total']}\n"
                    f"✅ *Active Coupons:* {coupon_stats['active']}\n\n"
                    f"🕐 *Created At:* {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                # Create action buttons
                keyboard = [
                    [
                        InlineKeyboardButton("📋 Copy Code", callback_data=f"copy_coupon_{code}"),
                        InlineKeyboardButton("📊 View Stats", callback_data="admin_coupon_stats")
                    ],
                    [InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_stats")]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    coupon_text,
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
                
                # Clean up
                del context.user_data["coupon_gen"]
            else:
                await update.message.reply_text(
                    "❌ Failed to create coupon! Please try again.",
                    parse_mode="Markdown"
                )
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid value! Please send a number.",
                parse_mode="Markdown"
            )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages (payment screenshots and face swap)"""
    user_id = str(update.effective_user.id)
    
    # Check if user is banned
    if is_user_banned(user_id):
        ban_info = get_ban_info(user_id)
        await update.message.reply_photo(
            photo=INFO_IMAGE,
            caption=f"❌ *You are banned from using this bot*\n\nReason: {ban_info.get('reason', 'No reason provided')}",
            parse_mode="Markdown"
        )
        return
    
    # Check maintenance mode
    if is_maintenance_mode() and update.effective_user.id != ADMIN_ID:
        await update.message.reply_photo(
            photo=MAINTENANCE_IMAGE,
            caption=get_maintenance_message(),
            parse_mode="Markdown"
        )
        return
    
    # Handle face swap photos
    if context.user_data.get("face_swap_state") is not None:
        face_swap_state = context.user_data["face_swap_state"]
        
        # Get the photo file
        photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        if face_swap_state == FACE_SWAP_SOURCE:
            # Store source photo and update state
            context.user_data["face_swap_source"] = photo_bytes
            context.user_data["face_swap_state"] = FACE_SWAP_TARGET
            
            await update.message.reply_photo(
                photo=FACE_SWAP_IMAGE,
                caption="✅ *Source image received*\n\n📸 Now send the *TARGET* image (where the face will be placed)",
                parse_mode="Markdown"
            )
            return
        
        elif face_swap_state == FACE_SWAP_TARGET:
            # Get source photo
            source_bytes = context.user_data.get("face_swap_source")
            if not source_bytes:
                await update.message.reply_photo(
                    photo=FACE_SWAP_IMAGE,
                    caption="❌ Source image not found. Please start over.",
                    parse_mode="Markdown"
                )
                # Reset state
                if "face_swap_state" in context.user_data:
                    del context.user_data["face_swap_state"]
                if "face_swap_source" in context.user_data:
                    del context.user_data["face_swap_source"]
                return
            
            # Check if user is premium or has enough credits
            credit_cost = get_credit_cost("face_swap")
            if not is_premium_user(user_id):
                user = get_user(user_id)
                if user["balance"] < credit_cost:
                    await update.message.reply_photo(
                        photo=FACE_SWAP_IMAGE,
                        caption=f"❌ Insufficient credits! Face swap requires {credit_cost} credits. Please buy more credits."
                    )
                    # Reset state
                    if "face_swap_state" in context.user_data:
                        del context.user_data["face_swap_state"]
                    if "face_swap_source" in context.user_data:
                        del context.user_data["face_swap_source"]
                    return
                
                # Deduct credits
                remove_credits(user_id, credit_cost)
                # Update statistics
                update_search_stats("face_swap", credit_cost)
            
            # Send processing message
            processing_msg = await update.message.reply_text(
                "⏳ *Swapping faces...* This may take a moment.",
                parse_mode="Markdown"
            )
            
            try:
                # Create a BytesIO object for the source image
                source_io = io.BytesIO(source_bytes)
                source_io.name = "source.jpg"
                
                # Create a BytesIO object for the target image
                target_io = io.BytesIO(photo_bytes)
                target_io.name = "target.jpg"
                
                # Prepare form data
                files = {
                    'source': (source_io.name, source_io, 'image/jpeg'),
                    'target': (target_io.name, target_io, 'image/jpeg')
                }
                
                # Make API request
                response = requests.post(
                    FACE_SWAP_API_URL,
                    files=files,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Android)",
                        "origin": "https://ab-faceswap.vercel.app",
                        "referer": "https://ab-faceswap.vercel.app/"
                    },
                    timeout=60  # Increased timeout for large images
                )
                
                # Close the BytesIO objects
                source_io.close()
                target_io.close()
                
                # Delete processing message
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=processing_msg.message_id
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Check if the response contains image data
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        # Send the result image
                        caption = "✅ *Face Swap Completed*\n\n"
                        if not is_premium_user(user_id):
                            caption += f"💰 Remaining Credits: {get_user(user_id)['balance']}"
                        else:
                            caption += "👑 *Premium User - Unlimited Swaps*"
                        
                        await update.message.reply_photo(
                            photo=response.content,
                            caption=caption,
                            parse_mode="Markdown"
                        )
                    else:
                        # Refund credits on error if not premium
                        if not is_premium_user(user_id):
                            add_credits(user_id, credit_cost)
                        logger.error(f"Face swap API returned non-image content: {response.text[:200]}")
                        await update.message.reply_photo(
                            photo=FACE_SWAP_IMAGE,
                            caption="❌ API returned invalid response!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                        )
                else:
                    # Refund credits on error if not premium
                    if not is_premium_user(user_id):
                        add_credits(user_id, credit_cost)
                    logger.error(f"Face swap API error: {response.status_code} - {response.text[:200]}")
                    await update.message.reply_photo(
                        photo=FACE_SWAP_IMAGE,
                        caption=f"❌ API error ({response.status_code})!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                    )
            except Exception as e:
                # Refund credits on error if not premium
                if not is_premium_user(user_id):
                    add_credits(user_id, credit_cost)
                logger.error(f"Face swap error: {str(e)}")
                await update.message.reply_photo(
                    photo=FACE_SWAP_IMAGE,
                    caption="❌ Face swap failed!" + (" Credits refunded." if not is_premium_user(user_id) else "")
                )
            
            # Reset state
            if "face_swap_state" in context.user_data:
                del context.user_data["face_swap_state"]
            if "face_swap_source" in context.user_data:
                del context.user_data["face_swap_source"]
            return
    
    # Check if user is sending payment screenshot
    if context.user_data.get("pending_payment"):
        payment_id = context.user_data["pending_payment"]
        
        payment = get_payment(payment_id)
        if not payment:
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption="❌ Payment session expired!"
            )
            context.user_data["pending_payment"] = None
            return
        
        # Forward screenshot to admin with approval buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"payment_approve_{payment_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"payment_reject_{payment_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        caption = (
            f"💳 *New Payment Request*\n\n"
            f"👤 User: {update.effective_user.full_name}\n"
            f"🆔 User ID: {user_id}\n"
            f"🔗 Username: @{update.effective_user.username or 'N/A'}\n"
            f"📦 Plan: {payment['plan_type']}\n"
            f"📋 Details: {payment['plan_details']}\n"
            f"⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        try:
            # Forward the photo first
            await context.bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            
            # Then send the caption with buttons
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption="✅ Payment screenshot sent to admin! Please wait for approval."
            )
            context.user_data["pending_payment"] = None
        except Exception as e:
            logger.error(f"Error forwarding payment screenshot: {e}")
            await update.message.reply_photo(
                photo=INFO_IMAGE,
                caption="❌ Failed to send screenshot to admin. Please try again."
            )
        return
    
    # Handle broadcast with photo
    if context.user_data.get("broadcast_mode") and update.effective_user.id == ADMIN_ID:
        await process_broadcast(update, context)
        return

async def process_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process broadcast message"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    context.user_data["broadcast_mode"] = False
    users = load_users()
    success = 0
    failed = 0
    
    await update.message.reply_text(f"📢 Starting broadcast to {len(users)} users...")
    
    for user_id in users.keys():
        try:
            if update.message.photo:
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=update.message.photo.file_id,
                    caption=update.message.caption,
                    parse_mode="Markdown"
                )
            else:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=update.message.text,
                    parse_mode="Markdown"
                )
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send broadcast to {user_id}: {e}")
    
    await update.message.reply_text(
        f"✅ Broadcast completed!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}"
    )

async def process_coupon_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process coupon creation"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    context.user_data["coupon_creation"] = False
    parts = update.message.text.strip().split("|")
    
    # Check if this is a custom coupon code format
    if len(parts) == 5:
        try:
            code, reward_type, reward_value, max_uses, expiry_days = parts
            reward_value = int(reward_value)
            max_uses = int(max_uses)
            expiry_days = int(expiry_days)
            
            if create_coupon(code.upper(), reward_type, reward_value, max_uses, expiry_days):
                # Get coupon statistics
                coupon_stats = get_coupon_stats()
                
                # Calculate expiry date
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=expiry_days)
                expiry_formatted = expiry_date.strftime("%d-%m-%Y")
                
                # Send coupon details to admin in advanced format
                coupon_text = (
                    f"*🎟️ ADVANCED COUPON CREATED*\n\n"
                    f"🔑 *Coupon Code:* `{code.upper()}`\n"
                    f"🎁 *Reward Type:* {reward_type.title()}\n"
                    f"💰 *Reward Value:* {reward_value} {'credits' if reward_type == 'credits' else 'days premium'}\n"
                    f"👥 *Max Uses:* {max_uses}\n"
                    f"📅 *Expiry Date:* {expiry_formatted}\n"
                    f"📊 *Redeem Status:* 0/{max_uses} redeemed\n\n"
                    f"📈 *SYSTEM STATISTICS*\n"
                    f"🔢 *Total Coupons:* {coupon_stats['total']}\n"
                    f"✅ *Active Coupons:* {coupon_stats['active']}\n\n"
                    f"🕐 *Created At:* {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                await update.message.reply_text(coupon_text, parse_mode="Markdown")
            else:
                await update.message.reply_text("❌ Failed to create coupon!")
        except ValueError:
            await update.message.reply_text("❌ Invalid values! Please check your input.")
    else:
        await update.message.reply_text("❌ Invalid format! Please use: CODE|TYPE|VALUE|MAX_USES|EXPIRY_DAYS")

# ==========================================

# ================= ERROR HANDLING =================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ==========================================

# ================= MAIN FUNCTION =================
def main():
    """Start the bot"""
    # Create application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("addcredit", addcredit_command))
    application.add_handler(CommandHandler("removecredit", removecredit_command))
    application.add_handler(CommandHandler("addpremium", addpremium_command))
    application.add_handler(CommandHandler("removepremium", removepremium_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("maintenance", maintenance_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Add callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    print("🤖 Bme aake leave krke bot use kre to usko phir se channel join hone bole aur baki kuchot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
