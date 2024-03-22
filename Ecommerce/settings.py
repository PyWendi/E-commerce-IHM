from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE_PATH = BASE_DIR / ".env"

load_dotenv(str(ENV_FILE_PATH))

print(os.getenv('SECRET_KEY'))

DEBUG = True if (os.getenv("DEBUG_MODE") == "True") else False

if os.getenv('DEBUG_MODE') == 'True':
    from .sub_settings.setting_dev import *
else:
    from .sub_settings.setting_prod import *