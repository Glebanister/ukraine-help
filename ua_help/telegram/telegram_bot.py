import enum
import queue
from typing import Callable, List, Dict

import telegram.ext
from telegram import Update, Chat
from telegram.ext import Filters, MessageHandler, CallbackContext

from ua_help.common.command_handler import CommandHandler


class MessageBuilder:
    def __init__(self):
        self.parts: List[str] = []

    def __call__(self, *args, **kwargs):
        self.parts.extend([*args])

    def send_to_user(self, update: Update, context: CallbackContext):
        bot_response = '\n'.join(self.parts)
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)


class TelegramBot:
    def __init__(
            self,
            token: str,
            command_handler_producer: Callable[[], CommandHandler]
    ):
        self.command_handler_producer = command_handler_producer
        self.all_chats: Dict[Chat, CommandHandler] = {}
        self.updater = telegram.ext.Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher


        def get_chat_handler(chat: Chat) -> CommandHandler:
            if chat not in self.all_chats:
                self.all_chats[chat] = self.command_handler_producer()
            return self.all_chats[chat]

        def command_wrapper(command: str):
            def handle(update: Update, context: telegram.ext.CallbackContext):
                chat = update.effective_chat.id
                chat_handler = get_chat_handler(chat)
                message_builder = MessageBuilder()
                chat_handler.handle_command(command, message_builder)
                message_builder.send_to_user(update, context)
                context.bot.getWebhookInfo

            return handle

        def user_message_handler(update: Update, context: telegram.ext.CallbackContext):
            chat = update.effective_chat.id
            chat_handler = get_chat_handler(chat)
            message_builder = MessageBuilder()
            chat_handler.handle_input(update.message.text, message_builder)
            message_builder.send_to_user(update, context)

        for command_of_handler in self.command_handler_producer().get_all_commands():
            self.dispatcher.add_handler(telegram.ext.CommandHandler(
                command_of_handler,
                command_wrapper(command_of_handler)
            ))

        self.dispatcher.add_handler(MessageHandler(
            Filters.text & (~Filters.command),
            user_message_handler
        ))

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
