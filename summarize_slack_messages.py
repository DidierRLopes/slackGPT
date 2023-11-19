import os
import json
import openai
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from dotenv import load_dotenv
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## Load environment variables
load_dotenv()

## OpenAI API
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY') or "REPLACE-ME"

## Slack API
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL') or "REPLACE-ME"
SLACK_TOKEN = os.getenv('SLACK_TOKEN') or "REPLACE-ME"

## Slack channels ids separated by commas (no spaces), e.g. ABC123,DEF456,GHI789
SLACK_CHANNEL_IDS = os.getenv('SLACK_CHANNEL_IDS') or "REPLACE-ME"


def main():
    openai.api_key = OPENAI_API_KEY
    client = WebClient(token=SLACK_TOKEN)

    for channel_id in SLACK_CHANNEL_IDS.split(","):
        # Store conversation history
        conversation_history = []

        try:

            # --- Get conversation history ---

            # Get the current date and time in UTC
            current_datetime_utc = datetime.utcnow()

            # Set the time to the beginning of today
            start_of_today_utc = datetime(current_datetime_utc.year, current_datetime_utc.month, current_datetime_utc.day, 0, 0, 0)

            # Get the data from the beginning of today in UTC
            result = client.conversations_history(channel=channel_id, oldest=str(int(start_of_today_utc.timestamp())))

            conversation_history = result["messages"]

            # --- Parse conversation history ---

            convo = ""
            # Parse this conversation history
            for message in conversation_history:
                # Check if this is a user message
                if ("type" in message and message["type"] == "message" and "subtype" not in message):
                    # Check if there's a user associated with the message
                    if "user" in message:
                        # Get the user's real name from the users.info API method
                        real_name = client.users_info(user=message['user']).get("user").get("real_name")
                        # The 28_000 is to convert from UTC to PST (8*60*60)
                        text = f"At {datetime.utcfromtimestamp(float(message['ts'])-28_800).strftime('%H:%M')} {real_name} "
                        if "text" in message and message['text']:
                            text += f"said '{message['text']}' "
                        # Provide a link to the files uploaded by the user
                        if "files" in message:
                            text += "shared the following files: "
                            for file in message["files"]:
                                text += file['url_private'] + ","
                            # Remove the last comma
                            text = text[:-1]
                        
                        # Create the conversation from a channel
                        convo += text + "\n"
            
            # --- Get channel name ---

            # Call the conversations.info method with the channel ID
            conversation_info = client.conversations_info(channel=channel_id)

            # Extract the channel name from the result
            channel_name = conversation_info["channel"]["name"]

            # Print results
            if convo:

                # --- OpenAI Summarization ---

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are an executive assistant that analyzes messages on Slack and performs a summary."
                        },
                        {
                            "role": "user", 
                            "content": f"In the channel {channel_name}, summarize the following conversation that has unfolded:\n{convo}"
                        },
                    ]
                )
                summary = response.choices[0].message.content

                # --- Send Slack message with summary ---

                payload = {
                    'text': summary,
                }

                req = Request(SLACK_WEBHOOK_URL, json.dumps(payload).encode('utf-8'))
                try:
                    response = urlopen(req)
                    response.read()
                    
                    print("SUCCESS: Message with insights sent to slack\n")

                except HTTPError as e:
                    print(f"Request failed: {e.code} {e.reason}\n")
                    
                except URLError as e:
                    print(f"Server connection failed: {e.reason}\n")

            else:

                # --- Send Slack message saying no messages were found ---

                payload = {
                    'text': f"No messages were found in channel {channel_name}.",
                }

                req = Request(SLACK_WEBHOOK_URL, json.dumps(payload).encode('utf-8'))
                try:
                    response = urlopen(req)
                    response.read()
                    
                    print("SUCCESS: Message with insights sent to slack\n")

                except HTTPError as e:
                    print(f"Request failed: {e.code} {e.reason}\n")
                    
                except URLError as e:
                    print(f"Server connection failed: {e.reason}\n")

        except SlackApiError as e:
            print(f"Error creating conversation: {e}")

if __name__ == '__main__':
    main()