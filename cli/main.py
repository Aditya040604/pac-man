import argparse
from core.install import install_with_resolver
from core.remove import remove
from storage.packages import load_packages


def install(args):
    
    install_with_resolver(args.package_str)

def list_packages(args):
    packages = load_packages()

    if not packages:
        print("No packages installed")
        return 
    print("Installed packages:")
    for pkg, version in packages.items():
    #  Check the packages alignment in the console; it's a bit off. Fix this last
        print("-", pkg, " ", version)



# --- CLI Setup
def main():
    parser = argparse.ArgumentParser(prog="pac-man")
    subparsers = parser.add_subparsers(dest="command")

    # install command
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("package_str")
    install_parser.set_defaults(func=install)

    # remove command
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("package_str")
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

