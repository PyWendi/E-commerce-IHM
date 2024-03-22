from dotenv import dotenv_values
import os


env = dotenv_values("../.env")


DEBUG = True if (env.get("DEBUG_MODE") == "True") else False

if env.get('DEBUG_MODE') == 'True':
    from .sub_settings.setting_dev import *
else:
    from .sub_settings.setting_prod import *