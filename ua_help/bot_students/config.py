import json
from pathlib import Path

from ua_help.common import log
from ua_help.localize.language import Language


class StudentTelegramFormConfig:
    def __init__(self, root: Path, config_path: Path):
        resources = root / 'resources'
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
        self.clients_data = Path(raw_json['clients_data'])
        if not self.clients_data.is_absolute():
            raise Exception('Client data path must be absolute')
        self.default_language = Language.from_str(raw_json['default_language'])
        self.priority_choice = resources / raw_json['priority_choice']
        self.languages_notice = resources / raw_json['languages_notice']
        self.fill_instructions = resources / raw_json['fill_instructions']
        self.host_url = raw_json['host_url']
        self.use_webhook = raw_json['use_webhook']
