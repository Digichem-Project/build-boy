# General miscellaneous utilities that should probably belong somewhere else.

import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
import copy
import time
import fabric

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

@contextmanager
def start_vm(vm_data, shutdown_on_error = True):
    """Start a virtual machine, returning an SSH object that can be used to communicate with it."""
    try:
        # First, we need to wake up the VM.
        print("Waking VM...")
        subprocess.run([
            'vboxmanage', 'startvm', vm_data['vm'], "--type=headless"
        ], universal_newlines = True, check = True)

        # Some VMs (Rocky 9 in particular) take a lot of attempts to connect...
        attempt = 0
        exception = None
        while attempt < 5:
            try:
                # Wait a little bit for the VM to start.
                print("Waiting for boot...")
                time.sleep(120)

                # Get our connection options.
                connect_kwargs = copy.copy(vm_data['connect_kwargs'])
                # The PC just turned on, give it some time to wake-up:
                connect_kwargs['timeout'] = 300 # 5 mins
                connect_kwargs['banner_timeout'] = 300

                # Next, connect with SSH.
                print("Connecting to VM...")
                with fabric.Connection(
                    'localhost',
                    user="digichem",
                    port=vm_data['port'],
                    connect_kwargs = connect_kwargs
                ) as ssh:

                    yield ssh
                
                # All done.
                exception = None
                break

            except ConnectionError as e:
                attempt += 1
                exception = e
        
        if exception:
            raise exception
    
    except:
        if shutdown_on_error:
            # Ask the VM to stop.
            subprocess.run([
                'vboxmanage', 'controlvm', vm_data['vm'], "acpipowerbutton"
            ], universal_newlines = True, check = False)

            time.sleep(10)

            # Make sure it is dead.
            subprocess.run([
                'vboxmanage', 'controlvm', vm_data['vm'], "poweroff"
            ], universal_newlines = True, check = False)

        raise
