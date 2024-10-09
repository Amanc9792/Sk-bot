async def error_log(log_message):
    try:
        with open("error_logs.txt", "a" , encoding="utf-8") as file:
            file.write(str(log_message) + "\n")
    except:
        pass

import os

async def getcards(lista):
    try:
        import re
        pattern = '(\d{15,18})[\/\s:|-]*?(\d\d)[\/\s:|-]*?(\d{2,4})[\/\s:|-]*?(\d{3,4})'
        pips    = re.findall(pattern, lista)
        return pips[0]
    except:
        return

async def getcc_for_txt(file_name, role):
    try:
        file = open(f"downloads/{file_name}").read().splitlines()
        os.remove(f"downloads/{file_name}")
        ccs = []
        for i in file:
            get  =await getcards(i)
            if get != None:
                cc     = get[0]
                mes    = get[1]
                ano    = get[2]
                cvv    = get[3]
                fullcc = f"{cc}|{mes}|{ano}|{cvv}"
                ccs.append(fullcc)
        return True, ccs
    except:
       return False , "Try Again Later"

async def getcc_for_mass(message, role):
    try:
        ccs = []
        for i in message.text.split("\n"):
            get =await  getcards(i)
            if get != None:
                cc     = get[0]
                mes    = get[1]
                ano    = get[2]
                cvv    = get[3]
                fullcc = f"{cc}|{mes}|{ano}|{cvv}"
                ccs.append(fullcc)
        return True,ccs
    except:
        return False,"Try Again Later"



import aiohttp
async def bin_lookup(cc_number):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://lookup.binlist.net/{cc_number}') as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'brand': data.get('scheme', 'Unknown'),
                        'type': data.get('type', 'Unknown'),
                        'country': data.get('country', {}).get('name', 'Unknown'),
                        'bank': data.get('bank', {}).get('name', 'Unknown'),
                        'emoji': data.get('country', {}).get('emoji', '')
                    }
    except Exception as e:
        print(f"Error during BIN lookup: {e}")
    return {}




async def getmessage(message):
    try:
        try:
            msg = message.reply_to_message.text
        except:
            msg = message.text.split(" ")[1]
        validate_msg = await getcards(msg)
        if validate_msg != None:
            return validate_msg
        else:
            return False
    except:
        return False
    


async def get_bin_details(cc,session):
    try:
        fbin = cc[:6]
        url = f"https://bins.antipublic.cc/bins/{fbin}"
        req = await session.get(url=url)
        req = req.json()
        try:
            brand = req.get("brand")
        except:
            brand = "N/A"
        try:
           type = req.get("type")
        except:
           type = "N/A"
        try:
           level = req.get("level")
        except:
            level = "N/A"
        try:
            bank = req.get("bank")
        except:
           bank = "N/A"
        try:
           country_data = req.get("country")
        except:
            country_data = "N/A"
        try:
            country = req.get("country_name")
        except:
           country = "N/A"
        try:
           flag = req.get("country_flag")
        except:
           flag = "N/A"
        try:
           currency = req.get("country_currencies")
           if not currency:
              currency = "N/A"
        except:
          currency = "N/A"

        return brand , type , level , bank , country , flag , currency
        
    except:
        return "N/A" , "N/A" , "N/A" , "N/A" , "N/A" , "N/A" , "N/A"