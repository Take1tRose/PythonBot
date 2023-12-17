import requests
import json
import signal
import sys

# Your Telegram Bot Token
TOKEN = '6768270353:AAE_UOKyfR_cwB-06XeIHjhO07vU4uOYorQ'

# Your private channel ID (numeric)
PRIVATE_CHANNEL_ID = -1002036223745

def send_message(chat_id, text):
    api_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(api_url, data=params)
    return response.json()

def handle_message(update):
    try:
        # Get the message text
        message_text = update.get('message', {}).get('text')

        if message_text and not message_text.startswith('/start'):
            # Forward the message to the private channel
            send_message(PRIVATE_CHANNEL_ID, message_text)

            # Reply to the user
            chat_id = update['message']['chat']['id']
            send_message(chat_id, "Your message has been forwarded to the private channel.")

    except Exception as e:
        print(f"An error occurred: {e}")

def shutdown(signum, frame):
    print("Bot shutting down gracefully...")
    sys.exit(0)

def main():
    # Register a signal handler to stop the bot gracefully
    signal.signal(signal.SIGINT, shutdown)

    # Start polling for updates
    offset = None
    while True:
        try:
            updates_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}'
            response = requests.get(updates_url)
            data = response.json()

            if 'result' in data and data['result']:
                updates = data['result']

                for update in updates:
                    # Update the offset to avoid receiving the same update again
                    offset = update['update_id'] + 1

                    # Handle the received message
                    handle_message(update)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the main function
    main()
