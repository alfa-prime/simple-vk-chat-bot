from pathlib import Path
from dotenv import load_dotenv
import os

def load_env_values():
    """ загружает переменные окружения из .env файла """
    env_file_path = Path.cwd() / 'application' / 'settings' / '.env'
    return load_dotenv(env_file_path) if env_file_path.exists() else False


if load_env_values():
    BOT_TOKEN = os.getenv('bot_token')
