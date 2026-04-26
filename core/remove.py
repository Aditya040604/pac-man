import os, shutil
from config import INSTALL_DIR
from core.meta import load_meta
from storage.packages import load_packages, save_packages
from utils.file_ops import delete_package
from core.resolver import parse_dependency
from core.versions import resolve_version


def remove_with_cleanup(package, installed_packages, version):    
    # Remove main package
    

    meta = load_meta(package, version)
    
    # Step 1 : Collect dependencies first
    deps_to_check= []
    if meta:
        for dep in meta.get("dependencies", []):
            dep_name, dep_version = parse_and_resolve_version(dep)
            if dep_name in installed_packages:
                deps_to_check.append((dep_name, dep_version))
    # Step 2: Remove current package

    path = os.path.join(INSTALL_DIR, package, version)

    if os.path.exists(path):
        delete_package(path)

    installed_packages.pop(package)

    print(f"Removed '{package}'")
    
    # Step 3: Now process dependencies
    for dep_name, dep_version in deps_to_check:
        if dep_name in installed_packages and not is_dependency(dep_name, installed_packages):
            remove_with_cleanup(dep_name, installed_packages, dep_version)


def remove(args):
    package = args.package_str
    # T1: Might need to change the way installed version is retreived.Get the version from installed packages.
    name, version = parse_and_resolve_version(package)
    installed_packages = load_packages()

    if name not in installed_packages:
        print(f"{name} is not installed")
        return
    
    dependent = is_dependency(name, installed_packages)

    if dependent:
        print(f"Cannot remove '{name}' -> required by '{dependent}'")
        return

    remove_with_cleanup(name, installed_packages, version)
    save_packages(installed_packages)


def is_dependency(package, installed):
    for pkg,ver in installed.items():
        meta = load_meta(pkg,ver)
        if not meta:
            continue

        for dep in meta.get("dependencies", []):
            dep_name, _, _ = parse_dependency(dep)
            if dep_name == package:
                return pkg
    
    return None

def parse_and_resolve_version(package):
    name, op, ver = parse_dependency(package)
    resolved_version = resolve_version(name, op, ver)
    return name, resolved_version
