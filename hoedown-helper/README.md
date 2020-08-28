<h1 align="center">
  Hoedown Helper
</h1>

------------
> The Hoedown Helper is a [Slack App](https://api.slack.com/). It runs as a serverless function on AWS Lambda which only triggers when a message is posted to a channel that Hoedown Helper is part of.
### In-App Style Checks
At The Texas Tribune, reporters and editors often ask for help creating a good headline. The Hoedown Helper checks every message in the channel where those conversations happen for Style errors. If an error is found, it responds with the issue and a potential solution. 
## Requirements
* [Lambda](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free)
* [Airtable](https://airtable.com/pricing)
* [Slack](https://slack.com/get-started#/)

[How to Create a Slack Bot using AWS Lambda in < 1 hour](https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c)


### Setup
#### Lambda
##### Environmental Variables
Set the following environment variables in Lambda UI:
| Variable            | Description                                                          |
| :------------------ | :------------------------------------------------------------------- |
| `AIRTABLE_API_KEY`  | Airtable account API                                                 |
| `AIRTABLE_BASE_ID`  | The Airtable Base ID for styleguide                                  |
| `BOT_TOKEN`         | _Oauth & Permissions_ > _Bot User OAuth Access Token_ (Copy everything after the "`xoxb-`")                                  |
| `SLACK_TOKEN`       | _Basic Information_ > _App Credentials_ > _Verification Token_             |
| `STYLEGUIDE_URL`    | URL to Styleguide documentation (Google Doc, website, etc)           |
#### Slack App
- On the [Slack API](https://api.slack.com/), click `start building`. 
- Enter the name of your app. We used `Hoedown Helper` and select the Slack you want to install the App on.  

##### Set App Permissions
- Click on `OAuth & Permissions` and scroll to the bottom of the page where it says scopes. 
- Under `Bot Token Scopes` click `Add an  OAuth Scope`. 
- Select `channels:history` and `chat:write`. 
- Scroll back to the top and click, `Install App to Workspace`. 
- Click `allow`. You will be return to the OAuth page. 
- At the top of the page there should be an access token. Copy everything that follows `xoxb-` This is your `BOT_TOKEN` and should be set in Lambda. 

##### Set Event Subscriptions
- Click on `Event Subscriptions` and enable events. 
- You will see a place to add your request url. Add the Lambda endpoint here. It should verify automatically. 
- Once your url has been verified, open `Subscribe to bot events` and select `message.channels`.

##### Install to Channel
- Open Slack and invite your bot to the channel it should be monitoring by calling it (i.e. `@hoedownhelper`)

#### Deploy  

Deploy to AWS Lambda function.  If there are local changes in the Lambda UI not reflected in this repo, this will overwrite them.

```sh
# enter this directory
cd hoedown-helper
# install dependencies and deploy zipped package to aws lambda
make deploy
```