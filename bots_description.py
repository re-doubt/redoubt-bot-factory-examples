import glob
import json
import os

os.chdir("./")

bots = {}

for file in glob.glob("**/bot.json", recursive=True):
    bot = json.load(open(file))
    bots[bot['bot_name']] = bot

with open('bots.json', 'w') as fp:
    print(json.dumps(bots, indent=4), file=fp)
