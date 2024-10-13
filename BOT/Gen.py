import re
import io
import random
import aiohttp
from pyrogram import Client, filters, enums

# Luhn algorithm to validate a card number
def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if isSecond:
            d *= 2
        nSum += d // 10
        nSum += d % 10
        isSecond = not isSecond

    return nSum % 10 == 0


# Function to fetch BIN information
async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    bin_info_text = f"""
**BIN Lookup:**

- **BIN**: `{bin_number}`
- **Brand**: {brand}
- **Type**: {card_type}
- **Level**: {level}
- **Bank**: {bank}
- **Country**: {country} {country_flag}
"""
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"


# Luhn-based valid credit card generator with file saving
def cc_gen(cc, amount, mes='x', ano='x', cvv='x', filename="generated_cc.txt"):
    generated = 0
    ccs = []

    while generated < amount:
        # Generate random digits to append to the provided BIN
        remaining_length = 16 - len(cc)  # To complete a 16-digit card number
        card_number = cc + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length - 1)])

        # Calculate the Luhn check digit
        total_sum = 0
        reverse_digits = card_number[::-1]
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 0:
                n *= 2
                if n > 9:
                    n -= 9
            total_sum += n

        check_digit = (10 - (total_sum % 10)) % 10
        card_number += str(check_digit)

        # Format month to always be MM (two digits)
        if mes == 'x':
            mesgen = random.randint(1, 12)
            mesgen = f"{mesgen:02}"  # Ensure two-digit month format
        else:
            mesgen = f"{int(mes):02}"

        # Randomly generate or use provided year in the format YYYY
        if ano == 'x':
            anogen = random.randint(2024, 2032)
        else:
            anogen = int(ano)

        # Generate CVV in the appropriate format based on card type
        if cvv == 'x':
            if cc[0] == "3":
                cvvgen = random.randint(1000, 9999)  # 4 digits for American Express
            else:
                cvvgen = random.randint(100, 999)  # 3 digits for other cards
        else:
            cvvgen = cvv

        # Generate the final card detail string in the format CCNO|MM|YYYY|CVC
        card_detail = f"{card_number}|{mesgen}|{anogen}|{cvvgen}"
        ccs.append(card_detail)

    # Write the generated credit card details to the specified file
    with open(filename, 'w') as file:
        for card in ccs:
            file.write(card + "\n")  # Write each card on a new line

    return ccs


# Main function to handle the command and generate credit cards
async def generate_cc(client, message):
    text_parts = message.text.split()

    # Default values
    text = None
    amount = 10  # Default number of cards to generate if not specified

    # Handle different lengths of input
    if len(text_parts) == 2:
        text = text_parts[1]  # BIN only, default 10 cards
    elif len(text_parts) == 3:
        text = text_parts[1]  # BIN and specific amount of cards
        amount = int(text_parts[2]) if text_parts[2].isdigit() else 10
    else:
        await message.reply("Invalid format. Usage: `.gen BIN|MONTH|YEAR|CVV [AMOUNT]`", parse_mode=enums.ParseMode.MARKDOWN)
        return

    if amount > 30000:
        await message.reply("Amount exceeds the limit of 30,000.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    # Parse the BIN and optional month/year/CVV values
    params = re.sub('x+', 'x', text).split('|')
    if len(params[0]) < 6:
        await message.reply("Invalid BIN format.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    loading_message = await message.reply("Generating cards, please wait...", parse_mode=enums.ParseMode.MARKDOWN)
    cc = params[0].replace('x', '')
    expiration_month = params[1] if len(params) > 1 and params[1] != 'x' else 'x'
    expiration_year = params[2] if len(params) > 2 and params[2] != 'x' else 'x'
    cvv = params[3] if len(params) > 3 and params[3] != 'x' else 'x'

    # Generate the credit card numbers
    ccs = cc_gen(cc, amount, expiration_month, expiration_year, cvv, filename="generated_cc.txt")

    # Fetch BIN info
    bin_info = await bin_lookup(cc[:6])

    response_text = f"""
**Generated Credit Cards:**

{'\n'.join([f"`{cc}`" for cc in ccs])}

**BIN Info:**
{bin_info}

Generated by: [{message.from_user.first_name}](tg://user?id={message.from_user.id})
"""
    if amount <= 10:
        # Send the cards in the message itself for 10 or fewer cards
        await loading_message.delete()
        await message.reply(response_text, parse_mode=enums.ParseMode.MARKDOWN)
    else:
        # For more than 10 cards, send as a file
        try:
            with io.BytesIO(bytes('\n'.join(ccs), 'utf-8')) as out_file:
                out_file.name = f'{cc[:6]}x{amount}.txt'
                await loading_message.delete()
                await client.send_document(message.chat.id, out_file, caption=response_text, parse_mode=enums.ParseMode.MARKDOWN)
        except Exception as e:
            await loading_message.delete()
            await message.reply(f"Error: {e}", parse_mode=enums.ParseMode.MARKDOWN)


# Pyrogram command handler
@Client.on_message(filters.command(["gen", "gen"], prefixes=[".", "/"]))
async def generate_cc_command(client, message):
    await generate_cc(client, message)
