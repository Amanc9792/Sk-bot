import httpx
import time
import asyncio
from pyrogram import Client, filters

from .response import *
from .gate import *
from .fuc import *

from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

@Client.on_message(filters.command("svv", [".", "/"]))
async def svv_handler(client, message):
    user_id = message.from_user.id

    # Allow the owner and premium users to use the command
    if user_id == OWNER_ID or is_user_approved(user_id):
        # Proceed to handle the command (owner and premium users continue)
        await stripe_auth_cmd(client, message)
    else:
        # Non-premium users get a notification and cannot proceed
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return  # Exit function for non-premium users


# Async function to handle stripe authorization
async def stripe_auth_cmd(client, message):
    try:
        user_id = str(message.from_user.id)
      
        # Extract card details from the message
        getcc = await getmessage(message)
        if not getcc:
            # Respond with a format error message if card details are missing or invalid
            resp = f"""
<b>┏━Formate Not Valid ↴
Response -» Not Valid CC FOUND from Input
Formate -» /svv cc|mes|ano|cvv
Example -» /svv 4060687045104190|06|2026|009
</b>
"""
            await message.reply_text(resp)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        
        # Initial response to indicate that the check is starting
        firstresp = f"""
<b>
━━━━⌁ SK BASED 1$ ⌁━━━━

(↯) 𝗖𝗮𝗿𝗱 ⇾ {fullcc}
(↯) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ SK Based 1$
(↯) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ Checking... (0%)
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp)

        # Update with progress
        secondresp = f"""
<b>
━━━━⌁ SK BASED 1$ ⌁━━━━

(↯) 𝗖𝗮𝗿𝗱 ⇾ {fullcc}
(↯) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ SK Based 1$
(↯) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ Checking... (50%)
</b>
"""
        await asyncio.sleep(0.5)
        secondchk = await client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        # Start the performance timer
        start = time.perf_counter()

        # Create an HTTPX session for async requests
        session = httpx.AsyncClient(timeout=30)    

        # Execute main API requests to check the card
        result_1_1 = await main_svv(fullcc)
        result = await stripe_cvv_response(result_1_1, fullcc)
        print(result)  # For debugging

        # Get additional card details from BIN
        getbin = await get_bin_details(cc, session)

        status = result["status"]
        response = result["response"]

        # Final response to indicate that the check is completed
        thirdresp = f"""
<b>
━━━━⌁ SK BASED 1$ ⌁━━━━

(↯) 𝗖𝗮𝗿𝗱 ⇾ {fullcc}
(↯) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ SK Based 1$
(↯) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ Checking... (100%)
</b>
"""
        await asyncio.sleep(0.5)
        thirdcheck = await client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        # Get details from BIN lookup
        brand = getbin[0]
        type = getbin[1]
        level = getbin[2]
        bank = getbin[3]
        country = getbin[4]
        flag = getbin[5]
        currency = getbin[6]

        # Final detailed response with the result
        finalresp = f"""
<b>
━━━━⌁ SK BASED 1$ ⌁━━━━

{status}

(↯) 𝗖𝗮𝗿𝗱 ⇾ {fullcc}
(↯) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ SK Based 1$
(↯) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {response}

(↯) 𝗜𝗻𝗳𝗼 ⇾ {brand} - {type} - {level}
(↯) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛
(↯) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}

(↯) 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾ {time.perf_counter() - start:0.4f} sec
(↯) 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}
</b>
"""
        await asyncio.sleep(0.5)
        await client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)

        # Close the HTTPX session
        await session.aclose()

    except Exception as e:
        # Log any error that occurs
        import traceback
        await error_log(traceback.format_exc())
