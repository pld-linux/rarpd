Summary:	rarpd - reverse address resolution protocol daemon
Summary(pl):	rarpd - demon do protoko³u odwrotnego odwzorowywania adresów
Name:		rarpd
Version:	1.1
Release:	1
Epoch:		1
License:	GPL-like?????
Group:		Networking/Daemons
Source0:	ftp://ftp.dementia.org/pub/net-tools/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Prereq:		rc-scripts >= 0.2.0
Prereq:		/sbin/chkconfig
BuildRequires:	libnet-devel
BuildRequires:	libpcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Reverse Address Resolution Protocol daemon.

%description -l pl
Demon do protoko³u odwrotnego odwzorowywania adresów.

%prep
%setup -q

%build
./configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SBINDIR=%{_sbindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man8
install rarpd.8 $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rarpd
if [ -f /var/lock/subsys/rarpd ]; then
	/etc/rc.d/init.d/rarpd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/rarpd start\" to start rarpd daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/rarpd ]; then
		/etc/rc.d/init.d/rarpd stop >&2
	fi
	/sbin/chkconfig --del rarpd
fi

%files
%defattr(644,root,root,755)
%doc *gz
%{_mandir}/man8/rarpd*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rarpd
%attr(755,root,root) %{_sbindir}/rarpd
%attr(754,root,root) /etc/rc.d/init.d/rarpd
