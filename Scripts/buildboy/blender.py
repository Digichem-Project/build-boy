# Code for building blender and beautiful atoms.

import os
from pathlib import Path
import subprocess
import tempfile
import zipfile
import urllib.request

from buildboy.util import expand_path, update_repo

def build_blender(target, basedir = "~/blender", branch = "main", build_target = "headless"):

    basedir = expand_path(basedir)
    
    # Switch to the build dir.
    os.chdir(Path(basedir, "src"))

    # Update the repo (incase we changed branches).
    update_repo(".", branch=branch)

    # Update libraries.
    subprocess.run(["./build_files/utils/make_update.py", "--use-linux-libraries"], universal_newlines = True, check = True)

    # Update src.
    subprocess.run(["make", "update"], universal_newlines = True, check = True)

    # Build.
    subprocess.run(["make", build_target], universal_newlines = True, check = True)

    target_dir = "build_linux_{}".format(build_target) if build_target is not None else "build_linux"
    
    # Install batoms.
    # First, download batoms to a temp dir.
    with tempfile.TemporaryDirectory() as temp_dir:
        print("Downloading batoms...")
        urllib.request.urlretrieve("https://github.com/beautiful-atoms/beautiful-atoms/archive/refs/heads/main.zip", Path(temp_dir, "batoms.zip"))

        print("Extracting archive...")
        with zipfile.ZipFile(Path(temp_dir, "batoms.zip"), 'r') as zip_ref:
            zip_ref.extractall(Path(temp_dir))

        # Remove the archive, we no longer need it.
        Path(temp_dir, "batoms.zip").unlink()

        print("Installing into blender...")
        batoms_dir = Path(temp_dir, "beautiful-atoms-main", "batoms")

        # Then install into blender.
        batoms_dir.rename(Path(basedir, target_dir, "bin", target,  "scripts/addons_core", "batoms"))


    # Next install dependencies.
    print("Installing dependencies..")
    os.chdir(Path(basedir, target_dir, "bin", target, "python/bin"))

    # Determine the python version.
    pythons = list(Path("./").glob("python*"))

    if len(pythons) == 0:
        raise Exception("Could not determine blender's python version")
    
    python = "./" + pythons[-1].name

    # Install depends.
    subprocess.run([python, "-m", "ensurepip"], universal_newlines = True, check = True)
    subprocess.run([python, "-m", "pip", "install", "--upgrade", "pip"], universal_newlines = True, check = True)
    subprocess.run(["./pip3", "install", "--upgrade", "ase"], universal_newlines = True, check = True)
    subprocess.run(["./pip3", "install", "scikit-image", "pyyaml"], universal_newlines = True, check = True)

    archive_name = "blender-{}-batoms.tar.gz".format(target)

    # Archive.
    os.chdir(Path(basedir, target_dir))
    Path("bin").rename("blender")
    subprocess.run(["tar", "-czf", archive_name, "blender"], universal_newlines = True, check = True)

    return {
        "dir": Path(basedir, target_dir, "blender").resolve(),
        "archive": Path(basedir, target_dir, archive_name).resolve()
    }
