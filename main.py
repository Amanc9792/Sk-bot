from pyrogram import Client
import os

# Your Telegram Bot API Token
api_id = "21160213"
api_hash = "3947b8737fd71b5c58edc1da33bd0e87"
bot_token = "7557279006:AAEAF7eeteCTci5EXmimE1MiHTdmi7hpAT8"

# Initialize Pyrogram Client and load plugins from the BOT folder
bot = Client(
    "MY_BOT",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=dict(root="BOT")  # Plugins will be loaded from the BOT folder
)

if __name__ == "__main__":
    print("Bot is starting...")
    bot.run()
