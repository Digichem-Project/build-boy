<img src="Banner.png" alt="Banner" />

# Welcome to Build-boy!

This is the Digichem automated build server.

If you're looking for <img src="Logo.png" alt="Banner" height=24 valign=middle /> Digichem downloads, you've come to the right place.

## Latest Versions

To download the latest version of Digichem, please select an option from the supported operating systems below.
Please not that the operating system should match that of the machine where you intend to install Digichem.
In most cases, this means the operating system of your computational server, not your personal machine.

### CentOS Linux (Redhat <= 8.5)
- CentOS-7.9: <!-- CentOS-7.9 --> [6.0.0-pre.17](https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.17-CentOS-7.9/digichem.6.0.0-pre.17.CentOS-7.9.tar.gz)
- CentOS-8.5: <!-- CentOS-8.5 --> [6.0.0-pre.16](https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.16-CentOS-8.5/digichem.6.0.0-pre.16.CentOS-8.5.tar.gz)

### CentOS Stream (Redhat > 8.5)
- CentOS-Stream-8: <!-- CentOS-Stream-8 --> [6.0.0-pre.16](https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.16-CentOS-Stream-8/digichem.6.0.0-pre.16.CentOS-Stream-8.tar.gz)

## All Builds

For historic builds of older versions, see the [releases page](https://github.com/Digichem-Project/build-boy/releases).

## My OS/version Isn't Supported!

Don't panic. First of all, if your OS is Redhat based, simply pick the matching CentOS version instead.
If your OS is more modern than any of the offered downloads, then choose the most modern OS that is offered.
For example, if your cluster runs CentOS Stream 9 (or Redhat 9 etc), choose CentOS-Stream-8.

If your OS is older than any of the offered download, then you are likely out of luck. CentOS-7.9 was first
released in 2020 and will reach end-of-life in July 2024. If your OS is older than this, then you should
seriously consider upgrading at the earliest opportunity. If you do not manage your cluster yourself,
consider sending a polite request to your system administrator to upgrade to a modern OS.

If your OS is based on a different distro to those that are offered (Debian, for example), chose the OS
that most closely matches yours in terms of release date. So long as your OS is more modern than the 
version you download, you will likely be fine.

Digichem tries to maintain a reasonable list of supported OS to match those that are found in the wild.
If your OS isn't supported and you think it should be, please consider creating an
[issue](https://github.com/Digichem-Project/build-boy/issues), and we'll see what we can do.

If in doubt, the oldest available OS (currently CentOS-7.9) is the most likely to be compatible.

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

The Digichem logo and branding is Copyright Digichem 2024, you may not use them in any way (although you are welcome to look at them).

### External libraries

Digichem and Digichem-core both use a number of 3rd party libraries and programs for certain functionality.
As part of the build process, these libraries are included into the distributed archive automatically.
Each program and library naturally retains its original license, which are separate from any of the Digichem licenses.
See the `_internal/LICENSES` folder of each distribution to view these individual licenses.