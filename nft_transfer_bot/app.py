#!/usr/bin/env python

import asyncio
import io
import json
import requests

from loguru import logger
from redoubt_agent import RedoubtEventsStream
from constants import *
from scrape_metadata import get_nft_metadata

with open('address_labels.json') as f:
    tracking_address = json.load(f)


def send_photo_to_telegram(caption, img_url, api_url=TG_API_URL, chat_id=CHAT_ID):
    remote_image = requests.get(img_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    response = requests.post(api_url + '/sendPhoto', {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML',
                                                      'disable_web_page_preview': True},
                             files={'photo': photo})
    return response.status_code


class NFTSalesBot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stream = RedoubtEventsStream(self.api_key)

    async def handler(self, obj, session):

        logger.info(obj)

        if obj['data']['marketplace'] in tracking_address.keys():
            marketplace = tracking_address[obj['data']['marketplace']]
        else:
            marketplace = obj['data']['marketplace'][:2] + '..' + obj['data']['marketplace'][-4:]

        nft_marketplace_link = f"<a href='{TONVIEWER + obj['data']['marketplace']}'>{marketplace}</a>"

        if obj['data']['previous_owner'] is not None:
            previous_owner = obj['data']['previous_owner'][:2] + '..' + obj['data']['previous_owner'][-4:]
            previous_owner_link = f"<a href='{TONVIEWER + obj['data']['previous_owner']}'>{previous_owner}</a>"
        else:
            previous_owner_link = "<b> Ghost </b>"

        new_owner = obj['data']['new_owner'][:2] + '..' + obj['data']['new_owner'][-4:]
        new_owner_link = f"<a href='{TONVIEWER + obj['data']['new_owner']}'>{new_owner}</a>"

        # NFT metadata
        nft_item_address = obj['data']['nft_item']
        nft_metadata = get_nft_metadata(nft_item_address)

        # logger.info(nft_metadata)

        if obj['data']['collection'] in tracking_address.keys():
            nft_collection = tracking_address[obj['data']['collection']]
        else:
            nft_collection = nft_metadata['collection']['name']
        nft_collection_link = f"<a href='{GETGEMS + 'collection/' + obj['data']['collection']}'>{nft_collection}</a>"
        nft_name = nft_metadata['metadata']['name']
        nft_item_link = f"<a href='{GETGEMS + 'nft/' + obj['data']['nft_item']}'>{nft_name}</a>"
        nft_image = nft_metadata['metadata']['image']

        # TG Message
        tg_message = f"{previous_owner_link} sold NFT {nft_item_link} from collection {nft_collection_link} " \
                     f"to {new_owner_link} through {nft_marketplace_link} for {obj['data']['price']} TON."
        send_photo_to_telegram(caption=tg_message, img_url=nft_image)

    async def run_bot(self):
        logger.info("Running NFT sales bot")
        await self.stream.subscribe(self.handler, scope="NFT", event_type='Sale')


if __name__ == "__main__":
    bot = NFTSalesBot(api_key=REDOUBT_API_KEY)  # FIXME Remove, use env
    asyncio.run(bot.run_bot())
