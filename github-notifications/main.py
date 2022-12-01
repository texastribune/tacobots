import os
import functions_framework
from slack import WebClient
from slack.errors import SlackApiError

import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

@functions_framework.http
@app.route('/', methods=['POST'])
def process_request(request):
    webhook_payload = request.get_json()
    webhook_payload_list = list(webhook_payload)  
    return_status = "Incomplete"

    # Check if event caused by dependabot
    sender = webhook_payload["sender"]["login"]
    if sender == "dependabot[bot]":
        return_status = "Complete"
        return return_status

    if "ref_type" in webhook_payload:
        if webhook_payload["ref_type"] == "branch":
            return_status = create_branch(webhook_payload)
    
    # if webhook_payload_list[1] == "ref_type":
    # elif webhook_payload_list[2] == "pull_request":
    if "pull_request" in webhook_payload:
        return_status = pull_request(webhook_payload)
    else:
        print("Key doesn't exist in JSON data")
        
    if return_status == None:
        return_status = "Incomplete bc Null"
    return return_status

def create_branch(payload):
    description = get_description(payload, "repository", "description")
    sender = payload["sender"]["login"]
    repository = payload["repository"]["full_name"]
    url = payload["repository"]["html_url"] + "/branches"
    text = ":tree-branch: Branch created"
    return_status = write_message(text,"Branch ", url, repository, description, sender)
    return return_status

def pull_request(payload):
    sender = payload["sender"]["login"]
    pr_url = payload["pull_request"]['html_url']
    repository = payload["repository"]["full_name"]
    text = ":pusheencomputer: Pull Request " + payload["action"]
    repository = payload["repository"]["full_name"]
    description = get_description(payload, "pull_request", "title")
    return_status = write_message(text,"Pull Request", pr_url, repository, description, sender)
    return return_status

def get_description(payload, index1, index2):
    description = " "
    if payload[index1][index2] != None:
        description = payload[index1][index2]
    return description

def write_message(text, type, url, repo, description, user): 
    # slack_token = os.environ["SLACK_API_TOKEN"]
    slack_token = os.getenv('SLACK_API_TOKEN')
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