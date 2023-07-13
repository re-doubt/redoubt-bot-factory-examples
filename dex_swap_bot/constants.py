#!/usr/bin/env python
import os

API_TOKEN = os.getenv('API_TOKEN')
REDOUBT_API_KEY = os.getenv('REDOUBT_API_KEY')
TG_API_URL = os.getenv('TG_API_URL')
CHAT_ID = os.getenv('CHAT_ID')
TONVIEWER = os.getenv('TONVIEWER')  # FIXME all links to redoubt

WRAPPED_COINS = [ 
  'EQBPAVa6fjMigxsnHF33UQ3auufVrg2Z8lBZTY9R-isfjIFr',
  'EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv', 
  'EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez', 
  'EQCajaUU1XXSAjTD-xOV7pE49fGtg4q8kF3ELCOJtGvQFQ2C']
