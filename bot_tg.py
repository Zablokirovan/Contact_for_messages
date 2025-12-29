"""
    The logic behind a Telegram bot sending messages
    to a chat user or group of which the bot is a member.
"""
import telebot
import os

from dotenv import load_dotenv
load_dotenv()

BOT = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))
chat_id = os.getenv('TG_USER_ID')


def telegram_send_messages(messages: str) -> None:
    """
    Send messages in group or chat Telegram
    :param messages: str
    :return: None
    """
    BOT.send_message(chat_id, messages)
