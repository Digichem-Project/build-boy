# General miscellaneous utilities that should probably belong somewhere else.

import os
import subprocess
from pathlib import Path

def expand_path(pth):
    """Perform shell-like expansion on a path."""
    pth = os.path.expanduser(pth)
    pth = os.path.expandvars(pth)
    return pth

def update_repo(repo_path, branch = "main", upstream = "origin"):
    """
    Forcibly update a local repo from origin.
    """
    print("Updating '{}' to '{}/{}'".format(repo_path, upstream, branch))
    start_dir = Path(os.getcwd()).resolve()
    try:
        os.chdir(repo_path)

        # Checkout.
        # TODO: Checkout could fail if there are untracked files, but best to stop then anyway.
        subprocess.run([
            'git', 'checkout', branch
        ], universal_newlines = True, check = True)
        # Get the latest version from git.
        subprocess.run([
        'git', 'fetch', upstream
        ], universal_newlines = True, check = True)
        subprocess.run([
        'git', 'reset', '--hard', upstream+ '/' + branch
        ], universal_newlines = True, check = True)
    
    finally:
        os.chdir(start_dir)