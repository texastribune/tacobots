The Hoedown Helper 
------------
> The Hoedown Helper is a [Slack App](https://api.slack.com/). It runs as a serverless function on AWS Lambda which only triggers when a message is posted to a channel that Hoedown Helper is part of.

### In-App Style Checks
At the Texas Tribune, reporters and editors often ask for help creating a good headline. The Hoedown Helper checks every message in the channel where those conversations happen for Style errors. If an error is found, it responds with the issue and a potential solution. 

### How To

**Create the Slack App**
- On the [Slack API](https://api.slack.com/), click `start building`. 
- Enter the name of your app. We used `Hoedown Helper` and select the Slack you want to install the App on.  

**App Permissions**
- Click on `OAuth & Permissions` and scroll to the bottom of the page where it says scopes. 
- Under `Bot Token Scopes` click `Add an  OAuth Scope`. 
- Select `channels:history` and `chat:write`. 
- Scroll back to the top and click, `Install App to Workspace`. 
- Click `allow`. You will be return to the OAuth page. 
- At the top of the page there should be an access token. Copy everything that follows `xoxb-` This is your `BOT_TOKEN` and should be set in Lambda. 

**Event Subscriptions**
- Click on `Event Subscriptions` and enable events. 
- You will see a place to add your request url. Add the Lambda endpoint here. It should verify automatically. 
- Once your url has been verified, open `Subscribe to bot events` and select `message.channels`.

**Install to Channel**
- Open Slack and invite your bot to the channel it should be monitoring by calling it (i.e. `@hoedown_helper`)