import time
import httpx
import threading
import asyncio
import json
from pyrogram import Client, filters
from datetime import timedelta
from .gate import *
from .response import *
from .fuc import *

from pyrogram import Client, filters
from .approve_logic import is_user_approved, remove_expired_users

OWNER_ID = 6492057414

async def get_checked_done_response(Client , message , ccs ,  key , hitsfile , start , stats , role , hits_count , chk_done):
    try:
        taken                     = str(timedelta(seconds=time.perf_counter() - start))
        hours , minutes , seconds = map(float, taken.split(":"))
        hour                      = int(hours)
        min                       = int(minutes)
        sec                       = int(seconds)
        if hits_count != 0:
            await Client.delete_messages(message.chat.id, stats.id)
            text = f"""<b>
Gates: Stripe Sk Based♻️

(↯) Total CC Input: {len(ccs)}
(↯) Hits: {hits_count} 
(↯) Dead: { chk_done - hits_count }
(↯) Total Checked: {chk_done}
(↯) Secret Key: <code>{key}</code>
(↯) Status: Checked All ✅
(↯) Checked By - <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> [ {role} ]
(↯) Credit Will Be Deducted - {len(ccs)} 
(↯) Time Taken - {hour} Hours {min} Minutes {sec} Seconds
</b>"""
            # Send the hits file if hits are found
            await message.reply_document(document = hitsfile , caption = text , reply_to_message_id = message.id)

        else:
            text = f"""<b>
Gates: Stripe Sk Based♻️

(↯) Total CC Input: {len(ccs)}
(↯) Hits: {hits_count} 
(↯) Dead: { chk_done - hits_count }
(↯) Total Checked: {chk_done}
(↯) Secret Key: <code>{key}</code>
<i>( Get Your Hits Key By "/gethits {key}" )</i>
(↯) Status: Checked All ✅
(↯) Checked By - <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> [ {role} ]
(↯) Credit Will Be Deducted - {len(ccs)} 
(↯) Time Taken - {hour} Hours {min} Minutes {sec} Seconds
</b>"""
            # If no hits, just send the response without the file
            await Client.edit_message_text(message.chat.id, stats.id, text )
    except:
        pass


async def get_checking_response(Client , message , ccs ,  key , i , start , stats , role , hits_count , chk_done):
    try:
        taken                     = str(timedelta(seconds=time.perf_counter() - start))
        hours , minutes , seconds = map(float, taken.split(":"))
        hour                      = int(hours)
        min                       = int(minutes)
        sec                       = int(seconds)
        cc                        = i["fullz"]
        response                  = i["response"]
        text = f"""<b>
Gates: Stripe Sk Based♻️

<code>{cc}</code>
(↯) Result - {response}

(↯) Total CC Input: {len(ccs)}
(↯) Hits: {hits_count} 
(↯) Dead: { chk_done - hits_count }
(↯) Total Checked: {chk_done}
(↯) Secret Key: <code>{key}</code>
<i>( Get Your Hits Key By "/gethits {key}" )</i>
(↯) Status: Checking...
(↯) Checked By - <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> [ {role} ]
(↯) Credit Will Be Deducted - {len(ccs)} 
(↯)Time Taken - {hour} Hours {min} Minutes {sec} Seconds
</b>"""
        await Client.edit_message_text(chat_id = message.chat.id , message_id = stats.id , text = text)
    except:
        pass


async def masstxtfunc(fullcc):
    result_1  = await main_svv(fullcc)
    result    = await stripe_cvv_response(result_1,fullcc)
    return result

    

async def gcgenfunc(len=4):
    import random
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(len))


async def save_cc(i, file_name):
    try:       
        cc       = i["fullz"]
        response = i["response"]
        hitsfile = f"HITS/{file_name}"
        with open(hitsfile, "a", encoding="utf-8") as f:
            f.write(f"{cc}\nResult - {response}\n")
    except:
        pass


@Client.on_message(filters.command("svvtxt", [".", "/"]))
def multi(Client, message):
    t1 = threading.Thread(target=bcall, args=(Client, message))
    t1.start()

async def svv_handler(client, message):
    user_id = message.from_user.id

    # Allow the owner and premium users to use the command
    if user_id == OWNER_ID or is_user_approved(user_id):
        # Proceed to handle the command (owner and premium users continue)
        await stripe_auth_cmd(client, message)
    else:
        # Non-premium users get a notification and cannot proceed
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")

def bcall(Client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stripe_mass_txt_auth_cmd(Client, message))
    loop.close()


async def stripe_mass_txt_auth_cmd(Client, message):
    try:
        user_id    = str(message.from_user.id)
        first_name = str(message.from_user.first_name)
        
        role = 'Premium'
        try:
            random_text = await gcgenfunc(len=8)
            key         = f"masstxt_{message.from_user.id}_{random_text}"
            file_name   = f"{key}.txt"
            hitsfile    = f"HITS/{file_name}"
            await message.reply_to_message.download(file_name=file_name)
        except:
            resp = """<b>
Gate Name: Mass Stripe Auth ♻️
CMD: /masstxt

Message: No CC Found in your input ❌

Usage: /masstxt [ in reply to txt file ]
        </b> """
            await message.reply_text(resp, message.id)
            return

        getcc = await getcc_for_txt(file_name, role)
        if getcc[0] == False:
            await message.reply_text(getcc[1], message.id)
            return
        

        ccs  = getcc[1]
    

#         text = f"""<b>
# Gate : Mass Stripe Auth ♻️

# (↯) CC Amount : {len(ccs)}
# (↯) Message : Checking CC For {first_name}
# Note: This Pop Up Will Change After 50 CC Checked . So Keep Patient . 

# (↯) Status : Processing...⌛️

# (↯) Checked By <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> [ {role} ] 
# (↯) Bot by - <a href=\"tg://user?id=6492057414\">[ヤ] Not Your Type </a>
#     </b> """
        stats = await message.reply_text("processing ur card", message.id)
      

        chk_done     = 0
        hits_count   = 0
        start        = time.perf_counter()
        session      = httpx.AsyncClient(timeout = 30)
        works        = [masstxtfunc(i) for i in ccs]
        worker_num   = 30

        while works:
            a = works[:worker_num]
            a = await asyncio.gather(*a)
            for i in a:
                chk_done += 1
                
                if i["hits"] == "YES":
                    hits_count += 1
                    await save_cc(i, file_name)

                if chk_done % 50 == 0:
                    await get_checking_response(Client , message , ccs ,  key , i , start , stats , role , hits_count , chk_done)

            works = works[worker_num:]

        await session.aclose()

        await get_checked_done_response(Client , message , ccs ,  key , hitsfile , start , stats , role , hits_count , chk_done)

    except:
        import traceback
        await error_log(traceback.format_exc())
