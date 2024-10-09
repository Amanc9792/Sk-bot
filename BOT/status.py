from pyrogram import Client, filters
from .approve_logic import get_user_premium_status, remove_expired_users

OWNER_ID = 6492057414

@Client.on_message(filters.command("status"))
async def status_handler(client, message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "User"

    # Remove expired users before checking
    remove_expired_users()

    # If the user is the owner, provide full access information without expiry
    if user_id == OWNER_ID:
        await message.reply(f"🎉 You are the bot owner, {username}, with full access and no expiry.")
        return

    # Check if the user is approved and send a formatted message
    premium_status = get_user_premium_status(user_id, username)
    if premium_status:
        # Send premium status message in the desired format
        await message.reply(f"""🎉✨ You are a Premium member, {username}! ✨🎉
We’re thrilled to have you in our exclusive club! 🌟

⏰ **Premium Activated On**: {premium_status['activation_date']}
⏱️ **Time of Activation**: {premium_status['activation_time']}

📅 **Your VIP Access Expires On**: {premium_status['expiry_date']}
⌛ **Expiration Time**: {premium_status['expiry_time']}

Let the adventure begin! 🛤️🚀 Enjoy all the perks of being a premium member!""")
    else:
        # If the user is not premium, inform them
        await message.reply("❌ You are not a premium user. Contact @DeaDxxGod for premium access.")
