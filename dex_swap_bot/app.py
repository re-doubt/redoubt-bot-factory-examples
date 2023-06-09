#!/usr/bin/env python

import asyncio
import requests

from loguru import logger
from redoubt_agent import RedoubtEventsStream
from constants import *

stream = RedoubtEventsStream(api_key=REDOUBT_API_KEY)

def send_message_to_telegram(message=None, api_url=TG_API_URL, chat_id=CHAT_ID, parse_mode='HTML'):
    response = requests.post(api_url + '/sendMessage',
                             json={'chat_id': chat_id, 'text': message,
                                   'parse_mode': parse_mode, 'disable_web_page_preview': True})
    logger.info(response.status_code)

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f'%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

async def handler(obj):
    logger.info(obj)

    asset_in_data = await stream.execute("""
        query jetton {
            redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                address
                symbol
                decimals
                admin_address
            }
        }
    """ % obj['data']['asset_in'])

    logger.info(asset_in_data)

    asset_out_data = await stream.execute("""
         query jetton {
             redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                 address
                 symbol
                 decimals
                 admin_address
             }
         }
     """ % obj['data']['asset_out'])

    logger.info(asset_out_data)

    jetton_in = asset_in_data['redoubt_jetton_master']
    jetton_out = asset_out_data['redoubt_jetton_master']

    # TG Message # FIXME when pool not connected to TON!!! jetton_in and jetton_out!!!
    try:
        tg_message =  f"""Platform: <a href='https://dedust.io/swap'> <b> #DeDust </b> </a>\n"""
        tg_message += f"""Pool: <a href='{TONVIEWER + obj['data']['pool']}'> {obj['data']['pool'][:2] + '..' + obj['data']['pool'][-4:]} </a>\n"""
        tg_message += f"""User: <a href='{TONVIEWER + obj['data']['swap_user']}'> {obj['data']['swap_user'][:2] + '..' + obj['data']['swap_user'][-4:]} </a>\n"""

        if jetton_in and jetton_out:
            decimals_in = jetton_in[0].get("decimals") if jetton_in[0].get("decimals") else 9
            amount_in = float(obj['data']['amount_in']) / pow(10, decimals_in)
            decimals_out = jetton_out[0].get("decimals") if jetton_out[0].get("decimals") else 9
            amount_out = float(obj['data']['amount_out']) / pow(10, decimals_out)

            tg_message += f"Trading: 🟢🔴#BUYSELL\n"
            tg_message += f"#{jetton_out[0]['symbol']}: {human_format(round(amount_out, 4))} to " \
                         f"#{jetton_in[0]['symbol']}: {human_format(round(amount_in, 4))}"

        elif jetton_in:
            decimals_in = jetton_in[0].get("decimals") if jetton_in[0].get("decimals") else 9
            amount_in = float(obj['data']['amount_in'])/pow(10, decimals_in)
            tg_message += f"Trading: 🔴#SELL\n"
            tg_message += f"""Amount: {human_format(round(amount_in, 4))} #{jetton_in[0]['symbol']} \n"""
            tg_message += f"Price: {round((float(obj['data']['amount_out'])/pow(10, 9)) / amount_in, 6)}"

        elif jetton_out:
            decimals_out = jetton_out[0].get("decimals") if jetton_out[0].get("decimals") else 9
            amount_out = float(obj['data']['amount_out']) / pow(10, decimals_out)
            tg_message += f"Trading: 🟢#BUY\n"
            tg_message += f"""Amount: {human_format(round(amount_out, 4))} #{jetton_out[0]['symbol']}\n"""
            tg_message += f"Price: {round(amount_out/(float(obj['data']['amount_in'])/pow(10, 9)), 6)}"

        # tg_message += f"Time(UTC): {obj['time']}\n"
        # tg_message += f"Source: <a href='https://www.redoubt.online'> re:doubt</a>"
        send_message_to_telegram(message=tg_message)

    except Exception as e:
        logger.warning(e)

async def run_bot():
    logger.info("Running new DEXes Swaps bot")
    await stream.subscribe(handler, scope="DEX", event_type='Swap')


if __name__ == "__main__":
    asyncio.run(run_bot())
