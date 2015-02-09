Name:           arraynetworks-l3vpn
Version:        %{_arraynetworks_l3vpn_version}
Release:        1%{?dist}
Summary:        Array Networks L3VPN CLI Tool
Vendor:         Array Networks
License:        Proprietary
Group:          Array Networks/Tools       
Packager:       Julio Lajara
URL:            https://github.com/ju2wheels/arraynetworks-l3vpn
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      i386 x86_64
BuildRequires:  groff ghostscript
Requires: zlib

%description
Array Networks L3VPN CLI Tool

%prep
# nothing to copy

%build
groff -Thtml -mandoc %{_sourcedir}/man/array_vpnc.1 > %{_sourcedir}/man/array_vpnc.1.html
groff -Tps -mandoc %{_sourcedir}/man/array_vpnc.1 | ps2pdf - %{_sourcedir}/man/array_vpnc.1.pdf
gzip -f %{_sourcedir}/man/*.1

%install
install -d -m755 %{buildroot}/usr/share/doc/%{name}/
install -d -m755 %{buildroot}/usr/share/man/man1
install -d -m755 %{buildroot}/opt/%{name}/bin
install -m644 %{_sourcedir}/man/array_vpnc.1.gz %{buildroot}/usr/share/man/man1/
install -m644 %{_sourcedir}/man/array_vpnc.1.html %{buildroot}/usr/share/doc/%{name}/
install -m644 %{_sourcedir}/man/array_vpnc.1.pdf %{buildroot}/usr/share/doc/%{name}/

#Unfortunately the 64bit agent doesnt work on RH5 and couldnt get SoftLayer to contact upstream support
#so we just use the 32bit agent on RH5 64bit
%if %{?el5:1}%{!?el5:0}
install -m751 %{_sourcedir}/bin/array_vpnc %{buildroot}/opt/%{name}/bin/array_vpnc
install -m751 %{_sourcedir}/bin/array_loader %{buildroot}/opt/%{name}/bin/array_loader
%else
    %ifarch x86_64
    install -m751 %{_sourcedir}/bin/array_vpnc64 %{buildroot}/opt/%{name}/bin/array_vpnc64
    install -m751 %{_sourcedir}/bin/array_loader64 %{buildroot}/opt/%{name}/bin/array_loader64
    %else
    install -m751 %{_sourcedir}/bin/array_vpnc %{buildroot}/opt/%{name}/bin/array_vpnc
    install -m751 %{_sourcedir}/bin/array_loader %{buildroot}/opt/%{name}/bin/array_loader
    %endif
%endif

%clean
[ X%{buildroot} != X ] && [ X%{buildroot} != X/ ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %dir  /opt/%{name}
%attr(0755,root,root) %dir  /opt/%{name}/bin
%attr(0755,root,root) %dir  /usr/share/doc/%{name}
%attr(0644,root,root)       /usr/share/doc/%{name}/*
%attr(0644,root,root)       /usr/share/man/man1/array_vpnc.1.gz
%attr(0751,root,root)       /opt/%{name}/bin/array_loader*
%attr(0751,root,root)       /opt/%{name}/bin/array_vpnc*

%changelog
* Sun Feb 08 2015 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.17-1
- Generalize the build spec so the version is auto determined from the binaries.

* Fri Jan 23 2015 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.17-1
- Upgrade to upstream .15 release, unknown fixes/improvements no change logs provided

* Thu Oct 23 2014 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.15-3
- Fixes segfault issue when connecting to SL VPN. Note that this is a new agent although the
  vendor did not update the agent version string, so do not go by the version string reported,
  you would have to verify by md5sum (55a81f98a8412874c930c9d712a81f17 for array_vpnc and
  4b6ba43ce34ea22c95bb76f3ed93c04f for array_vpnc 64bit).
- Revert the 64bit agent back to the original file names so that it can find array_loader64

* Tue Aug 26 2014 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.15-1
- Upgrade to upstream .15 release, unknown fixes/improvements no change logs prodvided

* Mon Mar 24 2014 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.14-2
- Add RH5 64bit support by using the 32bit agent since we couldnt get upstream support

* Mon Mar 24 2014 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.14-1
- Upgrade to upstream .14 release, unknown fixes/improvements no change logs provided

* Wed Aug 28 2013 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.12-1
- Upgrade to .12 aka beta 3

* Fri Aug 16 2013 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.11-1
- Upgrade to .11 beta which is supposed to resolve issue where vpn client doesnt recognize
  another vpn may be using a tunnel already and overwrites it.

* Mon Aug 05 2013 Julio Lajara <ju2wheels@gmail.com> - 8.4.6.10-4
- Initial release
