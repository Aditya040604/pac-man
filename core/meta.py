import json, os
from config import REGISTRY_DIR


def load_meta(package, version):
    if not version:
        raise ValueError(f"No version resolved for {package}")
    path = os.path.join(REGISTRY_DIR, package,version ,"meta.json")
    # print("Path:", path)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)