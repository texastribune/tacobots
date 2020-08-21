import requests
import os
def lambda_handler(data, context):
    # print logs to aws for debugging / development
    print(f"Received event:\n{data}\nWith context:\n{context}")
    # Set headers for requests
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer xoxb-{}'.format(os.environ['BOT_TOKEN'])
    }  
    # Get event
    event = data['event']
    # Check if the request contains a challenge
    challenge_answer = data.get("challenge")
    # If it does, verify the request
    if challenge_answer:
        return {
            'statusCode': 200,
            'body': challenge_answer
        }

    # Get Response Channel
    channel = event['channel']
    # If the message is a thread, get the text and thread ts.
    if event["thread_ts"]:
        thread = event['thread_ts']
        message = event['blocks'][0]['elements'][0]['elements'][0]['text']
    # Otherwise get the normal test and ts
    else:
        thread = event['ts']
        message = event['text']
    # Create response and set the thread and channel
    reply_info = {
            "channel": channel,
            "thread_ts": thread,
            "text": "You said{}".format(message)
    }
    # Format the reply 
    reply = '{}'.format(reply_info)
    # Post the message
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, data=reply)
    return 0