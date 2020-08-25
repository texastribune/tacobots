import requests
import os

def airtable_checks(messageText):
    air_headers = {
            'Authorization': 'Bearer {}'.format(os.environ['AIRTABLE_API_KEY'])
            }
    response = requests.get('https://api.airtable.com/v0/{}/stylechecks?'.format(os.environ['AIRTABLE_BASE']), headers=air_headers).json()
    # Clean response
    potential_errors = [(record['fields']['error'], record['fields']['correction'], record['fields']['type']) for record in response['records']]
    # Convert to set of strings 
    uppercase_str = messageText
    lowercase_str = messageText.lower()

    style_errors = []
    for error in potential_errors:
        # if it is not a capitalization error, count the number of errors found using 
        # the lowercased article. Otherwise use a case sensitive approach.
        if error[2] != 'capitalization':
            n = lowercase_str.count(error[0].lower())
        else:
            n = uppercase_str.count(error[0])
        # If the error is found, record it, the correction, 
        # and the number of times it was found.
        if n > 0:
            style_errors.append('- {} *should be* {}'.format(error[0], error[1]))
    print(style_errors)
    # Combine into one string.
    if not style_errors:
        message = None
    else:
        message = "According to the <https://docs.google.com/document/d/16GVkfnrvXhv-MnLCZ6vG3Tu-bTMdnVulkZdHlHai9Zw/|StyleGuide>:\n" + "\n".join(style_errors)
    return message




def lambda_handler(data, context):
    # print logs to aws for debugging / development
    print(f"Received event:\n{data}\nWith context:\n{context}")


    SLACK_TOKEN = os.environ['SLACK_TOKEN']
    token = data.get('token')

    # exit early if slack token is wrong or missing
    if token != SLACK_TOKEN:
        return {
            'text': 'Something is wrong with the Slack token.',
            'response_type': 'ephemeral'
        }

    # Set headers for requests
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer xoxb-{}'.format(os.environ['BOT_TOKEN'])
    }  
    challenge_answer = data.get('challenge')
    # If it does, verify the request
    if 'challenge' in data:
        return {
            'statusCode': 200,
            'body': challenge_answer
        }
    # Get event
    event = data['event']
    # Check if the request contains a challenge

    if 'bot_profile' in event:
        return 0

    # Get Response Channel
    channel = event['channel']
    message = event['text']
    # If the message is a thread, get the text and thread ts.
    if 'thread_ts' in  event:
        thread = event['thread_ts']
        # message = event['blocks'][0]['elements'][0]['elements'][0]['text']
    # Otherwise get the normal test and ts
    else:
        thread = event['ts']
    
    # Create response and set the thread and channel

    parsed_message = airtable_checks(message)

    if parsed_message:
        reply_info = {
                "channel": channel,
                "thread_ts": thread,
                "text": parsed_message
        }
        # Format the reply 
        reply = '{}'.format(reply_info)
        # Post the message
        response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, data=reply)
    return 0