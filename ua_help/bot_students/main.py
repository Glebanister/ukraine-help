import argparse
import sys

from pathlib import Path

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.bot_students.student_bot_command_handler import StudentBotCommandHandler
from ua_help.spreadsheet.spreadsheet_driver import SpreadSheetDriver
from ua_help.telegram.telegram_bot import TelegramBot

import logging


def is_test():
    config_index = sys.argv.index('--config')
    config_value = sys.argv[config_index + 1]
    return 'test' in config_value


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=f'bot_student{"test" if is_test() else "release"}.log',
                    filemode='w',
                    level=logging.INFO)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=Path, help='Path to the config file', required=True)
    arg_parser.add_argument('--root', type=Path, help='Path to the root folder (with resources)', required=True)

    args = arg_parser.parse_args()

    logging.info(f'root   = {args.root}')
    logging.info(f'config = {args.config}')

    root = args.root
    config = args.config

    initial_config = StudentTelegramFormConfig(root, config)

    sheets_driver = SpreadSheetDriver(initial_config.gdrive_cred, initial_config.spreadsheet_name)
    bot = TelegramBot(
        lambda chat: StudentBotCommandHandler(
            StudentTelegramFormConfig(root, config),
            lambda row: sheets_driver.append_row(row),
            chat
        ),
        all_commands=[
            'help',
            'start',
            'language',
            'update'
        ],
        config=initial_config
    )

    bot.run()


if __name__ == '__main__':
    main()
