# Source Reminder

> Source Reminder is a [Slack App](https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c) that runs as a serverless function at scheduled intervals to remind staffers to document the race, gender and ethnicity of the sources of the content that they produce.
### Source Diversity Project
With a commitment to coverage that reflects the diversity of Texas, we have recently put an emphasis on ensuring
that our sources are representative of the entire state. The idea of the initiative is to track race, ethnicity and gender of the people featured in our work.
Currently, reporters do so through a Google Form, but the system is not perfect.
Thus, this tool exists to cross-reference articles on the website and articles submitted via the form to
identify any pieces of work for which source information has not been submitted.

## Requirements
* Docker
* [Lambda](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free) (Amazon Web Services)
* [Google Drive](https://www.google.com/drive/)

_We can be loose with the requirements at times, but at least having them pinned to the major version of a package tends to be helpful._
## Running Locally
1. Clone repo and `cd source-reminder`
2. Configure a local `docker-env` file with the needed environment variables
    ```sh
    cp docker-env-example docker-env
    ```
3. Run Source Reminder Lambda container
    ```sh
    # builds a local image "source-reminder/lambda:local"
    # then runs a container from the image named "source-reminder" on localhost:9000
    make run-container
    ```
4. From a new terminal window, invoke the lambda function (simulates a webhook request to execute Lambda)
    ```sh
    make test-container
    # runs: curl -XPOST "http://localhost:9000/2015-03-31/functions/functioninvocations" -d '{}'
    # In case of source-reminder, we send an empty data body in the request to invoke the function ("-d '{}'"), but for other lambda functions, like hoedown-helper, this data body can be configured to test different invokation scenarios.
    ```
5. The function's output will show up in the terminal running the `source-reminder` Lambda container (matches what would show up in AWS Cloudwatch logs on function invokation).
6. _Optional_:  if `DRY_RUN=True`, no Slack messages will be sent.  The console will output what _would_ have been sent.  If you want to run the function locally and have it send the messages (running as production), then set `DRY_RUN=FALSE`.
### Developing/testing changes to lambda_function.py
Note:  To test out changes to `lambda_function.py`, you will need to:
- Make and save changes to the file
- Stop the `source-reminder` container (`ctrl+c` or `docker stop source-reminder`)
- Restart the `source-reminder container`(`make run-container`)

While we do volume mount `lambda_function.py` into the `source-reminder` container at runtime, so changes to the local file are immediately mirrored/synced inside the running container, it seems that the way the Lambda container works it won't pick up those changes until it's restarted.
## Deployment

This is deployed as a containerized AWS Lambda function.  A Github Action will build and push a new `:latest` Docker image to AWS Container Registry, which will be used to run a container on the next Lambda function execution.

## Google Cloud Integration
A Google Service Account is granted read-only permission to the Google Sheet needed for the API call in this function.  The Service Account Credentials from Google as a JSON file/string, and provided to this function as an environment variable that is base64 encoded (using default unix system package `base64 credentials.json`).  It gets decoded back to json at runtime.  This allows us to configure the json as an environment variable.

### Environment Variables
Set the following environment variables in the Lambda UI:

| Variable            | Description                                           |
| :------------------ | :---------------------------------------------------- |
| `FORM_URL`          | Internal URL to source diversity Google Form.                   |
| `GOOGLE_CREDENTIALS_BASE64`   | Google Service Account credentials, `base64`-encoded string. |
| `SLACK_BOT_TOKEN`   | **Oauth & Permissions > Bot User OAuth Access Token** (including the `xoxb-`). |
| `SLACK_REPORT_CHANNEL`   | ID of the Slack channel to send the finished report to. |
| `SLACK_TEST_CHANNEL`   | ID of Slack test channel. |
## Slack
First off, consult the [Slack API](https://api.slack.com/) to see if it answers any questions better than this document could.
It is a robust API that tries to be intuitive. Since Source Reminder should already exist in our workspace, you need only to open Slack and invite your bot to the appropriate channel, group chat or direct message.
But wait! There&rsquo;s more. For the computer to do what you want, it needs to be sure that you are who you say you are. Consequently, you may want to spend some time ensuring that you have been granted all the permissions that you need.
Note that to test this script locally, you will also need the environment variables on your computer. Try [reading them in](https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file) from an `.env` file or setting them manually in the shell beforehand.
```sh
  export FORM_URL=...
  export SLACK_BOT_TOKEN=...
```
The shell method is convenient in the short term, but you will have to rerun these lines every session.
And while we are on this topic, [@bfreeds](https://github.com/bfreeds) has [suggested](https://github.com/texastribune/tacobots/pull/7#discussion_r674945099) that in the near future we implement two other such variables.
> Might want to consider adding an environment variable for `PROD` or `DEV` environment to be able to configure the script to run differently based on the environment. This would allow us to add a conditional or some other way to configure where the slack messages get sent (to individual users or the test channel) to prevent potential unwanted messages to folks when developing locally.

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