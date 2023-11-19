# SlackGPT

The SlackGPT is a Slack bot that summarizes conversations and sends you a summary per channel.

If you want to run it locally, you can use:

```console
python slackgpt.py
```

Otherwise, fork the project, set up the GitHub secrets and you can leverage the GitHub action to run it automatically.

## Getting Started

### Slack API

1. Go to [Slack API page](https://api.slack.com/apps) and create a new app.

2. Install the app in the workspace you are interested in summarizing Slack messages.

3. Get the **User OAuth Token** which exists in the **Install App** settings. This will be needed to use Slack's SDK. Set this value as the `SLACK_TOKEN` on a `.env` file if you want to run the script locally or as a GitHub secret if you want to leverage the GitHub workflow.

<p align="center">
  <img width="800" alt="Screenshot 2023-11-18 at 9 49 53 PM" src="https://github.com/DidierRLopes/slackGPT/assets/25267873/0b4bd347-ff38-40d4-9f85-c3c069680597">
</p>

4. Create a **Webhook URL** for your channel so that you can receive messages' summary. Set this value as the `SLACK_WEBHOOK_URL` on a `.env` file if you want to run the script locally or as a GitHub secret if you want to leverage the GitHub workflow.

5. Depending on the type of access needed, different **User Token Scopes** need to be set. Here's the methods that we will need and the associated user token scopes.

- **conversations_history**: This method retrieves a conversation's history of messages and events. It requires the **channels:history** scope for public channels, or **groups:history** for private channels and **im:history** for direct messages.

- **users_info**: This method returns information about a user. It requires the **users:read** scope.

- **conversations_info**: This method retrieves information about a conversation. It requires the **channels:read** scope for public channels, or **groups:read** for private channels and **im:read** for direct messages.

<p align="center">
  <img width="800" alt="Screenshot 2023-11-18 at 9 53 57 PM" src="https://github.com/DidierRLopes/slackGPT/assets/25267873/7cd4ccea-5826-4cda-8a6f-dce246308957">
</p>


### OpenAI API

Go to [OpenAI API page](https://platform.openai.com/api-keys) to extract the API key. Set this value as the `OPENAI_API_KEY` on a `.env` file if you want to run the script locally or as a GitHub secret if you want to leverage the GitHub workflow.

<p align="center">
  <img width="800" src="https://github.com/DidierRLopes/slackGPT/assets/25267873/6ee7e1e8-df4c-4ba3-9d38-bf34c827778d">
</p>


### Slack channels

Get the Channel IDs that you are interested in reading messages from.

Set those values as the `SLACK_CHANNEL_IDS` on a `.env` file if you want to run the script locally or as a GitHub secret if you want to leverage the GitHub workflow. If you want to read from multiple channels you can set `SLACK_CHANNEL_IDS` with multiple IDs separated by commas (with no space), e.g. ABC123,DEF456,GHI789.

<p align="center">
  <img width="800" src="https://github.com/DidierRLopes/slackGPT/assets/25267873/4c68da63-370f-4f9f-b2ce-377347ce3817">
</p>


