Name:           amahi-netboot
Version: 0.2
Release:       1

Summary:        Amahi Netboot - Boot over the network

Group:          System Environment/Daemons
License:        GPL
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires: tftp-server

%define debug_package %{nil}

%description
Amahi Netboot - Boot over the network from your HDA

%prep
%setup -q

%build


%install
%{__mkdir} -p %{buildroot}/tftpboot/
%{__cp} -a tftp/* %{buildroot}/tftpboot/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/dnsmasq.d/
%{__cp} -a amahi-pxe.conf %{buildroot}%{_sysconfdir}/dnsmasq.d/

%clean
rm -rf %{buildroot}

%post

# restart dns
if [[ -a /etc/xinetd.d/tftp ]] ; then
	sed -i -e 's|disabled.*=.*$|disabled = no|' /etc/xinetd.d/tftp
	/bin/systemctl enable xinetd.service &> /dev/null
	/bin/systemctl restart dnsmasq.service &> /dev/null
fi

%preun

%files
%defattr(-,root,root,-)
/tftpboot/*
%{_sysconfdir}/dnsmasq.d/amahi-pxe.conf

%changelog
* Wed Jul 17 2013 Carlos Puchol <cpg+git@amahi.org>
- updated for fedora 19
* Sun Aug  2 2009 Carlos Puchol <cpg+git@amahi.org>
- initial version
