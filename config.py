import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))


REGISTRY_DIR = os.path.join(BASEDIR,"registry")
INSTALL_DIR = os.path.join(BASEDIR, "installed")
DB_FILE = os.path.join(BASEDIR, "package.json")