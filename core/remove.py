import os, shutil
from config import INSTALL_DIR
from core.meta import load_meta
from storage.packages import load_packages, save_packages
from utils.file_ops import copy_package, delete_package

def remove_with_cleanup(package, installed_packages):    
    # Remove main package
    path = os.path.join(INSTALL_DIR, package)

    if os.path.exists(path):
        delete_package(path)

    installed_packages.pop(package)

    print(f"Removed '{package}'")

    meta = load_meta(package)
    
    if not meta:
        return
    
    for dep in meta.get("dependencies", []):
        if dep in installed_packages and not is_dependency(dep, installed_packages):
            remove_with_cleanup(dep, installed_packages)

# Problem: Right now, always newly installed version will replace the old package in the installed packages json. So, for now there is no need of version checking before removing packages.


def remove(args):
    # Task: change the args.package to args.package_str and update the code to remove packages based on version
    package = args.package_str
    installed_packages = load_packages()

    if package not in installed_packages:
        print(f"{package} is not installed")
        return
    
    dependent = is_dependency(package, installed_packages)

    if dependent:
        print(f"Cannot remove '{package}' -> required by '{dependent}'")
        return

    remove_with_cleanup(args.package, installed_packages)
    save_packages(installed_packages)


def is_dependency(package, installed):
    for pkg in installed:
        meta = load_meta(pkg)
        if not meta:
            continue
        if package in meta.get("dependencies", []):
            return pkg # return dependent package
    
    return None