<img src="Banner.png" alt="Banner" />

# Welcome to Build-boy!

This is the Digichem automated build server.

If you're looking for <img src="Logo.png" alt="Banner" height=24 valign=middle /> Digichem downloads, you've come to the right place.

## Latest Versions

To download the latest version of Digichem, please select an option from the supported operating systems below.
Please not that the operating system should match that of the machine where you intend to install Digichem.
In most cases, this means the operating system of your computational server, not your personal machine.

### CentOS/Redhat <= 8.5 (CentOS Linux)
- CentOS-7.9: [6.0.0-pre.3](https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.3-CentOS-7.9/digichem.6.0.0-pre.3.CentOS-7.9.tar.gz)
- CentOS-8.5: [6.0.0-pre.3](https://github.com/Digichem-Project/build-boy/releases/download/6.0.0-pre.3-CentOS-8.5/digichem.6.0.0-pre.3.CentOS-8.5.tar.gz)

### CentOS/Redhat > 8.5 (CentOS Stream)
- CentOS-Stream-8: Coming-soon!


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