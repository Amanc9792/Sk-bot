import aiohttp
import random

sk_array = ['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']
pk_array = ['pk_live_51H7oosHIrwomVcexknp1XxS0WEUO6Onx1fqgnEGK4sHOunRX7Od7e7SvlbUQWsqG3ZDid3abGPLyHOT4PsTSlcSe00SrgvLqBc']

sk = random.choice(sk_array)
pk = random.choice(pk_array)

async def create_payment_method(cc, mes, ano, cvv,session):
    data = {
        'type': 'card',
        'card[number]': cc,
        'card[exp_month]': mes,
        'card[exp_year]': ano,
        'card[cvc]': cvv
    }
    try:
        response =await session.post('https://api.stripe.com/v1/payment_methods', data=data, auth=(pk, ''))
        if response.status_code == 200:
            return response.json().get('id')
    except Exception as e:
        return f'Error creating payment method for {cc}: {e}'
    return None

async def create_payment_intent(payment_method, amount,session):
    data = {
        'amount': amount * 100,
        'currency': 'usd',
        'payment_method_types[]': 'card',
        'description': 'Test Donation',
        'payment_method': payment_method,
        'confirm': 'true',
        'off_session': 'true'
    }
    response = await session.post('https://api.stripe.com/v1/payment_intents', data=data, auth=(sk, ''))
    return response.text
import httpx
async def main_svv(i):
    async with httpx.AsyncClient()as session:
        print(i)
        cc,mes,ano,cvv= i.split('|')
        resp = await  create_payment_method(cc, mes, ano, cvv,session)
        getres_result = await create_payment_intent(resp, 1,session)
        return getres_result
