import json
from pathlib import Path

from ua_help.common import log


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
        self.subjects_file = resources / raw_json['subjects']
        self.gdrive_cred = resources / raw_json['google_drive_credentials']
        self.telegram_bot_token = raw_json['telegram_bot_token']
