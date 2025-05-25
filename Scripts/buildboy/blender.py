# Code for building blender and beautiful atoms.

import os
import os.path
from pathlib import Path
import subprocess
import tempfile
import zipfile
import urllib.request
import shutil
import tarfile

from buildboy.util import expand_path, update_repo

def grab_blender(digichem_target, os_target = "CentOS-Stream-8", blender_target = "4.4",  basedir = "~/blender"):
    """
    Download a pre-built version of blender (for OS's that don't support building).
    """
    basedir = expand_path(basedir)
    archive_name = "blender.{}.batoms.{}.tar.gz".format(blender_target, os_target)

    url = "https://github.com/Digichem-Project/build-boy/releases/download/{}-{}/{}".format(
        digichem_target,
        os_target,
        archive_name
    )

    # Download.
    urllib.request.urlretrieve(url, Path(basedir, archive_name))

    # Extract
    with tarfile.open(Path(basedir, archive_name)) as tar:
        tar.extractall(basedir, filter = "data")

        # Done.
        return {
            "dir": Path(basedir, os.path.commonpath(tar.getnames())).resolve(),
            "archive": Path(basedir, archive_name).resolve()
        }
    

def build_blender(os_target, target = "4.4", basedir = "~/blender", branch = "blender-v4.4-release", build_target = "headless"):
    """
    Build blender on this system.

    :param target: The version of blender to build.
    :param basedir: The directory to build in. Inside should be a 'src' directory containing the blender repo.
    :param branch: The git branch to build from, ideally should match 'target'.
    :param build_target: The type of build to pass to make.
    """

    basedir = expand_path(basedir)
    target_dir = "build_linux_{}".format(build_target) if build_target is not None else "build_linux"
    archive_name = "blender.{}.batoms.{}.tar.gz".format(target, os_target)

    # Switch to the build dir.
    os.chdir(Path(basedir, "src"))

    # Update the repo (incase we changed branches).
    update_repo(".", branch=branch)

    # Update libraries.
    subprocess.run(["./build_files/utils/make_update.py", "--use-linux-libraries"], universal_newlines = True, check = True)

    # Update src.
    subprocess.run(["make", "update"], universal_newlines = True, check = True)

    # Remove the old python dir incase of conflicts with batoms or pip installation.
    try:
        shutil.rmtree(Path(basedir, target_dir))
    except FileNotFoundError:
        pass

    # Build.
    subprocess.run(["make", build_target, "ccache"], universal_newlines = True, check = True)
    
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

        batoms_install_dir = Path(basedir, target_dir, "bin", target,  "scripts/addons_core", "batoms")
        # Then install into blender.
        # First remove any previous install if present.
        try:
            shutil.rmtree(batoms_install_dir)
        except FileNotFoundError:
            pass
            
        batoms_dir.rename(batoms_install_dir)


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

    # Archive.
    os.chdir(Path(basedir, target_dir))

    try:
        shutil.rmtree("blender")
    except FileNotFoundError:
        pass
    Path("bin").rename("blender")

    print("Creating archive...")
    subprocess.run(["tar", "-czf", archive_name, "blender"], universal_newlines = True, check = True)

    return {
        "dir": Path(basedir, target_dir, "blender").resolve(),
        "archive": Path(basedir, target_dir, archive_name).resolve()
    }
