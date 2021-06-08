from pathlib import Path
from dotenv import load_dotenv
import os

def load_env_values():
    """ загружает переменные окружения из .env файла """
    root_dir = Path(__file__).parent.parent.parent
    env_file_path = root_dir / '.env'
    return load_dotenv(env_file_path) if env_file_path.exists() else False


if load_env_values():
    BOT_TOKEN = os.getenv('bot_token')
    USER_TOKEN = os.getenv('user_token')
    APP_ID = os.getenv('app_id')
    API_VERSION = os.getenv('api_version')
    DATABASE = os.getenv('database')
