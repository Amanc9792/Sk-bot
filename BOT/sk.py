import re
import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Get the current directory of this file (sk.py) and point to gate.py in the same folder
current_dir = os.path.dirname(os.path.abspath(__file__))
gate_file = os.path.join(current_dir, 'gate.py')

# Owner's Telegram User ID
OWNER_ID = 6492057414  # Replace this with your actual Telegram user ID

# Function to derive pk from sk (assuming pk is just sk with a replaced prefix)
def retrieve_pk_from_sk(sk):
    # Auto-derive the pk by replacing 'sk_' with 'pk_' in the sk
    if sk.startswith('sk_'):
        return sk.replace('sk_', 'pk_', 1)
    return "Invalid sk format. It should start with 'sk_'"

# Function to update sk and pk in gate.py
def update_sk_pk_in_file(new_sk):
    try:
        with open(gate_file, 'r') as file:
            content = file.read()

        new_pk = retrieve_pk_from_sk(new_sk)

        # Handle the case where the pk was invalid
        if "Invalid" in new_pk:
            return new_pk

        # Update the sk and pk arrays in the gate.py file
        content = re.sub(r"sk_array\s*=\s*\[.*\]", f"sk_array = ['{new_sk}']", content)
        content = re.sub(r"pk_array\s*=\s*\[.*\]", f"pk_array = ['{new_pk}']", content)

        with open(gate_file, 'w') as file:
            file.write(content)

        return f"Successfully updated sk to {new_sk} and pk to {new_pk}"

    except FileNotFoundError:
        return f"{gate_file} not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to view the current sk and pk
def view_sk_pk():
    try:
        with open(gate_file, 'r') as file:
            content = file.read()

        sk_match = re.search(r"sk_array\s*=\s*\['(.*)'\]", content)
        pk_match = re.search(r"pk_array\s*=\s*\['(.*)'\]", content)

        if sk_match and pk_match:
            current_sk = sk_match.group(1)
            current_pk = pk_match.group(1)
            return f"Current sk: {current_sk}\nCurrent pk: {current_pk}"
        else:
            return "Could not find sk or pk in gate.py."

    except FileNotFoundError:
        return f"{gate_file} not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Helper function to check if the user is the bot owner
def is_owner(message: Message):
    return message.from_user and message.from_user.id == OWNER_ID

# Command handler for /sk <skkey>
@Client.on_message(filters.command("sk") & filters.private)
async def update_sk_command(client, message: Message):
    if not is_owner(message):
        await message.reply("You are not authorized to use this command.")
        return

    try:
        args = message.text.split(" ")
        if len(args) < 2:
            await message.reply("Usage: /sk <new_sk>")
            return

        new_sk = args[1]
        result = update_sk_pk_in_file(new_sk)
        await message.reply(result)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Command handler for /viewsk
@Client.on_message(filters.command("viewsk") & filters.private)
async def view_sk_command(client, message: Message):
    if not is_owner(message):
        await message.reply("You are not authorized to use this command.")
        return

    try:
        result = view_sk_pk()
        await message.reply(result)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")
