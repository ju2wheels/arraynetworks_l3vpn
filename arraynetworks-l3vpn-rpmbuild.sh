#!/bin/bash

CURUSER=$(/usr/bin/whoami);
RHELVER=$(/usr/bin/lsb_release -sr);
RHELVER=${RHELVER%.*};

if [ "${CURUSER}" == "root" ] && [ "$1" != "--download" ]; then
    /bin/echo "ERROR: RPM's must not be built as the root user for security purposes. Please run the build as a regular user.";
    exit 1;
elif  [ "$1" == "--download" ] && [ "${CURUSER}" != "root" ]; then
    /bin/echo "ERROR: VPN tool download and prep must be run as root...";
    exit 1;
fi

if [ "$1" != "--download" ]; then
    if [ ${RHELVER} -eq 5 ]; then
	/bin/rpm -q buildsys-macros > /dev/null;
	
	if [ $? -ne 0 ]; then
	    /bin/echo "ERROR: RPM dependency buildsys-macros is not installed. Please install before continuing...";
	    exit 1;
	fi
    fi
    
    /bin/rpm -q rpm-build > /dev/null;

    if [ $? -ne 0 ]; then
	/bin/echo "ERROR: RPM dependency rpm-build is not installed. Please install before continuing...";
	exit 1;
    fi
    
    if [ -f ~/.rpmmacros ]; then
	/bin/rm -f ~/.rpmmacros;
    fi
    
    if [ ${RHELVER} -eq 5 ]; then
	/bin/echo "%_topdir ${HOME}/rpmbuild" > ~/.rpmmacros;
    fi

    arraynetworks_l3vpn_version=$(/usr/bin/strings bin/array_vpnc | /bin/grep -e '^VPNC_[[:digit:]]' | /bin/sed 's/^VPNC_//' | /bin/sed 's/_/./g');

    if [ -z "${arraynetworks_l3vpn_version}" ]; then
	/bin/echo "ERROR: Failed to determine Array Networks L3VPN version..." 1>&2;
	exit 1;
    fi
    
    /bin/mkdir -p ~/rpmbuild/{BUILD,RPMS,S{OURCES,PECS,RPMS}};
    /bin/cp -f *.spec ~/rpmbuild/SPECS/;
    /bin/cp -af bin ~/rpmbuild/SOURCES/;
    /bin/cp -af man ~/rpmbuild/SOURCES/;
    /usr/bin/rpmbuild -ba --define "_arraynetworks_l3vpn_version ${arraynetworks_l3vpn_version}" ~/rpmbuild/SPECS/arraynetworks-l3vpn.spec;
else
    if [ ! -d bin ]; then
	/bin/mkdir bin;
	/bin/chmod 755 bin;
    fi

    #If this download fails, go to the SoftLayer VPN login page, select the Help link and find the updated download link..."
    /usr/bin/wget -q 'https://vpn.dal01.softlayer.com/prx/000/http/speedtest.dal05.networklayer.com/array/ArrayNetworksL3VPN_LINUX.zip' -O ArrayNetworksL3VPN_LINUX.bin;

    if [ $? -ne 0 ]; then
	/bin/echo "ERROR: Failed to download Array Networks L3VPN..." 1>&2;
	exit 1;
    fi

    /bin/chmod 755 ArrayNetworksL3VPN_LINUX.bin;
    ./ArrayNetworksL3VPN_LINUX.bin;
    /bin/rm -f ArrayNetworksL3VPN_LINUX.bin;
    /bin/rm -f test.tar.gz;
    /bin/chown root:root array_*;
    /bin/chmod 644 array_*;
    /bin/rm -f bin/*;
    /bin/mv array_* bin/;
fi