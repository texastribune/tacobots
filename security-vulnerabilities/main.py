import os
import json
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import jsonify
import functions_framework
from slack import WebClient
from slack.errors import SlackApiError
from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['POST'])
def check_vulnerability_alert(request):
  vulnerability_alert = request.get_json()
  return_status = "Incomplete"
  # Validate slack token
  slack_token = os.environ["SLACK_API_TOKEN"]
  client = WebClient(token=slack_token)
      
  # Check to see if 'alert' and 'severity' are in payload --> ensures that this is the correct payload type
  if "alert" in vulnerability_alert:
      return_status = "Has Alert"
      if "severity" in vulnerability_alert["alert"]:
          return_status = "Has severity"
          alert_severity = vulnerability_alert["alert"]["severity"]
          if alert_severity == "high" or alert_severity == "critical": 
              return_status = "Alert severit high or critical"
              try:
                response = client.chat_postMessage(
                    channel="#testing",
                    blocks=[
                      {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "The repository " + vulnerability_alert["repository"]["full_name"] + " has a " + alert_severity + " security alert!"
                        },
                        "accessory": {
                          "type": "button",
                          "text": {
                            "type": "plain_text",
                            "text": "View Alert",
                            # "emoji": true
                          },
                          "value": "click_me_123",
                          "url": vulnerability_alert["repository"]["html_url"] + "/security/dependabot/" + str(vulnerability_alert["alert"]["number"]) ,
                          "action_id": "button-action"
                        }
                      }
                    ]
                )
                return_status =  "Completed"
              except SlackApiError as e:
                  # You will get a SlackApiError if "ok" is False
                  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
  return return_status