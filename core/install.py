
import os
from core.resolver import build_graph, topo_sort
from storage.packages import load_packages, save_packages, extract_packages
from config import REGISTRY_DIR, INSTALL_DIR
from utils.file_ops import copy_package
from core.resolver import parse_dependency
from core.versions import resolve_version

def install_with_resolver(package_str):
    graph = {}
    visited = set()

    name, op, ver = parse_dependency(package_str)
    print(name, op, ver)
    resolved_version = resolve_version(name, op, ver)
    print(resolved_version)
    
    if not resolved_version:
        raise Exception(f"Cannot resolve {package_str}")
    
    root = (name, resolved_version)

    # 1. Build graph
    build_graph(root, graph, visited)
    print(graph)

    # 2. Get Correct Order
    order = topo_sort(graph)
    print("Order:", order)

    # 3. Load installed packages
    packages = load_packages()

    # 4. Pre-check
    for name, version in order:
        path = os.path.join(REGISTRY_DIR, name, version)
        if not os.path.exists(path):
            raise Exception(f"{name}=={version} not found in registry.")

    # 5. Install in order
    for name, version in order:
        if name in packages:
            if packages[name] == version:
                print(f"{name} is already installed")
                continue
            else:
                print(f"Upgrading {name}: {packages[name]} -> {version}")
        src = os.path.join(REGISTRY_DIR, name, version)
        dest = os.path.join(INSTALL_DIR, name, version)
        
        copy_package(src, dest)

        print(f"Installed {name} == {version}")

    # 6. Flatten + merge
    extracted_packages = extract_packages(graph)
    packages.update(extracted_packages)
    save_packages(packages)