from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(str(ENV_FILE_PATH))

DEBUG = True if (os.getenv("DEBUG") == "True") else False

if DEBUG:
    from .sub_settings.setting_dev import *
else:
    from .sub_settings.setting_prod import *