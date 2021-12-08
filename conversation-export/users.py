import os
from slack_sdk import WebClient
import json
from time import sleep


CHANNEL = os.environ['SLACK_EXPORT_CHANNEL']

client = WebClient(token=os.environ['SLACK_EXPORT_TOKEN'])

# get all users in the channel
members = client.conversations_members(
    channel=CHANNEL
)
assert members["ok"]

# create a key of user ids and names
user_key = {}
count = 1
total = len(members['members'])
for member in members['members']:
    user_response = client.users_profile_get(
        user=member,
    )
    assert user_response["ok"]
    print("{} of {}".format(count, total))
    count += 1
    sleep(1)   # need to wait 1 sec before next call due to rate limits
    user_key[member] = user_response['profile']['real_name']

# write the key to json
data_folder = 'src/_data/'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
with open(data_folder + 'users.json', 'w', encoding='utf-8') as f:
    json.dump(
        user_key,
        f,
        sort_keys=True,
        indent=4,
        ensure_ascii=False
    )
print(
    "Fetched a total of {} users from channel {}".format(
        len(members['members']),
        CHANNEL
    ))
