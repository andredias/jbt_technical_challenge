import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

ENV: str = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. '
        "It should be 'production', 'development' or 'testing'"
    )
DEBUG: bool = ENV != 'production'
TESTING: bool = ENV == 'testing'

LOG_LEVEL: str = os.getenv('LOG_LEVEL') or (DEBUG and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'

# Authentication
SECRET_KEY: str = os.getenv('SECRET_KEY', '') or secrets.token_urlsafe(32)
TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=60)
ALGORITHM: str = 'HS256'

# Drone data
USERNAME: str = 'drone'
PASSWORD: str = '1234'
DRONE_ID: int = 1
