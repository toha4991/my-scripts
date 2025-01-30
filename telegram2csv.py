# a script that takes a telegram chat and extract all the links from it

import re                       # re as regurlar expresions
import os                       # a way to interact with os
import requests                 # a mdule for http or API requests
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API token and chat ID from environment variables
API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def extract_links(text):
    """
    Extracts all URLs from the given text using a regular expression.
    
    Args:
        text (str): The text to search for URLs.
    
    Returns:
        list: A list of URLs found in the text.
    """
    # Regular expression to find URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.findall(text)

def fetch_messages(bot, chat_id):
    """
    Fetches messages from the specified Telegram chat.
    
    Args:
        bot (telegram.Bot): The Telegram bot instance.
        chat_id (str): The ID of the chat to fetch messages from.
    
    Returns:
        list: A list of messages from the chat.
    """
    updates = bot.get_updates()
    messages = []
    for update in updates:
        if update.message and update.message.chat.id == chat_id:
            messages.append(update.message.text)
    return messages

def main():
    """
    Main function to fetch messages from a Telegram chat and extract all links.
    """
    # Initialize the bot with the API token
    bot = Bot(token=API_TOKEN)
    
    # Fetch messages from the specified chat
    messages = fetch_messages(bot, CHAT_ID)
    
    all_links = []
    for message in messages:
        if message:
            # Extract links from each message
            links = extract_links(message)
            all_links.extend(links)
    
    # Print all extracted links
    for link in all_links:
        print(link)

if __name__ == '__main__':
    main()