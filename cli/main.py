import argparse
import json
import os
import shutil

REGISTRY_DIR = "registry"
INSTALL_DIR = "installed"
DB_FILE = "package.json"

# --- Helpers ---

def load_packages():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)
    
def save_packages(packages):
    with open(DB_FILE, "w") as f:
        json.dump(packages,f )

def load_meta(package):
    path = os.path.join(REGISTRY_DIR, package, "meta.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)
    
# --- Core Logic ---
def install_package(package, installed):
    if package in installed:
        print(f"{package} already installed")
        return True # Success
    meta = load_meta(package)

    if not meta:
        print(f"Package `{package}` not found in registry")
        return False # Failure
    
    # install dependencies first
    for dep in meta.get("dependencies", []):
        success = install_package(dep, installed)
        if not success:
            print(f"Failed to install dependecy '{dep}' for '{package}'")
            return False # Stop immediately
    
    # Copy files
    src = os.path.join(REGISTRY_DIR, package)
    dest = os.path.join(INSTALL_DIR, package)

    os.makedirs(INSTALL_DIR,exist_ok=True)
    try:

        shutil.copytree(src, dest, dirs_exist_ok=True)
    except Exception as e:
        print(f"Error Installing {package}: {e}")
        return False

    installed.append(package)
    print(f"Installed {package}")
    return True

# check who depends on this package
def is_dependency(package, installed):
    for pkg in installed:
        meta = load_meta(pkg)
        if not meta:
            continue
        if package in meta.get("dependencies", []):
            return pkg # return dependent package
    
    return None

# Build Graph
def build_graph(package, graph, visited):
    if package in visited:
        return
    visited.add(package)
    meta = load_meta(package)
    if not meta:
        raise Exception(f"Package '{package}' not found")
    deps = meta.get("dependencies", [])
    graph[package] = deps

    for dep in deps:
        build_graph(dep, graph, visited)

# Topological Sort
def topo_sort(graph):
    visited = set()
    temp = set()
    order = []




    


def install(args):
    installed = load_packages()

    install_package(args.package, installed)
    save_packages(installed)

def remove(args):
    installed = load_packages()
    if args.package not in installed:
        print("Not Installed")
        return 
    dependent = is_dependency(args.package, installed)
    if dependent:
        print(f"Cannot remove '{args.package}' -> required by '{dependent}'")
        return
    path = os.path.join(INSTALL_DIR, args.package)

    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        print(f"Warning: files for {args.package} not found")
    
    installed.remove(args.package)
    save_packages(installed)

    print(f"Removed {args.package}")

def list_packages(args):
    packages = load_packages()

    if not packages:
        print("No packages installed")
        return 
    print("Installed packages:")
    for pkg in packages:
        print("-", pkg)



# --- CLI Setup

def main():
    parser = argparse.ArgumentParser(prog="mypm")
    subparsers = parser.add_subparsers(dest="command")

    # install command
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("package")
    install_parser.set_defaults(func=install)

    # remove command
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("package")
    remove_parser.set_defaults(func=remove)


    # list command
    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_packages)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

  

   




if __name__ == "__main__":
    main()

