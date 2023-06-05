#!/usr/bin/env python
import os

# FIXME remove constants before deploy

API_TOKEN = os.getenv('API_TOKEN')
REDOUBT_API_KEY = os.getenv('REDOUBT_API_KEY')
TG_API_URL = os.getenv('TG_API_URL')
CHAT_ID = os.getenv('CHAT_ID')
TONVIEWER = os.getenv('TONVIEWER')  # FIXME all links to redoubt
TONSCAN = os.getenv('TONSCAN')
TRANSFER_THRESHOLD = os.getenv('TRANSFER_THRESHOLD')

