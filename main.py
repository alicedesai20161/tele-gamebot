import os
import threading
import asyncio
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Game Config with Landing Page URLs
GAMES = {
    "GTA 5": {
        "cheats": ["Unlimited Money", "Weapons Unlock", "Mod Injector"],
        "lp": "https://gta5modss.netlify.app/"
    },
    "GTA 6": {
        "cheats": ["Vice City Mod", "Lucia Skin", "Map Enhancer"],
        "lp": "https://gta6-mod.netlify.app/"
    },
    "Fortnite": {
        "cheats": ["Aimbot", "ESP", "Skins Unlocked"],
        "lp": "https://fortnite-mod.netlify.app/"
    },
    "PUBG": {
        "cheats": ["UC Injector", "Skin Unlock", "Wall Hack"],
        "lp": "https://pubgg-battlefield.netlify.app/"
    },
    "Minecraft": {
        "cheats": ["Texture Unlocker", "Auto Build", "X-Ray Vision"],
        "lp": "https://minecraft-mod.netlify.app/"
    },
    "Free Fire": {
        "cheats": ["Diamond Generator", "Speed Hack", "Skin Injector"],
        "lp": "https://freefirer.netlify.app/"
    },
    "Roblox": {
        "cheats": ["Free Robux", "Fly Hack", "Unlock All Items"],
        "lp": "https://rbxmatrixhub.netlify.app/"
    },
    "Subway Surfers": {
        "cheats": ["Coins Injector", "Unlock All Boards", "High Score Hack"],
        "lp": "https://subwaysurferr.netlify.app/"
    },
    "Valorant": {
        "cheats": ["Skin Unlocker", "Aimbot", "Wall Hack"],
        "lp": "https://volarantt.netlify.app/"
    },
    "Apex Legends": {
        "cheats": ["Unlimited Shields", "ESP", "Wall Hack"],
        "lp": "https://apex-legendss.netlify.app/"
    },
    "COD Warzone": {
        "cheats": ["Aimbot", "Wall Hack", "No Recoil"],
        "lp": "https://warzone-cod.netlify.app/"
    },
}

MOD_MESSAGES = {
    "GTA 5": "Injecting Rockstar DLC Unlocker...",
    "GTA 6": "Modding Lucia's adventure...",
    "Fortnite": "Injecting pro aim assists...",
    "PUBG": "Configuring UC Generator Engine...",
    "Minecraft": "Installing RTX Texture Engine...",
    "Free Fire": "Unlocking elite bundles...",
    "Roblox": "Activating Robux bypass script...",
    "Subway Surfers": "Boosting high score matrix...",
    "Valorant": "Injecting skins into Riot server...",
    "Apex Legends": "Tapping unlimited shields...",
    "COD Warzone": "Hacking recoil module..."
}

# === /ping Server for Uptime Monitoring ===
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ping":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Pong")

def run_ping_server():
    server = HTTPServer(("", 10000), PingHandler)
    server.serve_forever()

# === Bot Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"🎮 {g}", callback_data=g)] for g in GAMES]
    await update.message.reply_text(
        "🔥 *Choose your game to unlock mods:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    game = query.data
    cheats = GAMES[game]["cheats"]
    lp_url = GAMES[game]["lp"]
    mod_message = MOD_MESSAGES[game]
    cheats_text = "\n".join([f"🔓 {c}" for c in cheats])

    await query.edit_message_text(
        f"*{game} Mods Detected:*\n{cheats_text}\n\n💉 {mod_message}",
        parse_mode="Markdown"
    )

    # Animated fake modding steps with dots
    fake_process = [
        "🔌 Connecting to game server",
        "🔐 Overriding permissions",
        "📁 Unlocking game resources",
        "⚙️ Generating mod files",
        "✅ Finalizing injection"
    ]
    for step in fake_process:
        msg: Message = await query.message.reply_text(f"{step}.")
        for dots in ["..", "...", ""]:
            await asyncio.sleep(0.5)
            await msg.edit_text(f"{step}{dots}")

    # Fake progress bar
    progress_stages = [
        "[▒▒▒▒▒▒▒▒▒▒] 0%",
        "[██▒▒▒▒▒▒▒▒] 20%",
        "[████▒▒▒▒▒▒] 40%",
        "[██████▒▒▒▒] 60%",
        "[████████▒▒] 80%",
        "[██████████] 100%"
    ]
    msg: Message = await query.message.reply_text("🚀 Progress:\n" + progress_stages[0])
    for stage in progress_stages[1:]:
        await asyncio.sleep(1)
        await msg.edit_text("🚀 Progress:\n" + stage)

    # Final Mod Unlock Button
    await asyncio.sleep(1)
    mod_link = f"{lp_url}?mod={game.replace(' ', '+')}+Mod+Unlocker"
    await query.message.reply_text(
        f"✅ *{game} Mod Unlocked!*\nTap below to open:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Open Mods", url=mod_link)]
        ])
    )

# === Main App ===
if __name__ == "__main__":
    threading.Thread(target=run_ping_server, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_game))
    app.run_polling(close_loop=False)
