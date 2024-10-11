from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    # Remove expired users before processing
    remove_expired_users()

    # Check if the user is the owner
    if user_id == OWNER_ID:
        await message.reply(
            f"👑 Welcome back, Owner {username}! You have full access to all commands.\n\n"
            "💡 Use /approve <tguserid> <no_of_days> to approve premium users."
        )
        return

    # Check if the user is a premium user
    if is_user_approved(user_id):
        await message.reply(
            f"🎉 Welcome back, Premium member {username}! 🎉\n\n"
            "You have access to all premium features. Type /cmds to see available commands!"
        )
    else:
        # Message for non-premium users
        await message.reply(
            f"👋 Hello, {username}!\n\n"
            "You currently do not have premium access. Contact @DeaDxxGod to become a premium member and unlock all features.\n\n"
            "Use /cmds to view the basic commands available to you."
        )
