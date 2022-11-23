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
    return_status = "Incomplete"
    print("in main")

    # Check if dependabot security alert
    if webhook_payload_list[1] == "alert":
        if webhook_payload["action"] == "created": 
            dependabot_alert(webhook_payload)

    # Check if event caused by dependabot
    sender = webhook_payload["sender"]["login"]
    print(sender)
    if sender == "dependabot[bot]":
        return_status = "Complete"
        return return_status

    print("checking")
    if webhook_payload_list[1] == "ref_type":
        print("type")
        if webhook_payload["ref_type"] == "branch":
            return_status = create_branch(webhook_payload)
        elif webhook_payload["ref_type"] == "tag":
            print("tag")
            return_status = create_tag(webhook_payload)
    elif webhook_payload_list[0] == "ref":
        if webhook_payload_list[4] == "pusher":
            return_status = push(webhook_payload)
    elif webhook_payload_list[1] == "comment":
        return_status = comments(webhook_payload)
    elif webhook_payload_list[1] == "deployment":
        return_status = deployment(webhook_payload)
    elif webhook_payload_list[1] == "issue":
        return_status = issues(webhook_payload)
    elif webhook_payload_list[1] == "review":
        return_status = pull_request_review(webhook_payload)
    elif webhook_payload_list[2] == "pull_request":
        return_status = pull_request(webhook_payload)
    elif webhook_payload_list[1] == "release":
        return_status = release(webhook_payload)
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

def create_tag(payload):
    # description = get_description(payload, "repository", "description")
    description = payload["ref"] 
    sender = payload["sender"]["login"]
    repository = payload["repository"]["full_name"]
    url = payload["repository"]["html_url"] + "/tags"
    text = ":tagspaces: Tag created"
    return_status = write_message(text,"Tag ", url, repository, description, sender)
    return return_status

def comments(payload):
    sender = payload["sender"]["login"]
    description = get_description(payload, "comment", "body")
    comment_url = payload["comment"]["html_url"]
    repository = payload["repository"]["full_name"]
    text = ":comment_add-1: Comment " + payload["action"]
    return_status = write_message(text,"Comment ", comment_url, repository, description, sender)
    return return_status

def deployment(payload):
    sender = payload["sender"]["login"]
    deployment_url = payload["repository"]["html_url"] + "/deployments"
    repository = payload["repository"]["full_name"]
    text = ":partydeploy: Deployment " + payload["action"]
    description = get_description(payload, "repository", "description")
    return_status = write_message(text,"Deployment", deployment_url, repository, description, sender)
    return return_status

def issues(payload):
    sender = payload["sender"]["login"]
    issues_url = payload["issue"]['html_url']
    text = ":dumpster-fire-cute: Issue " + payload["action"]
    repository = payload["repository"]["full_name"]
    # issue_description = payload["issue"]['body']
    description = get_description(payload, "issue", "title")
    return_status = write_message(text,"Issue", issues_url, repository, description, sender)
    return return_status

def pull_request(payload):
    sender = payload["sender"]["login"]
    pr_url = payload["pull_request"]['html_url']
    repository = payload["repository"]["full_name"]
    text = ":yay: Pull Request " + payload["action"]
    repository = payload["repository"]["full_name"]
    # title = payload["pull_request"]["title"]
    description = get_description(payload, "pull_request", "title")
    return_status = write_message(text,"Pull Request", pr_url, repository, description, sender)
    return return_status

def pull_request_review(payload):
    sender = payload["sender"]["login"]
    pr_review_url = payload["review"]['html_url']
    repository = payload["repository"]["full_name"]
    # title = payload["repository"]["title"]
    text = ":document_text: Pull Request Review " + payload["action"]
    description = get_description(payload, "pull_request", "body")
    return_status = write_message(text,"Pull Request Review ", pr_review_url, repository, description, sender)
    return return_status

def push(payload):
    sender = payload["sender"]["login"]
    text = ":pusheencomputer: Commit pushed"
    commit_url = payload['commits'][0]["url"]
    description = payload['commits'][0]["message"]
    repository = payload["repository"]["full_name"]
    write_message(text,"Commit ", commit_url, repository, description, sender)

def release(payload):
    sender = payload["sender"]["login"]
    text = ":laptop_parrot: Release " + payload["action"]
    release_url = payload['release']['html_url']
    repository = payload["repository"]["full_name"]
    description = get_description(payload, "release", "tag_name")
    return_status = write_message(text,"Release ", release_url, repository, description, sender)
    return return_status

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
    text = ":rotating_light:" + severity.title() + " level security alert "
    return_status = write_message(text,"Alert ", alert_url, repository, description, sender)
    return return_status

def get_description(payload, index1, index2):
    description = " "
    if payload[index1][index2] != None:
        description = payload[index1][index2]
    return description

def write_message(text, type, url, repo, description, user): 
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

#create_branch, comment, deployment, issues, pull_request, pull_request_review, release, high_level_alert, push
# Uncomment whichever type you want to test
# main(webhook_payloads.comment)
# main(webhook_payloads.create_branch)
# main(webhook_payloads.tag)
# main(webhook_payloads.issues)
# main(webhook_payloads.pull_request)
# main(webhook_payloads.pull_request_review)
# main(webhook_payloads.release)
# main(webhook_payloads.push)
# main(webhook_payloads.deployment)
