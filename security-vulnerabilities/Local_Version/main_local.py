from airtable import airtable
import json
import os
import requests
import dependabot_payloads
from slack import WebClient
from slack.errors import SlackApiError

# print(at.get('table1'))
def main(request): 
    payload = json.loads(request, strict=False)

    severity = payload['alert']['security_advisory']['severity']
    if severity == "medium" or severity == "low" or payload["action"] != "created":
        return
    
    description = " "
    if payload['alert']['security_advisory']['summary'] != None:
        description = payload['alert']['security_advisory']['summary']

    sender = payload["sender"]["login"]
    repository = payload["repository"]["full_name"]
    alert_url = payload['alert']['html_url']
    text = ":rotating_light: " + severity.title() + " level security alert "

    pr_url = payload['alert']['html_url'] + "/pulls" + str(payload['alert']['number'])
    task = payload['alert']['security_advisory']['summary']
    summary = "Vulnerability: " + alert_url + "\n\nRelated PR: " + pr_url + "\n\nWhat to test after upgrading: " 
    notes = payload['alert']['security_advisory']['description']
    
    print(create_record_airtable(task, summary, notes))
    return_status = write_slack_message(text,"Alert ", alert_url, repository, description, sender)
    return return_status 

def write_slack_message(text, type, url, repo, description, user): 
    slack_token = os.environ["SLACK_API_TOKEN"]
    client = WebClient(token=slack_token)
    return_status = "Incomplete"
    
    try:
        response = client.chat_postMessage(
                channel="#tech-test",
                blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text + " on " + repo + "."
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View " + type + "!"
                            # "emoji": true
                        },
                        "value": "click_me_123",
                        "url": url,
                        "action_id": "button-action"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": description + " - " + user
                        }
                    ]
                }
                ]
            )
        return_status = "Complete"
    except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    return return_status

def create_record_airtable(task, summary, notes):
    AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
    AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
    AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}"

    data = {
        "records": [
            {
        "fields": {
        "Task": task,
        "Summary": summary,
        "Status": "Todo",
        "Notes": notes,
        "Project": [
            "reckipR9m0M37Wx8b"
        ],
        "Type": [
            "Security"
        ]
        }
    },
        ]
    }

    url = f"{AIRTABLE_URL}/table1"
    headers = {
      'Authorization': f'Bearer {AIRTABLE_TOKEN}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(data))

    return response 

print(main(dependabot_payloads.high_level_alert))


