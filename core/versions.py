import os
from config import REGISTRY_DIR

def get_versions(package):
    path = os.path.join(REGISTRY_DIR, package)
    if not os.path.exists(path):
        return []
    
    return sorted(os.listdir(path))

def compare_version(v1, v2):
    return tuple(map(int, v1.split("."))) >= tuple(map(int, v2.split(".")))

def version_key(v):
    return tuple(map(int, v.split(".")))

def resolve_version(package, op, version):
    available_versions = get_versions(package)
    print("versions", available_versions)

    if not available_versions:
        return None
    

    available_versions.sort(key=version_key,reverse=True)

    for v in available_versions:
        if not op:
            # If no op specified then choose the latest version by default
            return v
        
        if op == ">" and version_key(v) > version_key(version):
            return v
        if op == "<" and version_key(v) < version_key(v):
            return v

        if op == "==" and v == version:
            return v

        if op == ">=" and compare_version(v, version):
            return v
        if op == "<=" and compare_version(version, v):
            return v
        
    return None

        