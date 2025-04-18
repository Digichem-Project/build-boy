import sys
import os
from pathlib import Path
import shutil
import subprocess
import re
import json

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

    update_repo(".", branch=branch)

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
    with open(Path('../../Builds', target, 'status')) as v_file:
        last_data = json.load(v_file)

    # Now get the latest version of repos that we'll need.
    update_repo(expand_path('~/silico'), "build")
    update_repo(expand_path('~/cclib'), "master")
    update_repo(expand_path('~/configurables'))
    update_repo(expand_path('~/digichem-core'))
    update_repo(expand_path('~/openprattle'))
    update_repo(expand_path('~/pysoc'), "master")

    os.chdir(expand_path('~/silico'))

    import silico
    import openprattle
    import digichem
    if silico.__version__.strip() == last_data.get('version', ""):
        # Nothing new.
        print("build-boy: Nothing to do, last built version was '{}', current version is '{}'".format(last_data.get('version', ""), silico.__version__))
        exit()

    # Update data.
    new_data = {
        'version': silico.__version__,
        'commit': subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], capture_output=True, universal_newlines=True, check=True).stdout.strip()
    }
    # If this is a major version, update that too.
    if not silico.development:
        new_data['release_version'] = new_data['version']
        new_data['release_commit'] = new_data['commit']

    # Get a list of changes for later.
    # If it's a release (!development), show from the last release version.
    if silico.development:
        last_commit = last_data.get('commit', "")
        last_version = last_data.get('version', "")
    
    else:
        last_commit = last_data.get('release_commit', "")
        last_version = last_data.get('release_version', "")

    # Get changes from git
    raw_changes = subprocess.run([
        'git', 'log', '--pretty=format:%as: %s', '--ancestry-path', '{}..{}'.format(
            # Old version.
            last_commit,
            # New version.
            "HEAD"
        )
        ], capture_output = True, universal_newlines = True, check = True).stdout.strip().split("\n")

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
    with open('status', 'wt') as v_file:
        v_file.write(json.dumps(new_data))

    # Write a changelog.
    # What we compare to depends on what type of release this is.
    # If this is a development version, just show from the last development version.
    changes = {
        'New features': [],
        'Bugfixes': [],
        'Documentation changes': [],
        'Testing updates': [],
        'Miscellaneous': []
    }
    # Only keep semantic commits, and split by type.
    for raw_change in raw_changes:
        try:
            change_split = raw_change.split(" ")
            date = change_split[0]
            change_type = change_split[1]
            message = " ".join(change_split[2:])

            if change_type.lower() == "feat:":
                dest = "New features"
            
            elif change_type.lower() == "fix:":
                dest = "Bugfixes"

            elif change_type.lower() == "doc:":
                dest = "Documentation changes"

            elif change_type.lower() == "test:":
                dest = "Testing updates"
            
            elif change_type.lower() in ("style:", "refactor:", "chore:"):
                dest = "Miscellaneous"
            
            else:
                continue

            changes[dest].append({'date': date, 'message': message})
        
        except Exception as e:
            print("Failed to process commit: {}, {}".format(raw_change, e))
    
    # Now assemble into a changelog
    changelog = ["### Changes in this version ({}) since {}".format(silico.__version__, last_version)]
    for change_type in changes:
        if len(changes[change_type]) == 0:
            # No updates for this class, skip.
            continue

        # First, add a header.
        changelog.append("\n#### {}:".format(change_type))

        # Add each change.
        for change in changes[change_type]:
            changelog.append(" - [{}]: {}".format(change['date'], change['message']))
    
    changelog = "\n".join(changelog)

    # Write the changelog.
    with open('changelog', 'wt') as changelog_file:
        changelog_file.write(changelog)

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

    depends = [
        ["digichem-core", 'digichem'],
        "basis_set_exchange",
        "cclib",
        "mako",
        "matplotlib",
        "openprattle",
        ["pillow", "PIL"],
        "pysoc",
        ["pyyaml", "yaml"],
        "rdkit",
        "scipy",
        "urwid",
        "weasyprint",
    ]
    
    notes = '### Automated build of Digichem v{} for the {} system\n'.format(silico.__version__, target) +\
            '#### Bundled with:\n'
    
    for depend in depends:
        # CAREFUL, a short module name will break this
        if len(depend) == 2:
            mod_desc = depend[0]
            mod_name = depend[1]
        
        else:
            mod_desc = depend
            mod_name = depend
        mod = __import__(mod_name)
        notes += "{}: {}".format(mod_desc, mod.__version__) + "\n"
    
    notes += '\n' +\
            changelog +\
            "\n\n"
    notes += 'Built by the hard-working Build-boy.'

    # Now create a github release and attach the build.
    sig = [
        'gh', 'release', 'create', tag, silico_paths['archive'],
        '--notes', notes,
        '--title', 'Digichem version {} for {}'.format(silico.__version__, target)
    ]
    # Add pre-release if necessary.
    if silico.development:
        sig.append('-p')

    # Upload
    subprocess.run(sig, universal_newlines = True, check = True)

    #https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.3-CentOS-Stream-8/digichem.6.0.0-pre.3.CentOS-Stream-8.tar.gz
    download_link = "https://github.com/Digichem-Project/build-boy/releases/download/{}-{}/digichem.{}.{}.tar.gz".format(
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
        "<!-- " + target + " --> [Download Digichem v{}]({})".format(
            silico.__version__,
            download_link
        ),
        readme_data
    )
    with open("../../README.md", "w") as readme_file:
        readme_file.write(readme_data)

    # Upload.
    subprocess.run(['git', 'commit', "../../README.md", '-m', "docs: updated download link for {}-{}".format(silico.__version__, target)],
        universal_newlines = True, check = True)
    subprocess.run(['git', 'push', 'origin'],
        universal_newlines = True, check = True)

    # All done.
