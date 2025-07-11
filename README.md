<img src="Banner.png" alt="Banner" />

# Welcome to Build-boy!

This is the Digichem automated build server.

If you're looking for <img src="Logo.png" alt="Banner" height=24 valign=middle /> Digichem downloads, you've come to the right place.

## Installation

1. Download <!-- Quick-Download --> [Digichem](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-Stream-8/digichem.6.9.2.CentOS-Stream-8-blender.tar.gz), or use one of the specific versions below.
1. Upload the archive to your computational server.
1. Unpack the archive with `tar -xzf digichem.*.tar.gz`.
1. Run the install script with `digichem/_internal/install.sh`.
1. If you've not used Digichem before, run the setup program with `digichem setup`.

Please see the Digichem [documentation](https://doc.digi-chem.co.uk) for full installation instructions and further information.

## Latest Versions

To download the latest version of Digichem, please select an option from the supported operating systems below.
Please not that the operating system should match that of the machine where you intend to install Digichem.
In most cases, this means the operating system of your computational server, not your personal machine.

Note that for most distros Digichem is offered in two flavours[^1]: a 'full' version that comes pre-bundled with a Blender-based rendering engine;
and a 'lite' version that does not. If you do not intend to use Blender as your rendering backend (either because you prefer VMD, or you don't intend to do rendering at all),
you should choose the lite version. Otherwise, choose the full version.

### Fedora Based

Suitable for Fedora, CentOS, CentOS Stream, Redhat, Rocky Linux, and other related distros.

| Distro | Full Version (Blender Included) | Lite Version (No Blender) |
|--------|---------------------------|---------------------------------|
| Rocky Linux 9 | <!-- Rocky-Linux-9 --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Rocky-Linux-9/digichem.6.9.2.Rocky-Linux-9-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Rocky-Linux-9/digichem.6.9.2.Rocky-Linux-9.tar.gz) |
| CentOS Stream 8 | <!-- CentOS-Stream-8 --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-Stream-8/digichem.6.9.2.CentOS-Stream-8-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-Stream-8/digichem.6.9.2.CentOS-Stream-8.tar.gz) |
| CentOS 8.5 | <!-- CentOS-8.5 --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-8.5/digichem.6.9.2.CentOS-8.5-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-8.5/digichem.6.9.2.CentOS-8.5.tar.gz) |
| CentOS 7.9 | <!-- CentOS-7.9 --> N/A | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-CentOS-7.9/digichem.6.9.2.CentOS-7.9.tar.gz) |

### Debian Based

Suitable for Debian, Ubuntu, and other related distros.

| Distro | Full Version (Blender Included) | Lite Version (No Blender) |
|--------|---------------------------|---------------------------------|
| Debian Bookworm (12) | <!-- Debian-Bookworm --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Bookworm/digichem.6.9.2.Debian-Bookworm-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Bookworm/digichem.6.9.2.Debian-Bookworm.tar.gz) |
| Debian Bullseye (11) | <!-- Debian-Bullseye --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Bullseye/digichem.6.9.2.Debian-Bullseye-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Bullseye/digichem.6.9.2.Debian-Bullseye.tar.gz) |
| Debian Buster (10) | <!-- Debian-Buster --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Buster/digichem.6.9.2.Debian-Buster-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Buster/digichem.6.9.2.Debian-Buster.tar.gz) |
| Debian Stretch (9) | <!-- Debian-Stretch --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Stretch/digichem.6.9.2.Debian-Stretch-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Stretch/digichem.6.9.2.Debian-Stretch.tar.gz) |
| Debian Jessie (8) | <!-- Debian-Jessie --> [Download Digichem v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Jessie/digichem.6.9.2.Debian-Jessie-blender.tar.gz) | [Download Digichem Lite v6.9.2](https://github.com/Digichem-Project/build-boy/releases/download/6.9.2-Debian-Jessie/digichem.6.9.2.Debian-Jessie.tar.gz) |

## All Builds

For historic builds of older versions, see the [releases page](https://github.com/Digichem-Project/build-boy/releases).

## My OS/version Isn't Supported!

Don't panic; you don't need to match your operating system exactly[^2]. At the moment, all compiled
versions of Digichem offer the exact same features, so you simply need to pick a version that is compatible
with your computational server. In most cases, so long as your OS is more recent (a higher version) than
the version you download, all will be fine.

If your OS is older than any of the offered download, then you are likely out of luck. CentOS-7.9 was first
released in 2020 and will reach end-of-life in July 2024. If your OS is older than this, then you should
seriously consider upgrading at the earliest opportunity. If you do not manage your cluster yourself,
consider sending a polite request to your system administrator to upgrade to a modern OS.

If your OS is based on a different distro to those that are offered (SUSE, for example), chose the OS
that most closely matches yours in terms of release date.

Digichem tries to maintain a reasonable list of supported OS to match those that are found in the wild.
If your OS isn't supported and you think it should be, please consider creating an
[issue](https://github.com/Digichem-Project/build-boy/issues), and we'll see what we can do.

If in doubt, the oldest available OS (currently CentOS-7.9) is the most likely to be compatible.

[^1]: Some distros are too old to support a modern version of Blender (currently CentOS 7.9). For these distros, only a 'lite' version is available.
[^2]: The main technical requirement is to match the glibc version of your operating system with the version you download.
Versions of Digichem compiled against a *newer* version of glibc than what is present on your system will not function.
The oldest currently supported glibc version is 2.17 (CentOS 7.9).


## Licenses

The Digichem project is split into two sections, each with it's own license.
 - The Digichem program is proprietary software. It is currently available in binary form only under a free-to-use but timed license. 
 - Core components of the library ([Digichem-core](https://github.com/Digichem-Project/digichem-core)) are distributed separately under an open-source license.

Additionally, Build-boy (the code in this repository) is available separately under an open-source license.

### Digichem

Digichem is proprietary software. However, it is currently being made available free-of-charge under a timed-license.
Each build of Digichem has a license automatically included within it, with an expiry set to
90 days from the build date. After this time, a new license must be acquired, or else the 
program will cease to function. The easiest way to acquire a new license is to upgrade to the
latest Digichem version, which will automatically contain a new license.

Digichem reserves the right to change the license terms in the future, but we will never change the terms of, or seek to revoke,
an already issued license.

Your Digichem license will be included in your download. See the included LICENSE file for full details.
See the [DIGICHEM_LICENSE_TEMPLATE](DIGICHEM_LICENSE_TEMPLATE.md) file for an example of such a license.

### Digichem-core

The Digichem-core library is licensed under the permissive, open-source BSD 3-clause license.
See [Digichem-core](https://github.com/Digichem-Project/digichem-core) for more information.

### Build-boy

Build-boy itself is licensed under the permissive, open-source BSD 3-clause license (see [LICENSE](LICENSE)).
In summary, you are free to do whatever you want to with the Build-boy code, but you cannot claim
affiliation with Digichem.

The Digichem logo and branding is Copyright Digichem 2025, you may not use them in any way (although you are welcome to look at them).

### External libraries

Digichem and Digichem-core both use a number of 3rd party libraries and programs for certain functionality.
As part of the build process, these libraries are included into the distributed archive automatically.
Each program and library naturally retains its original license, which are separate from any of the Digichem licenses.
See the `_internal/LICENSES` folder of each distribution to view these individual licenses.

### Bundled software

The Digichem download archives also contains additional software that is not directly incorporated into the Digichem program. These packages are:

 - [Openprattle](https://github.com/Digichem-Project/openprattle), used for file conversions
 - [Blender](https://www.blender.org/), used for rendering images

These packages are optional and can be removed if you wish, but as they provide useful functionality we generally recommend you include them in your installation.

#### Openprattle

Openprattle is currently licensed under the GPL V2.0. The licensing terms can be found in the `digichem/openprattle/_internal/LICENSES/openprattle` directory of your download, or on [github](https://github.com/Digichem-Project/openprattle/blob/main/LICENSE).
The source code for Openprattle is available from [github](https://github.com/Digichem-Project/openprattle).

#### Blender

Blender is licensed under the GPL v3.0. The licensing terms can be found in the `digichem/blender/license` directory of your download, or on the [Blender website](https://www.blender.org/about/license/).
The current builds of Digichem use un-modified versions of Blender, so the source code can be found at any of the official Blender distribution sites, such as on [github](https://github.com/blender/blender).

Please note that Digichem is in no way affiliated with Blender or The Blender Foundation (although we are very thankful of their excellent software).