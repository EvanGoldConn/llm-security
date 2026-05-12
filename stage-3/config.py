

#load .env file & set mode flag (controls mock vs real tools)

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() #read env file, parse each key=value line & load em into the process environment so os can see them, bridge b/n .env & os.getenv()

MODE = os.getenv("MODE", "mock")
DISCOVERY_AGENT_MODEL = os.getenv("DISCOVERY_AGENT_MODEL", "qwen2.5:7b")
ACCESS_AGENT_MODEL = os.getenv("ACCESS_AGENT_MODEL", "claude-haiku-4-5-20251001")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "llama3.1:8b")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
MOCK_NETWORK_FILE = DATA_DIR / "mock_network.json"


print(BASE_DIR)