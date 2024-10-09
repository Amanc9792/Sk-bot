from pyrogram import Client, filters
import re
from .approve_logic import approve_user, remove_expired_users

OWNER_ID = 6492057414

# Helper function to convert '3d', '2w', '1m' to days
def parse_duration(duration):
    match = re.match(r"(\d+)([dwm])", duration)
    if not match:
        return None

    value, unit = match.groups()
    value = int(value)

    if unit == 'd':
        return value
    elif unit == 'w':
        return value * 7
    elif unit == 'm':
        return value * 30
    else:
        return None

@Client.on_message(filters.command("approve"))
async def approve_handler(client, message):
    user_id = message.from_user.id
    command_args = message.text.split()

    # Only the owner can approve users
    if user_id != OWNER_ID:
        await message.reply("🚫 You do not have permission to approve users.")
        return

    # Ensure there are two arguments: /approve <user_id> <duration>
    if len(command_args) != 3:
        await message.reply("❌ Invalid format. Use: /approve <telegram user id> <duration (e.g., 3d, 2w, 1m)>")
        return

    try:
        tguserid = int(command_args[1])
    except ValueError:
        await message.reply("❌ Invalid user ID. User ID must be an integer.")
        return

    # Parse the duration
    duration = command_args[2]
    no_of_days = parse_duration(duration)

    if no_of_days is None:
        await message.reply("❌ Invalid duration format. Use: 3d (days), 2w (weeks), 1m (months).")
        return

    result = approve_user(tguserid, no_of_days, OWNER_ID)

    # Send a message to the approved user confirming their approval
    await client.send_message(
        tguserid, 
        f"""🎉✨ Welcome to the Premium Experience, {tguserid}! ✨🎉
We’re thrilled to have you join our exclusive club! 🌟

⏰ Premium Activated On: {result['activation_date']}
⏱️ Time of Activation: {result['activation_time']}

📅 Your VIP Access Expires On: {result['expiry_date']}
⌛ Expiration Time: {result['expiry_time']}

Let the adventure begin! 🛤️🚀 Enjoy all the perks of being a premium member!"""
    )

    # Send a confirmation message to the owner
    await message.reply(f"✅ User {tguserid} approved for {no_of_days} days.")
