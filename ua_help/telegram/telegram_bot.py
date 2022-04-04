import os
from typing import Callable, Dict, List

import telegram.ext
from telegram import Update, Chat
from telegram.ext import Filters, MessageHandler, CallbackQueryHandler, CallbackContext

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.common.command_handler import CommandHandler


class TelegramBot:
    def __init__(
            self,
            command_handler_producer: Callable[[Chat], CommandHandler],
            all_commands: List[str],
            config: StudentTelegramFormConfig
    ):
        self.command_handler_producer = command_handler_producer
        self.all_chats: Dict[Chat, CommandHandler] = {}
        self.updater = telegram.ext.Updater(config.telegram_bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.config = config

        def get_chat_handler(chat: Chat) -> CommandHandler:
            if chat.id not in self.all_chats:
                self.all_chats[chat.id] = self.command_handler_producer(chat)
            return self.all_chats[chat.id]

        def command_wrapper(command: str):
            def handle(update: Update, context: CallbackContext):
                chat_handler = get_chat_handler(update.effective_chat)
                chat_handler.handle_command(command, (update, context))

            return handle

        def user_message_handler(update: Update, context: CallbackContext):
            chat_handler = get_chat_handler(update.effective_chat)
            chat_handler.handle_input(update.message.text, (update, context))

        def query_handler(update: Update, context: CallbackContext):
            chat_handler = get_chat_handler(update.effective_chat)
            chat_handler.handle_input(update.callback_query.data, (update, context))

        for command_of_handler in all_commands:
            self.dispatcher.add_handler(telegram.ext.CommandHandler(
                command_of_handler,
                command_wrapper(command_of_handler)
            ))

        self.dispatcher.add_handler(MessageHandler(
            Filters.text & (~Filters.command),
            user_message_handler
        ))

        self.dispatcher.add_handler(CallbackQueryHandler(
            query_handler
        ))

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
