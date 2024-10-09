from pyrogram import Client, filters

@Client.on_message(filters.command("cmds"))
async def cmds_handler(client, message):
    # This message will be available to all users, including free and premium users
    await message.reply(
        """🛠️ **Available Commands for All Users**:
    
1. /start - Start interacting with the bot.
2. /status - Check your premium status and details.
3. /cmds - Show all available commands.
4. /help - Get help and information about the bot.

🛠️ **Premium and Owner Exclusive Commands**:
5. /approve <tguserid> <noofdays> - Approve users (Owner only).
6. /svv - Single CC check.
7. /msvv - Mass CC check (Limit 30).
8. /svvtxt - CC check from a txt file.
9. /open - Open a .txt file from HITS folder.
10. /gethits <key> - Retrieve hits from a key.

Enjoy the full power of the bot! 🚀"""
    )