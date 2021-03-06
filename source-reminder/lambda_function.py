import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from datetime import date, datetime, timedelta
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/admin.directory.user']
API_ENDPOINT = 'https://www.texastribune.org/api/v2/articles/'
FORM_URL = os.environ['FORM_URL']
# Add credentials to the service account.
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# Authorize the client sheet.
client = gspread.authorize(credentials)
# Get the instance of the spreadsheet.
sheet = client.open('Source Diversity Submission (Responses) 2021')
# Get instance of the second sheet.
sheet_instance = sheet.get_worksheet(1)
# Get all records of the data of the instance.
records_data = sheet_instance.get_all_records()
headers = {'headline': 'Headline ', 'pub_date': 'Date of Publication'}

start = date.today() - timedelta(weeks=3)
end = date.today() - timedelta(weeks=1)

# View the data for the relevant window of time and filter out empty lines.
records_data = filter(lambda i: not all(value == '' for value in i.values()), records_data)
timeframe_records = sorted(
    filter(lambda x: start <= datetime.strptime(x[headers['pub_date']], '%m/%d/%Y').date() <= end, records_data),
    key=lambda i: i[headers['pub_date']])
sheet_headlines = [k[headers['headline']] for k in timeframe_records]


def request_data(limit, start_date, end_date):
    query = {'limit': limit, 'start_date': start_date, 'end_date': end_date}
    try:
        response_data = requests.get(API_ENDPOINT, params=query)
        return response_data
    except HTTPError as errh:
        print("HTTP Error:", errh)  # Should Slack send a message to the channel, stating that an error occurred?
    except ConnectionError as errc:
        print("Error Connecting:", errc)
    except Timeout as errt:
        print("Timeout Error:", errt)
    except RequestException as err:
        print("Something Else:", err)

    return 0


response = request_data(100, start, end)
sorted_site = sorted(response.json()['results'], key=lambda i: i['pub_date'])
site_headlines = sorted([x['headline'] for x in sorted_site])

submitted = set(sheet_headlines) & set(site_headlines)
missing = list(sorted(set([x.strip() for x in site_headlines]) - set([x.strip() for x in sheet_headlines])))
missing_full = sorted([x for x in sorted_site if x['headline'] in missing], key=lambda i: i['headline'])


def itemize(elements):
    return " and ".join([", ".join(elements[:-1]), elements[-1]] if len(elements) > 2 else elements)


def cell(headline, image_url):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": headline
        },
        "accessory": {
            "type": "image",
            "image_url": image_url,
            "alt_text": "test"
        }
    }


divider = {
    "type": "divider"
}

blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "We found *{} articles* from *{} to {}* that do not have source information documented.".format(len(missing_full), start.strftime("%B %-d"), end.strftime("%B %-d"))
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Submit Info",
                "emoji": True
            },
            "value": "click_me_123",
            "url": FORM_URL,
            "action_id": "button-action"
        }
    }
]


def generate_blocks():
    # Going to limit the number of identified articles during the development process.
    for item in missing_full[:3]:
        names = [x['author'] for x in item['authors']]
        headline = item['headline']
        sitewide_image = item['sitewide_image']['url']
        link = item['url']
        pub_date = datetime.strptime(item['pub_date'], '%Y-%m-%dT%H:%M:%S%z').strftime("%B %-d")
        blocks.insert(2, cell('*<{}|{}>*\n{}\n{}'.format(link, headline, 'By ' + itemize(names), pub_date), sitewide_image))
        blocks.insert(2, divider)
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Next 2 Results"  # Still trying to see if we can get this to work.
                },
                "value": "click_me_123"
            }
        ]
    })


def lambda_handler(data, context):
    # For debugging purposes.
    print(f"Received event:\n{data}\nWith context:\n{context}.")
    # Keys for the Slack API should be stored as environment variables for security.
    SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    token = data.get('token')
    # Exit early if Slack token is wrong, missing or otherwise problematic.
    if token != SLACK_BOT_TOKEN:
        return {
            'text': 'Something is wrong with the Slack token.',
            'response_type': 'ephemeral'
        }

    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    logger = logging.getLogger(__name__)
    test_channel_id = 'C094XLFL3'
    generate_blocks()
    try:
        # Post the message with WebClient.
        result = slack_client.chat_postMessage(channel=test_channel_id, blocks=blocks)
        # Print result, which includes information about the message (like TS).
        print(result)
    except SlackApiError as e:
        print("Error: {}".format(e))

    # At this point, should we return 0 or the following?
    return {
        'statusCode': 200,
        'body': {}
    }
