from pyrogram import Client, filters

@Client.on_message(filters.command("help"))
def help_handler(client, message):
    message.reply(
        "ℹ️ **Help Menu**:\n\n"
        "1. Use /start to begin interacting with the bot.\n"
        "2. For premium features, please contact @DeaDxxGod to get access.\n"
        "3. Once you are a premium user, you can use /cmds to see all commands available for you.\n\n"
        "Enjoy using the bot!"
    )