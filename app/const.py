from datetime import datetime

LOG_FORM = '%(asctime)s, %(levelname)s, %(message)s'
LOG_FILEMOD = 'w'
LOG_FILENAME = 'logger.log'
LOGS_DIR = 'logs'
YEARS = [str(year) for year in range(2019, datetime.now().year + 1)]
MONTHS = [f"{month:02}" for month in range(1, 13)]
DAYS = [f"{day:02}" for day in range(1, 32)]

REGULAR_FOR_MATCH = r'prog(\d+)_'
REGULAR_FOR_SEARCH = r'(\d{1,2}-\d{1,2}-\d{4})'

EXTRACT_PROG_DATE = '%d-%m-%Y'
SELECT_PROG_DATE = '%Y-%m-%d'

TEXT_COLOR = (1, 1, 1, 1)
BACKGROUND_COLOR_CHOICE = (46 / 255, 46 / 255, 46 / 255, 1)
BACKGROUND_COLOR_NOT_ACTIVE = (0.1, 0.1, 0.1, 0.8)
