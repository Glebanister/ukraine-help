from pathlib import Path
from typing import List, Tuple

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ua_help.common.log import LOGGER


class SpreadSheetDriver:
    def __init__(self, credentials_file_path: Path, spreadsheet_title: str):
        LOGGER.info(f'Initialize credentials from {credentials_file_path}')
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            str(credentials_file_path),
            [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file'
            ]
        )
        LOGGER.info(f'Spreadsheet credentials initialized')
        LOGGER.info('Spreadsheet initializing client with credentials')
        self.client = gspread.authorize(self.credentials)
        LOGGER.info('Spreadsheet client initialized')
        self.sheet = self.client.open(spreadsheet_title).sheet1

    def append_row(self, row: List[Tuple[str, str]]):
        LOGGER.debug('Spreadsheet append row: {row}')
        self.sheet.append_row(list(map(lambda kv: kv[1], row)))
