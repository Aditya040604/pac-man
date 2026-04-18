import json, os
from config import REGISTRY_DIR


def load_meta(package):
    path = os.path.join(REGISTRY_DIR, package, "meta.json")
    # print("Path:", path)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)