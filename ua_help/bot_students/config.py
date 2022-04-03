import json
from pathlib import Path

from ua_help.common import log
from ua_help.localize.language import Language


class StudentTelegramFormConfig:
    def __init__(self, root: Path):
        resources = root / 'resources'
        config_path = resources / 'config.json'
        log.LOGGER.info(f'Config load from {config_path}')
        with config_path.open('r') as config_file:
            raw_json = json.loads(config_file.read())
            log.LOGGER.info(f'Execute with config: {raw_json}')
        self.spreadsheet_name = raw_json['spreadsheet_name']
        self.log_file = raw_json['log_file']
        self.intro_folder = resources / raw_json['intro']
        self.help_folder = resources / raw_json['help']
        self.subjects_file = resources / raw_json['subjects']
        self.gdrive_cred = resources / raw_json['google_drive_credentials']
        self.telegram_bot_token = raw_json['telegram_bot_token']
        self.clients_data = root / raw_json['clients_data']
        self.default_language = Language.from_str(raw_json['default_language'])
        self.priority_choice = resources / raw_json['priority_choice']
        self.languages_notice = resources / raw_json['languages_notice']
