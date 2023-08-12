import subprocess
import pkg_resources
pkgs = [pkg.key for pkg in pkg_resources.working_set]

for pkg in pkgs:
    subprocess.call(['pip','uninstall', '-y',pkg])