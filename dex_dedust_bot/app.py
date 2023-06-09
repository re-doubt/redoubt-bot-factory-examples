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
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


async def handler(obj):
    logger.info(obj)

    asset_in_data = await stream.execute("""
        query asset_in {
            redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                address
                symbol
                decimals
                admin_address
            }
        }
    """ % obj['data']['asset_in'])

    asset_out_data = await stream.execute("""
         query asset_out {
             redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                 address
                 symbol
                 decimals
                 admin_address
             }
         }
     """ % obj['data']['asset_out'])

    jetton_in = asset_in_data['redoubt_jetton_master']
    jetton_out = asset_out_data['redoubt_jetton_master']

    # TG Message
    tg_message = ""
    platform = "DeDust"

    try:  # FIXME LAVE nKOTE
        if jetton_in and jetton_out:
            decimals_in = jetton_in[0].get("decimals") if jetton_in[0].get("decimals") else 9
            amount_in = float(obj['data']['amount_in']) / pow(10, decimals_in)
            decimals_out = jetton_out[0].get("decimals") if jetton_out[0].get("decimals") else 9
            amount_out = float(obj['data']['amount_out']) / pow(10, decimals_out)

            tg_message = f"🟢🔴 #{jetton_out[0]['symbol']}: {human_format(round(amount_out, 4))} to " \
                         f"#{jetton_in[0]['symbol']}: {human_format(round(amount_in, 4))} | #{platform}"
        elif jetton_in:
            decimals_in = jetton_in[0].get("decimals") if jetton_in[0].get("decimals") else 9
            amount_in = float(obj['data']['amount_in']) / pow(10, decimals_in)
            amount_out = float(obj['data']['amount_out']) / pow(10, 9)

            tg_message = f"🔴 #{jetton_in[0]['symbol']}: {human_format(round(amount_in, 4))} at " \
                         f" {round(amount_out / amount_in, 4)} | #{platform}"

        elif jetton_out:
            decimals_out = jetton_out[0].get("decimals") if jetton_out[0].get("decimals") else 9
            amount_out = float(obj['data']['amount_out']) / pow(10, decimals_out)
            amount_in = float(obj['data']['amount_in']) / pow(10, 9)

            tg_message = f"🟢 #{jetton_out[0]['symbol']}: {human_format(round(amount_out, 4))} at" \
                         f" {round(amount_in / amount_out, 4)} | #{platform}"

        if tg_message:
            send_message_to_telegram(message=tg_message)

    except Exception as e:
        logger.warning(e)


async def run_bot():
    logger.info("Running new DeDust Swaps bot")
    await stream.subscribe(handler, scope="DEX", event_type='Swap')


if __name__ == "__main__":
    asyncio.run(run_bot())
