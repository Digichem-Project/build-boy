import sys
import os
from pathlib import Path
import shutil
import subprocess
import re

def expand_path(pth):
    """Perform shell-like expansion on a path."""
    pth = os.path.expanduser(pth)
    pth = os.path.expandvars(pth)
    return pth

def build_target(
    basedir,
    target,
    branch = "main",
    freezeargs = None
):
    freezeargs = freezeargs if freezeargs is not None else []
    basedir = expand_path(basedir)

    # Switch to the build dir.
    os.chdir(Path(basedir, "freeze", 'general'))

    # Cleanup any previous builds.
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)

    # Change branches.
    subprocess.run([
        'git', 'checkout', branch
    ], universal_newlines = True, check = True)

    # Get the latest version from git.
    # WARNING: This will forcibly update and remove local files.
    subprocess.run([
       'git', 'fetch', 'origin'
    ], universal_newlines = True, check = True)
    subprocess.run([
       'git', 'reset', '--hard', 'origin/' + branch
    ], universal_newlines = True, check = True)
    #subprocess.run([
    #    'git', 'pull', 'origin'
    #], universal_newlines = True, check = True)

    # Now build.
    sig = ['./freeze', target]
    sig.extend(freezeargs)
    subprocess.run(sig, universal_newlines = True, check = True)

    # We should have two files in the 'dist' dir, the build folder and the archive.
    _paths = list(Path("dist").glob("*"))
    paths = {}

    for path in _paths:
        if path.is_dir():
            paths['dir'] = path.resolve()
        
        elif path.suffixes[-2:] == ['.tar', '.gz']:
            paths['archive'] = path.resolve()
    
    if len(paths) != 2:
        raise Exception("Build error, incorrect number of files in dist dir: {}".format(paths))
    
    return paths

def build_oprattle(target):
    """Build openprattle; a stand-in for openbabel"""
    return build_target("~/openprattle", target)

def build_silico(target, prattledir):
    """Build silico"""
    return build_target("~/silico", target = target, branch = "build", freezeargs = [prattledir])

def build(target, branch = "build"):
    # Disable git prompting.
    os.environ['GIT_TERMINAL_PROMPT'] = "0"

    # First, make sure we're up to date.
    #print("---------------------")
    #print("Updating Build-boy...")
    #print("---------------------")
    #subprocess.run(['git', 'checkout', 'main'], universal_newlines = True, check = True)
    #subprocess.run(['git', 'pull', 'origin'], universal_newlines = True, check = True)

    print("-----------------------------")
    print("Checking for a new version...")
    print("-----------------------------")
    # First, check if there's a new version to build.
    # Get the last version we did.
    with open(Path('../../Builds', target, 'version')) as v_file:
        last_version = v_file.read().strip()

    # Now get the latest version.
    os.chdir(expand_path('~/silico'))
    # Checkout.
    subprocess.run([
        'git', 'checkout', branch
    ], universal_newlines = True, check = True)
    # Get the latest version from git.
    subprocess.run([
       'git', 'fetch', 'origin'
    ], universal_newlines = True, check = True)
    subprocess.run([
       'git', 'reset', '--hard', 'origin/' + branch
    ], universal_newlines = True, check = True)

    import silico
    import openprattle
    if silico.__version__.strip() == last_version:
        # Nothing new.
        print("build-boy: Nothing to do, last built version was '{}', current version is '{}'".format(last_version, silico.__version__))
        exit()

    # Work to be done.

    print("-----------------------")
    print("Building openprattle...")
    print("-----------------------")
    oprattle_paths = build_oprattle(target)

    print("--------------------")
    print("Building digichem...")
    print("--------------------")
    silico_paths = build_silico(target, oprattle_paths['dir'])

    # Change back to build-boy's dir.
    build_dir = Path(expand_path("~/build-boy/Builds"), target)
    os.chdir(Path(expand_path("~/build-boy/Builds"), target))

    # Update the version.
    with open('version', 'wt') as v_file:
        v_file.write("{}\n".format(silico.__version__))

    # Copy the LICENSES folder for easier viewing.
    shutil.rmtree(Path(build_dir, 'LICENSES'), ignore_errors = True)
    shutil.copytree(
        Path(silico_paths['dir'], '_internal', 'LICENSES'),
        Path(build_dir, 'LICENSES'),
        copy_function = shutil.copy)
    
    # And also the main Digichem license.
    shutil.copy(Path(silico_paths['dir'], "LICENSE"), Path(build_dir))

    # Commit the new version.
    subprocess.run([
        "git", "add", "."
    ], universal_newlines = True, check = True)
    subprocess.run([
        'git', 'commit', '-m', 'Build version {} on {}'.format(silico.__version__, target)
    ], universal_newlines = True, check = True)

    tag = '{}-{}'.format(silico.__version__, target)
    # Tag it.
    subprocess.run([
        'git', 'tag', '-a', tag, '-m', 'Build of version {} on {}'.format(silico.__version__, target)
    ], universal_newlines = True, check = True)

    # Upload to the server.
    subprocess.run(['git', 'push', 'origin'],
        universal_newlines = True, check = True)
    # Also the tag
    subprocess.run(['git', 'push', 'origin', tag],
        universal_newlines = True, check = True)

    # Now create a github release and attach the build.
    sig = [
        'gh', 'release', 'create', tag, silico_paths['archive'],
        '--notes',
            'Automated build of Digichem v{} for the {} system.\n'.format(silico.__version__, target) +\
            'Bundled with Openprattle v{}\n\n'.format(openprattle.__version__) +\
            'Built by the hard-working Build-boy.',
        '--title', 'Digichem version {} for {}'.format(silico.__version__, target)
    ]
    # Add pre-release if necessary.
    if silico.development:
        sig.append('-p')

    # Upload
    subprocess.run(sig, universal_newlines = True, check = True)

    #https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.3-CentOS-Stream-8/digichem.6.0.0-pre.3.CentOS-Stream-8.tar.gz
    download_link = "https://github.com/Digichem-Project/build-boy/releases/download/{}-{}/{}-{}.tar.gz".format(
        silico.__version__,
        target,
        silico.__version__,
        target
    )
    print(download_link)

    # All done, update the main README with the latest version.
    with open("../../README.md", "r") as readme_file:
        readme_data = readme_file.read()
    
    readme_data = re.sub(
        r"<!-- " + re.escape(target) + r" -->.*",
        "<!-- " + target + " --> [{}]({})".format(
            silico.__version__,
            download_link
        ),
        readme_data
    )
    with open("../../README.md", "w") as readme_file:
        readme_file.write(readme_data)

    # All done.
