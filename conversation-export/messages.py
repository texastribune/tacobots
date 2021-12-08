import os
from slack_sdk import WebClient
import json
from time import sleep
from datetime import datetime

CHANNEL = os.environ['SLACK_EXPORT_CHANNEL']
MESSAGES_PER_PAGE = 20
MAX_MESSAGES = 4000
OLDEST_DATE = '01-01-20' # mm-dd-yyyy (leading zeros)

# time formatting
def pretty_time(timestamp):
    datetime_time = datetime.fromtimestamp(int(float(timestamp)))
    return datetime_time.strftime('%-m-%-d-%y %I:%M%p')

# reference from Stack Overflow
# https://stackoverflow.com/questions/56744339/pulling-historical-channel-messages-python

# init web client
client = WebClient(token=os.environ['SLACK_EXPORT_TOKEN'])

# get replies (threads)
def add_replies(message):
    thread_ts = message.get('thread_ts')
    message['replies'] = []
    if message['type'] == 'message' and thread_ts:
        reply_page = 1
        thread_response = client.conversations_replies(
            channel=CHANNEL,
            limit=MESSAGES_PER_PAGE,
            ts=thread_ts
        )
        assert thread_response["ok"]
        # remove first one because it duplicates original message
        thread_response['messages'].pop(0)
        message['replies'] = thread_response['messages']
        while len(message['replies']) + MESSAGES_PER_PAGE <= MAX_MESSAGES and thread_response['has_more']:
            reply_page += 1
            print("Retrieving thread page {}".format(reply_page))
            sleep(1)   # need to wait 1 sec before next call due to rate limits
            thread_response = client.conversations_replies(
                channel=CHANNEL,
                limit=MESSAGES_PER_PAGE,
                cursor=thread_response['response_metadata']['next_cursor'],
                ts=thread_ts
            )
            assert thread_response["ok"]
            thread_response['messages'].pop(0)
            replies = thread_response['messages']
            message['replies'] = message['replies'] + replies
    return message


# get first page of channel messages and threaded replies
page = 1
oldest = datetime.timestamp(datetime.strptime(OLDEST_DATE, '%m-%d-%y'))
print("Retrieving page {}".format(page))
response = client.conversations_history(
    channel=CHANNEL,
    limit=MESSAGES_PER_PAGE,
    oldest=oldest
)
assert response["ok"]
messages_all = response['messages']

for message in messages_all:
    # add human readable date
    message['date'] = pretty_time(message['ts'])
    # modify the message object to include threads
    message = add_replies(message)

# get additional pages if below max message and if they are any
while len(messages_all) + MESSAGES_PER_PAGE <= MAX_MESSAGES and response['has_more']:
    page += 1
    print("Retrieving page {}".format(page))
    sleep(1)   # need to wait 1 sec before next call due to rate limits
    response = client.conversations_history(
        channel=CHANNEL,
        limit=MESSAGES_PER_PAGE,
        cursor=response['response_metadata']['next_cursor'],
        oldest=oldest
    )
    assert response["ok"]
    messages = response['messages']
    date_marker = ''
    for message in messages:
        # modify the message object to include threads
        message = add_replies(message)
        # add human readable date
        date_marker = pretty_time(message['ts'])
        message['date'] = date_marker
    print("Date complete: {}".format(date_marker))
    messages_all = messages_all + messages
print(
    "Fetched a total of {} messages from channel {}".format(
        len(messages_all),
        CHANNEL
    ))


# write the results to json
data_folder = 'src/_data/'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
with open(data_folder + 'messages.json', 'w', encoding='utf-8') as f:
    json.dump(
        messages_all,
        f,
        sort_keys=True,
        indent=4,
        ensure_ascii=False
    )


