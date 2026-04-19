import os
from config import REGISTRY_DIR

def get_versions(package):
    path = os.path.join(REGISTRY_DIR, package)
    if not os.path.exists(path):
        return []
    
    return sorted(os.listdir(path))

def compare_version(v1, v2):
    return list(map(int, v1.split("."))) >= list(map(int, v2.split(".")))


def resolve_version(package, op, version):
    versions = get_versions(package)
    print("versions", versions)

    if not versions:
        return None
    
    versions.sort(reverse=True)

    for v in versions:
        if not op:
            # If no op specified then choose the latest version by default
            return v
        if op == "==" and v == version:
            return v

        if op == ">=" and compare_version(v, version):
            return v
        if op == "<=" and compare_version(version, v):
            return v
        
    return None

        