#!/usr/bin/env python

import asyncio
import requests

from gql import gql
from loguru import logger
from redoubt_agent import RedoubtEventsStream
from datetime import datetime, timezone, timedelta
from constants import *


def send_message_to_telegram(message=None, api_url=TG_API_URL, chat_id=CHAT_ID, parse_mode='HTML'):
    response = requests.post(api_url + '/sendMessage',
                             json={'chat_id': chat_id, 'text': message,
                                   'parse_mode': parse_mode, 'disable_web_page_preview': True})
    logger.info(response.status_code)


class JettonTransfersBot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stream = RedoubtEventsStream(self.api_key)
        self.jetton_market_data = {}

    async def handler(self, obj, session):
        now = datetime.now().astimezone(timezone.utc)
        market_data = {}

        # Jetton blockchain address
        jetton_address = obj['data']['master']

        # Jetton symbol and decimals
        jetton_data = await session.execute(gql("""
            query jetton {
                redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                    address
                    symbol
                    decimals
                    admin_address
                }
            }
        """ % jetton_address))

        if len(jetton_data['redoubt_jetton_master']) == 0:
            logger.info("Jetton master info not found")

        jetton = jetton_data['redoubt_jetton_master'][0]
        decimals = jetton.get("decimals", 9) if jetton.get("decimals", 9) else 9

        logger.info(jetton_data)

        # Jetton Market Data
        if not jetton_address in self.jetton_market_data.keys() or self.jetton_market_data[jetton_address][
            'time'] < now - timedelta(TIMEDELTA):
            market_data = await session.execute(gql("""
            query jetton {
                redoubt_jettons_market_data(
                      where: {address: {_eq: "%s"}},
                      order_by: {build_time: desc},
                      limit: 1
                    ) {
                        address
                        symbol
                        price
                        market_volume_ton
                    }
                }
                """ % jetton_address))

            # Check is traded Jetton
            if market_data['redoubt_jettons_market_data']:
                self.jetton_market_data[jetton_address] = {'time': now,
                                                           'price': market_data['redoubt_jettons_market_data'][0][
                                                               'price'],
                                                           'volume': market_data['redoubt_jettons_market_data'][0][
                                                               'market_volume_ton']}

        jetton_amount = round(float(obj['data']['amount']) / pow(10, decimals), 6)

        logger.info(f"{obj['data']['source_owner']} => {obj['data']['destination_owner']} "
                    f"{jetton_amount} {jetton['symbol']}")

        if market_data and 'redoubt_jettons_market_data' in market_data.keys():
            # To avoid TG Exceptions or missed Jettons just wrap
            try:
                jetton_amount_ton = round(jetton_amount * self.jetton_market_data[jetton_address]['price'], 3)
                send = False
                tg_message = ""

                if jetton_amount_ton >= self.jetton_market_data[jetton_address]['volume'] * VOLUME_THRESHOLD:
                    tg_message = f"<b>Alert:</b> Transfer more than {VOLUME_THRESHOLD * 100}% than daily market " \
                                 f"volume " \
                                 f"[{self.jetton_market_data[jetton_address]['volume']} TON]" \
                                 f".\n"
                    send = True
                elif jetton_amount_ton >= TON_THRESHOLD:
                    tg_message = f"Alert: Transfer more than {TON_THRESHOLD} TON.\n"
                    send = True

                # TG Message
                # FIXME move WRAPPED_TON condition to the start to avoid extra calculations
                if send and jetton['symbol'] not in WRAPPED_TON:
                    tg_message += f"""From: <a href='{TONSCAN + obj['data']['source_owner']}'
                                    >{obj['data']['source_owner']}</a>\n"""
                    tg_message += f"""To: <a href='{TONSCAN + obj['data']['destination_owner']}'
                                    >{obj['data']['destination_owner']}</a>\n"""
                    tg_message += f"Amount: {jetton_amount} {jetton['symbol']} [" \
                                  f"{jetton_amount_ton} TON]\n"
                    tg_message += f"Jetton: #{jetton['symbol']}\n"
                    # tg_message += f"Time(UTC): {obj['time']}\n"
                    # tg_message += f"Source: <a href='https://www.redoubt.online'> re:doubt</a>"

                    send_message_to_telegram(message=tg_message)

            except Exception as e:
                logger.warning(e)

        logger.info(self.jetton_market_data)

    async def run_bot(self):
        logger.info("Running jetton transfer bot")
        await self.stream.subscribe(self.handler, scope="Jetton", event_type='Transfer')


if __name__ == "__main__":
    bot = JettonTransfersBot(api_key=REDOUBT_API_KEY)  # FIXME Remove, use env
    asyncio.run(bot.run_bot())

