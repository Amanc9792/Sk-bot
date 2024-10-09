import time
import threading
import asyncio
from pyrogram import Client, filters
from datetime import timedelta
from .gate import *
from .response import *
from .fuc import *

from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

# This function starts a new thread to handle the command
@Client.on_message(filters.command("msvv", [".", "/"]))
def multi(Client, message):
    # Run the `bcall` function in a new thread
    t1 = threading.Thread(target=bcall, args=(Client, message))
    t1.start()

# Thread target function, uses asyncio to manage the command execution
def bcall(Client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stripe_mass_auth_cmd(Client, message))
    loop.close()

# The main function that checks if the user is approved or the owner and continues with the full process
async def stripe_mass_auth_cmd(Client, message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name

        # Check if the user is the owner or a premium user
        if user_id != OWNER_ID and not is_user_approved(user_id):
            # Notify only non-premium users that they don't have access
            await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
            return

        # If the user is allowed (owner or premium), proceed with the full process
        role = 'FREE' if user_id != OWNER_ID else 'OWNER'
        getcc = await getcc_for_mass(message, role)
        if not getcc[0]:
            await message.reply_text(getcc[1], message.id)
            return

        # Continue processing for owner or premium users
        ccs = getcc[1]
        resp = f"""<b>
━⌁ MASS SK BASED 1$ ⌁━━
CC Amount : {len(ccs)}
Message : Checking CC For {first_name}
Status : Processing...⌛️
Checked By <a href="tg://user?id={message.from_user.id}"> {first_name}</a> [ {role} ]
        </b>"""
        nov = await message.reply_text(resp, message.id)

        text = f"""━⌁ MASS SK BASED 1$ ⌁━━\n\n"""
        amt = 0
        start = time.perf_counter()
        works = [mchkfunc(i) for i in ccs]
        worker_num = 30

        # Process credit cards in batches
        while works:
            a = works[:worker_num]
            a = await asyncio.gather(*a)
            for i in a:
                amt += 1
                text += f"(↯)  {ccs[amt - 1]}\n{i}\n\n"
                if amt % 5 == 0:
                    try:
                        await Client.edit_message_text(message.chat.id, nov.id, text)
                    except:
                        pass
            await asyncio.sleep(1)
            works = works[worker_num:]

        taken = str(timedelta(seconds=time.perf_counter() - start))
        hours, minutes, seconds = map(float, taken.split(":"))
        hour = int(hours)
        min = int(minutes)
        sec = int(seconds)

        # Final response with summary
        text += f"""
◈━━━━━━━━━━━━━━━━━━◈
🝂 [ CHECK INFO ]
🝂  Total CC Checked - {len(ccs)}
🝂  Credit Deducted - {len(ccs)}
🝂  Time Taken - {hour} Hours {min} Minutes {sec} Seconds
🝂  Checked by: <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a>
"""
        await Client.edit_message_text(message.chat.id, nov.id, text)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())

# Async function to check credit cards
async def mchkfunc(fullcc):
    try:  
        getresp_1 = await main_svv(fullcc) 
        getresp = await stripe_cvv_response(getresp_1, fullcc)
        response = getresp["response"]
        
        return f"<code>{fullcc}</code>\n<b>Result - {response}</b>\n"

    except:
        import traceback
        await error_log(traceback.format_exc())
        return f"<code>{fullcc}</code>\n<b>Result - Card Declined 🚫</b>\n"