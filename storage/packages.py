import json, os
from config import DB_FILE


def load_packages():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)
    
def save_packages(packages):
    with open(DB_FILE, "w") as f:
        json.dump(packages,f, indent=4 )
    
    print("Saved Installed Packages")
    for name, version in packages.items():
        print(f"{name} == {version}")

def extract_packages(graph):
    packages = {}
    for pkg, deps in graph.items():
        name, version = pkg
        packages[name] = version
        for dep in deps:
            dep_name, dep_ver = dep
            packages[dep_name] = dep_ver
    return packages



