# Conversation export
> Pulls history of a specified channel into a static site, which can be saved as a PDF


## Limitations
- Does not display screenshots
- Does not find the name of users no longer in Slack
- Waits a second between each paginated response. (Could take a while for chatty channels)
- Does not work for DMs

## Getting started

1. Clone this repo and make sure you're in this folder

```sh
cd conversation-exporter
```

2. Set up required variables
```sh
export SLACK_EXPORT_CHANNEL=<channel-id> SLACK_EXPORT_TOKEN=<slack-token-from-vault>
```

3. Go to the specified channel in Slack and type `@Conversation Export`. Slack will prompt to invite the bot, which is what we want.

4. Install python and npm libraries
```sh
make
```

5. Start the job to retrieve messages. This will take a while.
```sh
python messages.py
```
(Note you may need to specify `python3`)
This builds a json file called `messages.json` in `/src/_data`

6. Get user and channel data. This shouldn't take as long message retrieval.
```sh
python users.py
```
```sh
python channel.py
```

7. Confirm you have `messages.json`, `users.json`, `channel.json` in `/src/_data`

8. Start local preview
```sh
npm run serve
```

9. If desired, print page and save as PDF.