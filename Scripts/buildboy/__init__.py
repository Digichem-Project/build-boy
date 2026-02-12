import os
from pathlib import Path
import shutil
import subprocess
import re
import copy
import json
import logging
import importlib

from buildboy.util import update_repo, expand_path, asset_dir
from buildboy.blender import build_blender, grab_blender

class Builder():
    """Class to handle building digichem."""

    def __init__(self, target):
        self.target = target

        # Disable git prompting.
        os.environ['GIT_TERMINAL_PROMPT'] = "0"

        # Setup build caches.
        self._oprattle_path = None
        self._blender_path = None

        # Build information from the previous version.
        self.last_data = {}
        self.raw_changes = None
        self.last_version = None

        # Read our history file to see what the latest completed builds are.
        with open(Path('../../Builds', target, 'status')) as v_file:
            self.last_data = json.load(v_file)

    def build_target(
        self,
        basedir,
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
        sig = ['./freeze', self.target]
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

    @property
    def oprattle_path(self):
        """Build openprattle; a stand-in for openbabel"""
        if self._oprattle_path is None:
            self._oprattle_path = self.build_target("~/openprattle")

        return self._oprattle_path
    
    def build_blender(self, *args, **kwargs):
        """Build blender"""
        if self._blender_path is None:
            self._blender_path = build_blender(self.target, *args, **kwargs)

        return self._blender_path

    def build_silico(self, branch = "build"):
        """Build silico"""
        return self.build_target(
            "~/silico",
            branch = branch,
            freezeargs = [
                # Pass along the oprattle dir so that gets bundled.
                self.oprattle_path['dir'],
                # As well as any assets we want included.
                asset_dir / "CENSO/censo",
                asset_dir / "CREST/crest",
                asset_dir / "xTB/xtb",
            ]
        )

    def prep_repos(self, silico_branch = "build", digichem_branch = "main"):
        """
        Setup the build environment.
        """
        # Get the latest version of repos that we'll need.
        update_repo(expand_path('~/silico'), silico_branch)
        update_repo(expand_path('~/cclib'), "master")
        update_repo(expand_path('~/configurables'))
        update_repo(expand_path('~/digichem-core'), digichem_branch)
        update_repo(expand_path('~/openprattle'))
        update_repo(expand_path('~/pysoc'), "master")
        os.chdir(expand_path('~/silico'))

        import silico
        import digichem
        importlib.reload(silico)
        importlib.reload(digichem)

    def check_for_new_version(self, branch):
        """
        """
        import silico
        import digichem

        import openprattle
        if silico.__version__.strip() == self.last_data.get(branch, {}).get('version', ""):
            # Nothing new.
            raise Exception("build-boy: Nothing to do, last built version was '{}', current version is '{}'".format(self.last_data.get(branch, {}).get('version', ""), silico.__version__))

    def get_upgrade_info(self, branch):
        """
        """
        import silico

        new_commit = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], capture_output=True, universal_newlines=True, check=True).stdout.strip()

        # Update data.
        self.new_data = copy.deepcopy(self.last_data)
        self.new_data[branch] = {
            'version': silico.__version__,
            'commit': new_commit,
            'release_version': self.last_data.get(branch, {}).get('release_version', silico.__version__),
            'release_commit': self.last_data.get(branch, {}).get('release_commit', new_commit)
        }
        # If this is a major version, update that too.
        if not silico.development:
            self.new_data[branch]['release_version'] = self.new_data[branch]['version']
            self.new_data[branch]['release_commit'] = self.new_data[branch]['commit']

        # Get a list of changes for later.
        # If it's a release (!development), show from the last release version.
        if silico.development:
            last_commit = self.last_data.get(branch, {}).get('commit', "")
            self.last_version = self.last_data.get(branch, {}).get('version', "")
        
        else:
            last_commit = self.last_data.get(branch, {}).get('release_commit', "")
            self.last_version = self.last_data.get(branch, {}).get('release_version', "")

        try:
            # Get changes from git
            # First, get time of last commit.
            last_commit_time = subprocess.run([
                'git', 'show', '--no-patch', '--format=%ci', last_commit
            ], capture_output = True, universal_newlines = True, check = True).stdout.strip()

            # TODO: This might be picking up one commit too many?
            self.raw_changes = subprocess.run([
                'git', 'log', '--pretty=format:%as: %s', '--since', last_commit_time
            ], capture_output = True, universal_newlines = True, check = True).stdout.strip().split("\n")
        
        except Exception as e:
            logging.error("Could not fetch version changes", exc_info = True)
            self.raw_changes = []
    

    def build(self, branch = "build", digichem_branch = "main", blender = None, download_blender = False):
        """
        Build digichem.

        :param target: The OS we're building for.
        :param blender: The version of blender to include (if not None).
        :param download_blender:  If True, a pre-compiled version of blender will be downloaded and used instead of a locally compiled version.
        """
        # Do setup.
        self.prep_repos(branch, digichem_branch)

        print("-----------------------------")
        print("Checking for a new version...")
        print("-----------------------------")
        # First, check if there's a new version to build.
        self.check_for_new_version(branch)

        # Get updates for later.
        self.get_upgrade_info(branch)

        # Work to be done.
        print("-----------------------")
        print("Building openprattle...")
        print("-----------------------")
        self.oprattle_path

        print("--------------------")
        print("Building digichem...")
        print("--------------------")
        silico_paths = self.build_silico(branch = branch)

        print("-------------------")
        print("Building blender...")
        print("-------------------")
        import silico
        if blender and not download_blender:
            blender_paths = self.build_blender(blender, branch = "blender-v{}-release".format(blender))
        
        elif blender and download_blender:
            blender_paths = grab_blender(silico.__version__)
        
        else:
            blender_paths = {}

        # TODO: Handling all archives should be done here, rather than partially in the freeze script.
        if blender:
            # Create a second archive, this one-containing blender.
            # Instead of copying, we'll move the blender build (to save file space).
            blender_paths['dir'].rename(
                Path(silico_paths['dir'], "blender")
            )

            try:
                # Create a symlink.
                os.chdir(Path(silico_paths['dir']))
                os.symlink("blender/blender", "batoms-blender")

                # Create a new archive.
                print("Creating archive with blender...")
                
                os.chdir(Path(silico_paths['dir'], ".."))
                subprocess.run([
                    "tar",
                    "-czf"
                    "{}-blender.tar.gz".format(silico_paths['archive'].with_suffix("").with_suffix("")),
                    "digichem"
                ])

                silico_blender_paths = {
                    "archive": Path(silico_paths['dir'], "..", "{}-blender.tar.gz".format(silico_paths['archive'].with_suffix("").with_suffix(""))).resolve()
                }
            
            finally:
                # Move blender back in case another build want it.
                Path(silico_paths['dir'], "blender").rename(
                    blender_paths['dir']
                )
        
        else:
            silico_blender_paths = {}

        # Change back to build-boy's dir.
        build_dir = Path(expand_path("~/build-boy/Builds"), self.target)
        os.chdir(build_dir)

        # Update the version.
        with open('status', 'wt') as v_file:
            v_file.write(json.dumps(self.new_data))

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
        for raw_change in self.raw_changes:
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
        changelog = ["### Changes in this version ({}) since {}".format(silico.__version__, self.last_version)]
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
            'git', 'commit', '-m', 'Build version {} on {}'.format(silico.__version__, self.target)
        ], universal_newlines = True, check = True)

        tag = '{}-{}'.format(silico.__version__, self.target)
        # Tag it.
        subprocess.run([
            'git', 'tag', '-a', tag, '-m', 'Build of version {} on {}'.format(silico.__version__, self.target)
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
            "pyscf",
            "pysoc",
            ["pyyaml", "yaml"],
            "rdkit",
            "scipy",
            "urwid",
            "weasyprint",
        ]
        
        notes = '### Automated build of Digichem v{} for the {} system\n'.format(silico.__version__, self.target) +\
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
        sig = ['gh', 'release', 'create', tag, silico_paths['archive']]

        if "archive" in blender_paths:
            sig.append(blender_paths['archive'])
        
        if "archive" in silico_blender_paths:
            sig.append(silico_blender_paths['archive'])
        
        sig.extend([
            '--notes', notes,
            '--title', 'Digichem version {} for {}'.format(silico.__version__, self.target)
        ])
        # Add pre-release if necessary.
        if silico.development:
            sig.append('-p')

        # Upload
        attempt = 1

        while True:
            try:
                subprocess.run(sig, universal_newlines = True, check = True)
                break

            except:
                if attempt < 4:
                    print("Failed to create release, trying again...")
                
                else:
                    print("Max tries {} exceeded".format(attempt))
                    raise
            
            attempt += 1

        # All done, update the main README with the latest version.
        # But only if this is a production version!
        # And only if this is the stable branch!
        if not silico.development and branch == "build":
            # First, prepare the links we'll need.
            #https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.3-CentOS-Stream-8/digichem.6.0.0-pre.3.CentOS-Stream-8.tar.gz
            full_download_link = "https://github.com/Digichem-Project/build-boy/releases/download/{}-{}/digichem.{}.{}-blender.tar.gz".format(
                silico.__version__,
                self.target,
                silico.__version__,
                self.target
            )
            full_download_string = "[Download Digichem v{}]({})".format(
                silico.__version__,
                full_download_link
            ) if "archive" in silico_blender_paths else "N/A"
            lite_download_link = "https://github.com/Digichem-Project/build-boy/releases/download/{}-{}/digichem.{}.{}.tar.gz".format(
                silico.__version__,
                self.target,
                silico.__version__,
                self.target
            )
            lite_download_string = "[Download Digichem Lite v{}]({})".format(
                silico.__version__,
                lite_download_link
            )

            # Read the old readme.
            with open("../../README.md", "r") as readme_file:
                readme_data = readme_file.read()
            
            # Change the download link for this version.
            readme_data = re.sub(
                r"<!-- " + re.escape(self.target) + r" -->.*",
                "<!-- {} --> {} | {} |".format(self.target, full_download_string, lite_download_string),
                readme_data
            )

            # If this version is the 'default' (Currently CentOS-Stream-8), update that link too.
            if self.target == "CentOS-Stream-8":
                readme_data = re.sub(
                    r"<!-- Quick-Download -->.*",
                    "<!-- Quick-Download --> [Digichem]({}), or use one of the specific versions below.".format(full_download_link),
                    readme_data
                )

            # Save the modified file.
            with open("../../README.md", "w") as readme_file:
                readme_file.write(readme_data)

            # Upload.
            subprocess.run(['git', 'commit', "../../README.md", '-m', "docs: updated download link for {}-{}".format(silico.__version__, self.target)],
                universal_newlines = True, check = True)
            subprocess.run(['git', 'push', 'origin'],
                universal_newlines = True, check = True)

        # All done.


def build(target, blender = None, download_blender = False):
    """Build!"""
    # What shall we make?
    builds = [
        ["build", "main"],
        ["build-testing", "v8.x"]
    ]

    # Get manager.
    man = Builder(target)

    # And go!
    for branch, digichem_branch in builds:
        try:
            man.build(branch, digichem_branch, blender, download_blender)
        
        except Exception as e:
            logging.error("Build failed", exc_info = True)