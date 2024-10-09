import os
from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

# Get the absolute path to the HITS folder (assuming it's at the same level as main.py and BOT folder)
HITS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HITS'))

@Client.on_message(filters.command("open"))
async def open_file_handler(client, message):
    user_id = message.from_user.id

    # Check if the user is the owner or a premium user
    if user_id != OWNER_ID and not is_user_approved(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    # Ensure that the command is a reply to a document (txt file)
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document

        # Check if the document is a text file
        if document.mime_type == "text/plain":
            # Define the file path to save the document in the HITS folder
            file_path = os.path.join(HITS_FOLDER, document.file_name)

            # Download and read the file
            try:
                await message.reply_to_message.download(file_path)
                with open(file_path, "r") as f:
                    content = f.read()

                    # Send the content back to the user
                    if content.strip():
                        await message.reply(f"📄 **File Content**:\n\n```\n{content}\n```", quote=True)
                    else:
                        await message.reply(f"⚠️ The file `{document.file_name}` is empty.")
            except Exception as e:
                await message.reply(f"❌ Error reading file `{document.file_name}`: {str(e)}")
        else:
            await message.reply("❌ Please reply to a valid text file (.txt).")
    else:
        await message.reply("❌ Please reply to a message with a text file attached.")
