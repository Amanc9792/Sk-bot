from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
def start_handler(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    message.reply(
        f"""🎉 Welcome to CARD4U! 🔥
💡 Discover something exciting just for YOU, {username}!

🔮 Ready for surprises, secret features, and personalized experiences?
💥 Type /cmds to unlock the magic! 🚀

Your journey begins here. Don’t miss out! 🎁✨"""
    )from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
def start_handler(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    message.reply(
        f"""🎉 Welcome to CARD4U! 🔥
💡 Discover something exciting just for YOU, {username}!

🔮 Ready for surprises, secret features, and personalized experiences?
💥 Type /cmds to unlock the magic! 🚀

Your journey begins here. Don’t miss out! 🎁✨"""
    )