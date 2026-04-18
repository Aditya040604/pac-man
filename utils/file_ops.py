import os, shutil

def copy_package(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok=True)

def delete_package(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        