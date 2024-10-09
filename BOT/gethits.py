import os
from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

# Get the absolute path to the HITS folder (assuming it's at the same level as main.py and BOT folder)
HITS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HITS'))

@Client.on_message(filters.command("gethits"))
async def gethits_handler(client, message):
    user_id = message.from_user.id
    command_text = message.text.strip()

    # Check if the user is the owner or a premium user
    if user_id != OWNER_ID and not is_user_approved(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    # Command should be like: /gethits <key>
    try:
        _, key = command_text.split(" ", 1)
    except ValueError:
        await message.reply("❌ Invalid format. Use: /gethits <key>")
        return

    # Generate the filename from the key
    file_name = f"{key}.txt"
    file_path = os.path.join(HITS_FOLDER, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            await client.send_document(message.chat.id, document=file_path, caption=f"📄 Hits file for key: {key}")
        except Exception as e:
            await message.reply(f"❌ Failed to send the hits file: {str(e)}")
    else:
        await message.reply(f"❌ File `{file_name}` not found in the HITS folder.")
