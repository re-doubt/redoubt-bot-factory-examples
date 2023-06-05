import json
import requests
from bs4 import BeautifulSoup


def get_nft_metadata(nft_address):
    url = f"https://tonviewer.com/{nft_address}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find(id='__NEXT_DATA__')
    nft_data = json.loads(name.text)
    return nft_data['props']['pageProps']['nftDetails']
