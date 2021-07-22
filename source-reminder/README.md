# Source Reminder

> Source Reminder is a [Slack App](https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c) that runs as a serverless function at scheduled intervals to remind staffers to document the race, gender and ethnicity of the sources of the content that they produce.
### Source Diversity Project
With a commitment to coverage that reflects the diversity of Texas, we have recently put an emphasis on ensuring
that our sources are representative of the entire state. The idea of the initiative is to track race, ethnicity and gender of the people featured in our work.
Currently, reporters do so through a Google Form, but the system is not perfect.
Thus, this tool exists to cross-reference articles on the website and articles submitted via the form to
identify any pieces of work for which source information has not been submitted.

## Requirements
* [Lambda](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free) (Amazon Web Services)
* [Google Drive](https://www.google.com/drive/)
* [Slack SDK](https://slack.dev/node-slack-sdk/)
* [Gspread](https://github.com/burnash/gspread) 
* [Client library](https://github.com/googleapis/oauth2client) for OAuth 2.0&mdash;also known as `oauth2client`
* [Python Requests](https://docs.python-requests.org/)
* [Python Datetime](https://docs.python.org/3/library/datetime.html)

## Google Cloud Integration
To properly receive the data from an API call, you&rsquo;ll be required at some point to provide what&rsquo;s called a *credentials* file for said account.
It lives in the Amazon Web Services Lambda computing platform with the rest of the files and responds to webhook requests. Seven libraries are required, but two of them are pre-installed with Python, so really you only need to worry about packaging the five above.

## Deployment

Once the integrity of the code is certain, deploy it to its AWS Lambda function. If there are local changes in the Lambda UI not reflected in this repo, this will overwrite them. The Serverless Application Model
requires Docker and the AWS CLI. Down the road, we may implement deployment with the following:

| Operating System            | Instructions                                           |
| :------------------ | :---------------------------------------------------- |
| macOS          | Install SAM CLI with Brew. First run `brew tap aws/tap` and then `brew install aws-sam-cli` immediately thereafter.                   |
| Windows   | Install SAM CLI using an [MSI](https://github.com/awslabs/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi). |
| Linux   | Install SAM CLI by downloading an [archive file](https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip). |
For now, developers will use their local copy of the Makefile to handle it.
Ideally, this procedure would be decentralized, carried out through one of several [more sophisticated methods](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) and automated with a GitHub Action, which is what may eventually come to pass.
At present, the crafty among us will see that `sam` creates a hidden folder after the builder, regardless of whether deployment takes place. The contents of the folder may be [uploaded](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) to AWS manually, but we will avoid this _in vitro_ approach for now.

If you are still feeling bold today, go ahead and give it a go in Finder with <kbd>⌘</kbd> + <kbd>⇧</kbd> + <kbd>.</kbd>. Remember to archive the files in the folder, not the folder itself. Yes, highlight all the items inside the folder and do it that way.
Otherwise, it will not work properly.

## Packaging

Here is the real deal:
```sh
# Enter the directory at hand.
cd source-reminder
# Install dependencies and deploy zipped package to us-east-1 in Lambda via Makefile.
make
```
If this does not work right away, do not panic. Contact a colleague to see whether the error is critical or merely trivial in some way.
There are many ways for it to go wrong and a handful of ways for it to go right. See [**Troubleshooting**](#troubleshooting) for some quick fixes.
## Lambda
Once the code is in the right place, along with its dependencies, you are within eyeshot of the end.
1. In the interface, look for the orange button that says **Create function** in the upper right.
2. Follow the on-screen prompts until you have blank function.
3. Click **Upload from** and upload the `.zip` file containing the package.
### Environment Variables
Set the following environment variables in the Lambda UI:

| Variable            | Description                                           |
| :------------------ | :---------------------------------------------------- |
| `FORM_URL`          | Internal URL to source diversity Google Form.                   |
| `SLACK_BOT_TOKEN`   | **Oauth & Permissions > Bot User OAuth Access Token** (including the `xoxb-`). |
## Slack
First off, consult the [Slack API](https://api.slack.com/) to see if it answers any questions better than this document could.
It is a robust API that tries to be intuitive. Since Source Reminder should already exist in our workspace, you need only to open Slack and invite your bot to the appropriate channel, group chat or direct message.
But wait! There&rsquo;s more. For the computer to do what you want, it needs to be sure that you are who you say you are. Consequently, you may want to spend some time ensuring that you have been granted all the permissions that you need.

### App Permissions
- Click on **OAuth & Permissions** and scroll to the bottom of the page to find the scopes. 
- Under **Bot Token Scopes** click the **Add an  OAuth Scope** button. 
- Select `channels:read`, `chat:write`, `users:read` and `users:read.email`.
- Scroll back to the top and click the **Install App to Workspace** button. 
- Grant permissions, and you will be returned to the OAuth page. 
- At the top of the page, there should be an access token. This is your `SLACK_BOT_TOKEN` and should be set in Lambda. 

Should any of these steps cause you difficulty, reach out to a team member who has access to that which you need.
## Invocation

In the Lambda interface, you will notice that the deployment package for the function is too large for inline code editing.
The code will not be visible, but it is there, and you can invoke it in the **Test** panel.
The script can only be run at the request of a human being&mdash;but that is temporary.
In the near future, Source Reminder will become a [cron job](https://www.freecodecamp.org/news/using-lambda-functions-as-cronjobs/) that runs once every Friday morning at 9 a.m. Central Standard Time.

### Troubleshooting

If it does not run as it is supposed to, here are a few common issues:
- Messages do not arrive at the right place.
    - The culprit here could be the line in the `def send_message(package):` block that passes in a `channel` identifier to Slack&rsquo;s SDK as a keyword argument.
    -  Passing in `recipient_id` will result in the appropriate staffer being notified of their outstanding pieces of content and is the value that ought to exist in Lambda.
    -  If you are testing the functionality, running these lines repeatedly, it is best not to bug your colleagues so incessantly and without reason.
    -   Consider changing up the value passed in as `channel` to the ID of a test channel or your own Slack ID (can be found in your profile panel). Twist the dials and see what does and does not result in the desired functionality.
- Not all the articles for the time frame are being counted.
    - The program limits each request to 100 articles by default.
    - A way to circumvent this is to (1) change the limit in the query parameters or (2) run the `while` loop for as long as the API response still indicates that there is another page of results, which can conveniently be accessed with a reference to the request followed by `.json()['next']`.
    - You will receive a new URL that leads to another JSON object, this time containing the next 100 responses, as well as a URL to the next 100 responses after that if such responses exist.
- The environment variables are causing the program to crash locally.
    - Tough. If you can figure out how to set an environment variable in your computer&rsquo;s operating system, we would love to hear from you.
    - In all seriousness, there are [resources](https://www.twilio.com/blog/environment-variables-python) online for how to get the environment variables to work, but if it&rsquo;s getting thorny and you are in a pinch, it is okay to _temporarily_ replace them with the actual secret strings. **Just make sure that you revert those lines** back to `os.environ['FORM_URL']` and `os.environ['SLACK_BOT_TOKEN']` for Lambda. This repository is public.
- The API comes back with a non-200 response.
    - Check your Internet connection if you are calling the API remotely.
    - If you are calling the API locally, have you run `make dev` in your directory for the main `texastribune` repository? If so, take a second look at the virtual environment in your command line, and see if npm update or npm install does anything. And of course, to get everything in motion, you must run `make runserver`.
    - See if anything in Docker needs to be refreshed.