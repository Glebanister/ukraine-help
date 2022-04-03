from pathlib import Path

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.bot_students.student_bot_command_handler import StudentBotCommandHandler
from ua_help.spreadsheet.spreadsheet_driver import SpreadSheetDriver
from ua_help.telegram.telegram_bot import TelegramBot

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    root = Path('.')
    initial_config = StudentTelegramFormConfig(root)
    sheets_driver = SpreadSheetDriver(initial_config.gdrive_cred, initial_config.spreadsheet_name)
    bot = TelegramBot(
        initial_config.telegram_bot_token,
        lambda chat: StudentBotCommandHandler(
            StudentTelegramFormConfig(root),
            lambda row: sheets_driver.append_row(row),
            chat
        ),
        [
            'help',
            'start',
            'language',
            'update'
        ]
    )

    bot.run()


if __name__ == '__main__':
    main()
