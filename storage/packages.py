import json, os
from config import DB_FILE


def load_packages():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)
    
def save_packages(packages):
    with open(DB_FILE, "w") as f:
        json.dump(packages,f )