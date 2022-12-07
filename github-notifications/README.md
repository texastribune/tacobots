<h1 align="center">
  GitHub Notifications
</h1>

------------
> GitHub Notifications is a [Slack App](https://api.slack.com/). It runs as a serverless function on Google Cloud Function that is only trigger when a webhook is sent from GitHub.
### Reduce Noise in Slack Channel
Currently, our team is using the GitHub Slack app to receive notifications about pull requests, branches, deployments, etc. However, the issue is that the GitHub Slack app also sends a high volume of messages from dependabot to our channel. The purpose of this Slackbot is to help reduce this number of Slack notifications by filtering out pull requests and branches created by dependabot. 
## Requirements
\* [Slack](https://slack.com/get-started#/)

\* [Google Cloud Functions](https://cloud.google.com/functions#/)

## Setup
### Google Cloud Function
##### Environmental Variables
Set the following environment variable in Google Cloud Function:
| Variable            | Description                                                          |
| :------------------ | :------------------------------------------------------------------- |
| `SLACK_API_TOKEN`         | _Oauth & Permissions_ > _Bot User OAuth Access Token_ (Copy everything after the "`xoxb-`")  

##### Create New Function
- On the Cloud Functions, click `Create Function`.
- Under `Environment`, select `2nd gen`.
- Under `Function Name`, enter the name of your function.
- Under `Runtime environment variables`, click `Add Variable`. Then enter the `SLACK_API_TOKEN`.
- Click `Next`.
- Under `Runtime`, select `Python 3.10`.
- Enter the code for your main.py and requirements.txt files here. 
- Make sure to update the `Entry Point`. 
- Click `Deploy`.
- If the function was successfully deployed, there should been a green checkmark in the upper left hand corner. You will also see an URL, which you will need to set up your GitHub webhook. 

##### Set Function Permissions
- In order for this function to receive webhooks from GitHub, it needs to be able to [allow unauthenticated HTTP function invocation](https://cloud.google.com/functions/docs/securing/managing-access-iam#after_deployment#/). Make sure to follow the instructions for 2nd gen functions. 


### Set up GitHub Webhook 
- On the repository that you want to receive alerts from, click `Settings`.
- Under `Code and Automation`, select `Webhooks`.
- Click `Add webhook`.
- Under `Payload URL`, add the URL from your Cloud Function. 
- Under `Content Type`, select `application/json`.
- Under `Which events would you like to trigger this webhook?`, select `Let me select individual events.`. Then select `Branch or tag creation` and `Pull requests`. 
- Make sure the that the checkbox for `Active` is selected.
- Click `Add webhook`. 

### Slack App
- On the [Slack API](https://api.slack.com/), click `start building`. 
- Enter the name of your app. We used `GitHub Notifications` and select the Slack you want to install the App on.  

##### Set App Permissions
- Click on `OAuth & Permissions` and scroll to the bottom of the page where it says scopes. 
- Under `Bot Token Scopes` click `Add an  OAuth Scope`. 
- Select `chat:write`. 
- Scroll back to the top and click, `Install App to Workspace`. 
- Click `allow`. You will be return to the OAuth page. 
- At the top of the page there should be an access token. Copy everything that follows `xoxb-` This is your `SLACK_API_TOKEN` and should be set in your Google Cloud Function. 

##### Install to Channel
- Open Slack and invite your bot to the channel it should be monitoring by calling it (i.e. `@`)

### Test Locally
In order to test locally, you will need a .env file with the SLACK_API_TOKEN. The json_payloads.py file has test GitHub webhook payloads that can be switched out if necessary. 

##### Run the Server
```sh
# enter this directory
cd github-notifications
# start the server (will run on localhost)
functions-framework --target process_request --debug
```

##### Option 1: Use the invoke_function.py file
```sh
# open up another terminal
# enter this directory
cd github-notifications
# run the local version of the function
python3 invoke_function.py
```
After running the function, you should receive a Slack message to the designated channel. 

##### Option 2: Use the Curl command
You can also send a Curl command to localhost when the server is running. Your command will look similar to below: 
```sh
curl -X POST localhost:8080 \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{
    }'
```
After running the command, you should receive a Slack message to the designated channel. 
