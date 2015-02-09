# Array Networks L3VPN CLI Client

This is RPM spec files for Array Networks L3VPN CLI Client for Linux (tested against RHEL 5/6).

The build process for this tool requires first downloading and extracting the Array Networks L3VPN client as root before beginning the build process as we dont want to store the binaries in this repo as they are proprietary to Array Networks.

The build process is:

1. Install the build tools as root/sudo:
  ```
  yum install buildsys-macros rpm-build groff ghostscript
  ```
  
2. Download the Array Networks L3VPN client as root/sudo:
  ```
  ./arraynetworks-l3vpn-rpmbuild.sh --download
  ```
  
3. Build as normal user:
  ```
  ./arraynetworks-l3vpn-rpmbuild.sh
  ```
  
4. Check for your rpms in `~/rpmbuild/RPMS/`.

# Supported Platforms

The Array Networks L3VPN Linux agent supports RHEL 5/6 and Ubuntu. There is currently an issue with the way the 64bit Array Networks agent is compiled (it uses a newer library version than is supported on RH 5 64bit) and is not compatible with RH 5 64bit so we package the 32bit agent instead.

# TODO

* Ubuntu deb packaging

# License

The spec and helper files are GPLv2.

The Array Networks L3VPN Client and related files are proprietary to Array Networks.
