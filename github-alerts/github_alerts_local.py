import webhook_payloads
import json
import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

def main(request):
    webhook_payload = json.loads(request)
    webhook_payload_list = list(webhook_payload)  

    # Check if dependabot security alert
    if webhook_payload_list[1] == "alert":
        dependabot_alert(webhook_payload)

    # Check if event caused by dependabot
    sender = webhook_payload["sender"]["login"]
    if sender == "dependabot[bot]":
        return      

    if webhook_payload_list[1] == "ref_type":
        create_branch(webhook_payload)
    elif webhook_payload_list[1] == "comment":
        comments(webhook_payload)
    elif webhook_payload_list[1] == "deployment":
        deployment(webhook_payload)
    elif webhook_payload_list[1] == "issue":
        issues(webhook_payload)
    elif webhook_payload_list[1] == "review":
        pull_request_review(webhook_payload)
    elif webhook_payload_list[2] == "pull_request":
        pull_request(webhook_payload)
    elif webhook_payload_list[1] == "release":
        release(webhook_payload)
    else:
        print("Key doesn't exist in JSON data")
        return

def create_branch(payload):
    description = get_description(payload, "repository", "description")
    sender = payload["sender"]["login"]
    if payload["ref_type"] == "branch": 
        repository = payload["repository"]["full_name"]
        url = payload["repository"]["html_url"] + "/branches"
        text = "Branch created"
        type = "Branch"
    if payload["ref_type"] == "tag": 
        repository = payload["repository"]["full_name"]
        url = payload["repository"]["html_url"] + "/tags"
        text = "Tag created"
        type = "Tag"
    else:
        return
    write_message(text,type, url, repository, description, sender)

def comments(payload):
    sender = payload["sender"]["login"]
    description = get_description(payload, "comment", "body")
    comment_url = payload["comment"]["html_url"]
    repository = payload["repository"]["full_name"]
    text = "Comment " + payload["action"]
    write_message(text,"Comment ", comment_url, repository, description, sender)

def deployment(payload):
    sender = payload["sender"]["login"]
    deployment_url = payload["repository"]["html_url"] + "/deployments"
    repository = payload["repository"]["full_name"]
    text = "Deployment " + payload["action"]
    description = get_description(payload, "repository", "description")
    write_message(text,"Deployment", deployment_url, repository, description, sender)

def issues(payload):
    sender = payload["sender"]["login"]
    issues_url = payload["issue"]['html_url']
    text = "Issue " + payload["action"]
    repository = payload["repository"]["full_name"]
    # issue_description = payload["issue"]['body']
    description = get_description(payload, "issue", "title")
    write_message(text,"Issue", issues_url, repository, description, sender)

def pull_request(payload):
    sender = payload["sender"]["login"]
    pr_url = payload["pull_request"]['html_url']
    repository = payload["repository"]["full_name"]
    text = "Pull Request " + payload["action"]
    repository = payload["repository"]["full_name"]
    # title = payload["pull_request"]["title"]
    description = get_description(payload, "pull_request", "title")
    write_message(text,"Pull Request", pr_url, repository, description, sender)

def pull_request_review(payload):
    sender = payload["sender"]["login"]
    pr_review_url = payload["review"]['html_url']
    repository = payload["repository"]["full_name"]
    # title = payload["repository"]["title"]
    text = "Pull Request Review " + payload["action"]
    description = get_description(payload, "pull_request", "body")
    write_message(text,"Pull Request Review ", pr_review_url, repository, description, sender)

def release(payload):
    sender = payload["sender"]["login"]
    text = "Release " + payload["action"]
    release_url = payload['release']['html_url']
    repository = payload["repository"]["full_name"]
    description = get_description(payload, "release", "tag_name")
    write_message(text,"Release ", release_url, repository, description, sender)

def dependabot_alert(payload):
    severity = payload['alert']['security_advisory']['severity']
    if severity == "medium" or severity == "low":
        return
    sender = payload["sender"]["login"]
    repository = payload["repository"]["full_name"]
    alert_url = payload['alert']['html_url']
    description = " "
    if payload['alert']['security_advisory']['summary'] != None:
        description = payload['alert']['security_advisory']['summary']
    text = severity.title() + " level security alert "
    write_message(text,"Alert ", alert_url, repository, description, sender)

def get_description(payload, index1, index2):
    description = " "
    if payload[index1][index2] != None:
        description = payload[index1][index2]
    return description

def write_message(text, type, url, repo, description, user): 
    print(url)
    try:
        response = client.chat_postMessage(
                channel="#testing",
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
    except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

main(webhook_payloads.comment)