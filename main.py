import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

GAMES = {
    "GTA 5": {"cheats": ["Unlimited Money", "Weapons Unlock", "Mod Injector"], "lp": "https://gta5modss.netlify.app/"},
    "GTA 6": {"cheats": ["Vice City Mod", "Lucia Skin", "Map Enhancer"], "lp": "https://gta6-mod.netlify.app/"},
    "Fortnite": {"cheats": ["Aimbot", "ESP", "Skins Unlocked"], "lp": "https://fortnite-mod.netlify.app/"},
    "PUBG": {"cheats": ["UC Injector", "Skin Unlock", "Wall Hack"], "lp": "https://pubgg-battlefield.netlify.app/"},
    "Minecraft": {"cheats": ["Texture Unlocker", "Auto Build", "X-Ray Vision"], "lp": "https://minecraft-mod.netlify.app/"},
    "Free Fire": {"cheats": ["Diamond Generator", "Speed Hack", "Skin Injector"], "lp": "https://freefirer.netlify.app/"},
    "Roblox": {"cheats": ["Free Robux", "Fly Hack", "Unlock All Items"], "lp": "https://rbxmatrixhub.netlify.app/"},
    "Subway Surfers": {"cheats": ["Coins Injector", "Unlock All Boards", "High Score Hack"], "lp": "https://subwaysurferr.netlify.app/"},
    "Valorant": {"cheats": ["Skin Unlocker", "Aimbot", "Wall Hack"], "lp": "https://volarantt.netlify.app/"},
    "Apex Legends": {"cheats": ["Unlimited Shields", "ESP", "Wall Hack"], "lp": "https://apex-legendss.netlify.app/"},
    "COD Warzone": {"cheats": ["Aimbot", "Wall Hack", "No Recoil"], "lp": "https://warzone-cod.netlify.app/"}
}

# === /ping Server for UptimeRobot ===
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ping":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Pong")

def run_ping_server():
    server = HTTPServer(("", 10000), PingHandler)
    server.serve_forever()

# === Telegram Bot Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(game, callback_data=game)] for game in GAMES]
    await update.message.reply_text("🎮 Choose a game to unlock cheats:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    game = query.data
    cheats = GAMES[game]["cheats"]
    cheats_text = "\n".join([f"✅ {c}" for c in cheats])
    await query.edit_message_text(f"🔓 *{game}* Cheats Unlocked:\n\n{cheats_text}\n\nGenerating mod tools...", parse_mode="Markdown")
    await query.message.reply_text("👇 Tap below to access your tools:", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Open Mods", url=GAMES[game]["lp"] + f"?mod={game.replace(' ', '%20')}+Mod+Unlocker")]
    ]))

# === Start Everything ===
if __name__ == "__main__":
    threading.Thread(target=run_ping_server, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_game))
    app.run_polling(close_loop=False)
