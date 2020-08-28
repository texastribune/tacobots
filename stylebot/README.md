<h1 align="center">
  Stylebot
</h1>

------------
> StyleBot is a [custom slash command](https://api.slack.com/interactivity/slash-commands) that returns information from the style guide upon request.  It runs as an AWS Lambda function.

### Slash Command Bot
Slack has an app, [Slash Commands](https://slack.com/apps/A0F82E8CA-slash-commands), which makes custom commands simple. The StyleBot was created using this app, and can be found in `Configurations` under `Settings` . 
- Command: `/styleguide`
- Method: `POST`
- Name: `StyleBot`
- Autocomplete: `Yes`
- Description: _Find a term in the Style Guide_

## Requirements
* [Lambda](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free)
* [Airtable](https://airtable.com/pricing)
* [Slack](https://slack.com/get-started#/)


### Environmental Variables
Set the following environment variables in Lambda UI:
| Variable            | Description                                                |
| :------------------ | :--------------------------------------------------------- |
| `AIRTABLE_API_KEY`  | Airtable account API                                       |
| `AIRTABLE_BASE_ID`  | The Airtable Base ID for styleguide                        |
| `SLACK_TOKEN`       | Slash Commands > Integration Settings> "Token"             |
| `STYLEGUIDE_URL`    | URL to Styleguide documentation (Google Doc, website, etc) |


### Deploy
Deploy to AWS Lambda function.  If there are local changes in the Lambda UI not reflected in this repo, this will overwrite them.

```sh
# enter this directory
cd stylebot
# install dependencies and deploy zipped package to aws lambda
make deploy
```
