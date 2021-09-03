import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from datetime import date, datetime, timedelta
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# temp vars for testing
MANUAL_RUN = True
DRY_RUN = True

ARTICLE_API_ENDPOINT = 'https://www.texastribune.org/api/v2/articles/'
AUTHOR_API_ENDPOINT = 'https://www.texastribune.org/api/v2/authors/'
FORM_URL = os.environ['FORM_URL']

SLACK_REPORT_CHANNEL = os.environ['SLACK_REPORT_CHANNEL']
SLACK_TEST_CHANNEL = os.environ['SLACK_TEST_CHANNEL']

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/admin.directory.user']
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

start = datetime.today() - timedelta(weeks=3)
end = datetime.today() - timedelta(weeks=1)
# View the data for the relevant window of time and filter out empty lines.
records_data = filter(lambda i: not all(value == '' for value in i.values()), records_data)
timeframe_records = sorted(
    filter(lambda x: start <= datetime.strptime(x[headers['pub_date']], '%m/%d/%Y') <= end, records_data),
    key=lambda i: i[headers['pub_date']])
sheet_headlines = [k[headers['headline']] for k in timeframe_records]
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
slack_client = WebClient(token=SLACK_BOT_TOKEN)


def request_data(limit, start_date, end_date):
    query = {'limit': limit, 'start_date': start_date.isoformat(), 'end_date': end_date.isoformat()}
    try:
        response_data = requests.get(ARTICLE_API_ENDPOINT, params=query)
        if response_data.status_code == 200:
            print('Retrieved articles from article API')
            total_items = response_data.json()['results']
            next_page = response_data.json()['next']
            while next_page is not None:
                additional_data = requests.get(next_page).json()
                total_items.extend(additional_data['results'])
                next_page = additional_data['next']
            return total_items
        else:
            print(f'Request is not good: {response_data.status_code}.')  # Set missing_full to empty?
    except HTTPError as errh:
        print("HTTP Error:", errh)  # Should Slack send a message to the channel, stating that an error occurred?
    except ConnectionError as errc:
        print("Error Connecting:", errc)
    except Timeout as errt:
        print("Timeout Error:", errt)
    except RequestException as err:
        print("Something Else:", err)
    # TODO - Add Sentry error handling: https://github.com/texastribune/tacobots/pull/7#discussion_r674926028
    return 0


def request_author(slug):
    try:
        response_data = requests.get(AUTHOR_API_ENDPOINT + slug)
        return response_data
    except HTTPError as errh:
        print("HTTP Error:", errh)  # Should Slack send a message to the channel, stating that an error occurred?
    except ConnectionError as errc:
        print("Error Connecting:", errc)
    except Timeout as errt:
        print("Timeout Error:", errt)
    except RequestException as err:
        print("Something Else:", err)

    return ''


response = request_data(100, start, end)

sorted_site = sorted(response, key=lambda i: i['pub_date'])
site_headlines = sorted([x['headline'] for x in sorted_site])

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


numerals = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

divider = {
    "type": "divider"
}


def format_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').strftime("%B %-d, %Y")
    except ValueError:
        return s


def serialize_authors(articles):
    articles_of_interest = {}
    for entry in articles:
        authors = entry['authors']
        for author in authors:
            slug = ''.join(author['url'].split('/')[-2])

            if slug not in articles_of_interest:
                articles_of_interest[slug] = []
            articles_of_interest[slug].append(entry)
    return articles_of_interest


def generate_block(article, cowriters):
    print('generator', cowriters)
    has_cowriters = len(cowriters) >= 1
    addressees = ['You'] + cowriters
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*" + article['headline'] + "*" + has_cowriters*f'\n{itemize(addressees)} on ' + (not has_cowriters)*'\n' + format_date(article['pub_date'])  # <@user_id>
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "View",
                "emoji": True
            },
            "value": "click_me",
            "url": article['url'],
            "action_id": "button-action"
        }
    }


def generate_blocks_groups(serialization):
    blocks_groups = []
    for slug, articles in serialization.items():
        blocks = []
        print(slug, len(articles))
        for article in sorted(articles, key=lambda i: i['pub_date'], reverse=True):
            try:
                cowriters = [x['author'] for x in article['authors'] if x['url'].split('/')[-2] != slug]
            except KeyError:
                cowriters = []
            blocks.append(generate_block(article, cowriters))
            blocks.append(divider)
        blocks_groups.append({slug: blocks})
    return blocks_groups


cores = []
opener = {
    "type": "context",
    "elements": [
        {
            "type": "mrkdwn",
            "text": ""
        }
    ]
}


def generate_packages(blocks_group):
    packages = []
    for blocks_group in blocks_group:
        for slug, blocks in blocks_group.items():
            try:
                staff_email = request_author(slug).json()['staff_email']
                user_response = slack_client.users_lookupByEmail(token=SLACK_BOT_TOKEN,
                                                                 email=staff_email)
                if staff_email != '':
                    slack_id = user_response['user']['id']
                    core = {"blocks": []}
                    core['blocks'] = blocks
                    packages.append({'slack_id': slack_id, 'core': core, 'first_name': user_response['user']['profile']['first_name']})
                else:
                    continue
            except KeyError:
                print(f'Author {slug} does not have email address publicly available.')
                continue
            except AttributeError:
                print(f'Something went wrong with the email address returned for {slug}.')
            except SlackApiError as e:
                print(f"Error posting message: {e}")
                continue
    return packages


def send_message(package):
    recipient_id, first_name, r_core = package['slack_id'], package['first_name'], package['core']
    num_articles = len(r_core['blocks'])//2
    is_plural = num_articles != 1
    first_sentence = '️{}, you have not documented source information for {} recent {}.'.format(first_name, numerals[num_articles] if num_articles <= 9 else num_articles, 'article' + is_plural*'s')
    opener['elements'][0]['text'] = '\u26A0 ' + first_sentence + ' *Kindly <{}|submit a response> to the Google Form at your earliest convenience where applicable.*'.format(FORM_URL)

    r_core['blocks'].insert(0, opener)
    if not DRY_RUN:
        try:
            print(f'Sending message to {first_name}...')
            return slack_client.chat_postMessage(channel=recipient_id, text=first_sentence, blocks=r_core['blocks'])
        except SlackApiError as e:
            print(f'Something went wrong with slack {e}')
            return None
    else:
        print(f'Would have sent message to {first_name}...')


# Send all the messages!
def send_messages(packages):
    for package in packages:
        result = send_message(package)
        if result is not None:
            print(result)
        else:
            print('Doesn\'t seem like everything went to plan for this package: {}.'.format(package))

# Send report of missing submissions
def send_report(serialization):
    slack_blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*_Report for {start.strftime('%m/%d/%Y')} - {end.strftime('%m/%d/%Y')}_*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Number of stories submitted*: {len(sheet_headlines)}\n*Number of stories missing*: {len(missing_full)}",
            },
        },
    ]
    text_block = ''
    for slug, articles in serialization.items():
        text_block += f"\n{slug}\n"
        for article in sorted(articles, key=lambda i: i['pub_date'], reverse=True):
            text_block += f"{article['url']}\n"

    slack_blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"```{text_block}```",
            },
        ]
    })

    if DRY_RUN:
        source_diversity_channel = SLACK_TEST_CHANNEL
    else:
        source_diversity_channel = SLACK_REPORT_CHANNEL
    try:
        print('Sending report...')
        return slack_client.chat_postMessage(channel=source_diversity_channel, text='Source report', blocks=slack_blocks)
    except SlackApiError as e:
        print(f'Something went wrong with slack {e}')
        return None


def lambda_handler(data, context):
    # For debugging purposes.
    print(f"Received event:\n{data}\nWith context:\n{context}.")
    # Keys for the Slack API should be stored as environment variables for security.
    token = data.get('token')
    # Exit early if Slack token is wrong, missing or otherwise problematic.
    if token != SLACK_BOT_TOKEN:
        return {
            'text': 'Something is wrong with the Slack token.',
            'response_type': 'ephemeral'
        }

    logger = logging.getLogger(__name__)

    try:
        serialization = serialize_authors(missing_full)
        grouped_blocks = generate_blocks_groups(serialization)
        final_packages = generate_packages(grouped_blocks)
        send_messages(final_packages)
        send_report(serialization)
        return {
            'statusCode': 200,
            'text': 'Success.',
            'body': {}
        }
    except SlackApiError as e:
        # At this point, should we return 0 or the following?
        return {
            'statusCode': 500,
            'text': e,
            'body': {}
        }

if MANUAL_RUN:
    serialization = serialize_authors(missing_full)
    grouped_blocks = generate_blocks_groups(serialization)
    final_packages = generate_packages(grouped_blocks)
    send_messages(final_packages)
    send_report(serialization)
    print('Manual run complete')
