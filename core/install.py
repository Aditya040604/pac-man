
import os
from core.resolver import build_graph, topo_sort
from storage.packages import load_packages, save_packages
from config import REGISTRY_DIR, INSTALL_DIR
from utils.file_ops import copy_package

def install_with_resolver(package):
    graph = {}
    visited = set()

    # 1. Build graph
    build_graph(package, graph, visited)
    print(graph)

    # 2. Get Correct Order
    order = topo_sort(graph)

    # 3. Load installed packages
    packages = load_packages()

    # 4. Install in order
    for pkg in order:
        if pkg in packages:
            print(f"{pkg} is already installed")
            continue
        src = os.path.join(REGISTRY_DIR, pkg)
        dest = os.path.join(INSTALL_DIR, pkg)

        if not os.path.exists(src):
            print(f"{pkg} not found in registry")
            return
        
        copy_package(src, dest)
        packages.append(pkg)

        print(f"Installed {pkg}")
    save_packages(packages)