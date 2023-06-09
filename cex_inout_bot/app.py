#!/usr/bin/env python

import asyncio
import json
import requests

from loguru import logger
from redoubt_agent import RedoubtEventsStream
from constants import *

with open('cex_address_mapping.json') as f:
    cex_address = json.load(f)


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

    if obj['data']['amount'] >= TRANSFER_THRESHOLD:

        publish = False

        if obj['data']['source'] in cex_address.keys():
            source = cex_address[obj['data']['source']]
            publish = True
        else:
            source = obj['data']['source'][:2]+ '..' +obj['data']['source'][-4:]

        if obj['data']['destination'] in cex_address.keys():
            destination = cex_address[obj['data']['destination']]
            publish = True
        else:
            destination = obj['data']['destination'][:2] + '..' + obj['data']['destination'][-4:]

        if publish:
            tg_message = f"<b>Source:</b> <a href='{TONVIEWER + obj['data']['source']}'> {source}</a>   "
            tg_message += f"<b>Destination:</b> <a href='{TONVIEWER + obj['data']['destination']}'> {destination}</a>\n"
            tg_message += f"<b>Amount:</b> {human_format(obj['data']['amount'])} "
            tg_message += f"(<a href='{TONSCAN + obj['data']['msg_hash']}'> View on TONScan</a>)"
            send_message_to_telegram(message=tg_message)

async def run_bot():
    logger.info("Running new CEX Funding bot")
    stream = RedoubtEventsStream(api_key=REDOUBT_API_KEY)  # FIXME - use env
    await stream.subscribe(handler, scope="TON", event_type='Transfer')


if __name__ == "__main__":
    asyncio.run(run_bot())
