import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env")
DB_PATH = Path(os.getenv("DB_PATH")).resolve()
KEY_PATH = Path(os.getenv("KEY_PATH")).resolve()