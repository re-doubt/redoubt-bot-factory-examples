#!/usr/bin/env python
import os

API_TOKEN = os.getenv('API_TOKEN')
REDOUBT_API_KEY = os.getenv('REDOUBT_API_KEY')
TG_API_URL = os.getenv('TG_API_URL')
CHAT_ID = os.getenv('CHAT_ID')
TONSCAN = os.getenv('TONSCAN')  # FIXME all links to redoubt
TIMEDELTA = int(os.getenv('TIMEDELTA'))
VOLUME_THRESHOLD = float(os.getenv('VOLUME_THRESHOLD'))
TON_THRESHOLD = int(os.getenv('TON_THRESHOLD'))
WRAPPED_TON = ['TON', 'WTON', 'pTON', 'jTON', 'wTON', 'JTON']
