The StyleBot
------------
> StyleBot is a [custom slash command](https://api.slack.com/interactivity/slash-commands) that runs as a serverless function on AWS Lambda.

### Slash Command Bot
Slack has an app, [Slash Commands](https://slack.com/apps/A0F82E8CA-slash-commands), which makes custom commands simple. The StyleBot was created using this app, and can be found in `Configurations` under `Settings` . 
- Command: `/styleguide`
- Method: `POST`
- Name: `StyleBot`
- Autocomplete: `Yes`
- Description: _Find a term in the Style Guide_

### Environmental Variables
The StyleBot requires one environmental variable:
- `AIRTABLE_API_KEY`
- `AIRTABLE_BASE_ID`
- `SLACK_TOKEN`
- `STYLEGUIDE_URL`

### Deploy
The StyleBot slash command runs as a serverless function on AWS Lambda.  Though it's possible to use the Lambda UI text editor to make changes to `index.js` for quick testing, changes should always be version controlled through this repo.  

To deploy changes:
1.  Use your text editor to update stylebot locally
1.  Save and git commit your changes
1.  Deploy to Lambda
    ```sh
    make deploy
    ```
    - `make deploy` requires:
      - AWS CLI installed & configured with your credentials
      - NPM installed
