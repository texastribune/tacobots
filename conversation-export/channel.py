import os
from slack_sdk import WebClient
import json


CHANNEL = os.environ['SLACK_EXPORT_CHANNEL']

client = WebClient(token=os.environ['SLACK_EXPORT_TOKEN'])

# get channel information
channel_info = client.conversations_info(
    channel=CHANNEL
)
assert channel_info["ok"]

# write the channel info to json
data_folder = 'src/_data/'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
with open(data_folder + 'channel.json', 'w', encoding='utf-8') as f:
    json.dump(
        channel_info['channel'],
        f,
        sort_keys=True,
        indent=4,
        ensure_ascii=False
    )
print("Fetched info for {}".format(CHANNEL))
