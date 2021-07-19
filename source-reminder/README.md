# Source Reminder

> Source Reminder is a [Slack App](https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c) that runs as a serverless function at scheduled intervals.
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

Deploy to AWS Lambda function. If there are local changes in the Lambda UI not reflected in this repo, this will overwrite them. Serverless Application Model
*Requires Docker and the AWS CLI.*

| Operating System            | Instructions                                           |
| :------------------ | :---------------------------------------------------- |
| macOS          | Install SAM CLI with Brew. First run `brew tap aws/tap` and then `brew install aws-sam-cli` immediately thereafter.                   |
| Windows   | Install SAM CLI using an [MSI](https://github.com/awslabs/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi). |
| Linux   | Install SAM CLI by downloading an [archive file](https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip). |


## Packaging

```sh
# enter this directory
cd source-reminder
# install dependencies and deploy zipped package to aws lambda
sam build
```
Then you&rsquo;ll have a hidden folder, the contents of which you may [upload](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) to AWS. Reveal hidden items in Finder with <kbd>⌘</kbd> + <kbd>⇧</kbd> + <kbd>.</kbd>; likewise, remember to archive the files in the folder, not the folder itself. Yes, highlight all the items inside the folder and do it that way.
Otherwise, it will not work properly. There are [several ways](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) to get the proper files into Lambda, but so far this is the only method that has reliably worked.

## Lambda
- In the interface, look for the orange button that says **Create function** in the upper right.
- Follow the on-screen prompts until you have blank function.
- Click **Upload from** and upload the `.zip` file containing the package.
### Environment Variables
Set the following environment variables in the Lambda UI:

| Variable            | Description                                           |
| :------------------ | :---------------------------------------------------- |
| `FORM_URL`          | Internal URL to source diversity Google Form.                   |
| `SLACK_BOT_TOKEN`   | **Oauth & Permissions > Bot User OAuth Access Token** (including the `xoxb-`). |
## Slack
- On the [Slack API](https://api.slack.com/),
- Open Slack and invite your bot to the appropriate channel.

### App Permissions
- Click on **OAuth & Permissions** and scroll to the bottom of the page to find the scopes. 
- Under **Bot Token Scopes** click the **Add an  OAuth Scope** button. 
- Select `channels:read`, `chat:write`, `users:read` and `users:read.email`.
- Scroll back to the top and click the **Install App to Workspace** button. 
- Grant permissions, and you will be returned to the OAuth page. 
- At the top of the page, there should be an access token. This is your `SLACK_BOT_TOKEN` and should be set in Lambda. 

## Invocation

In the Lambda interface, you will notice that the deployment package for the function is too large for inline code editing.
The code will not be visible, but it is there, and you can invoke it in the **Test** panel.

### Troubleshooting
If it does not run as it is supposed to, here are a few common issues: