Summary:	rarpd - reverse address resolution protocol daemon
Summary(pl.UTF-8):   rarpd - demon do protokołu odwrotnego odwzorowywania adresów
Name:		rarpd
Version:	1.1
Release:	4
Epoch:		1
License:	GPL-like (?)
Group:		Networking/Daemons
Source0:	ftp://ftp.dementia.org/pub/net-tools/%{name}-%{version}.tar.gz
# Source0-md5:	04e2ca849e758d0b88c8281775ec3b58
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-libnet1.patch
BuildRequires:	libnet1-devel
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Reverse Address Resolution Protocol daemon.

%description -l pl.UTF-8
Demon do protokołu odwrotnego odwzorowywania adresów.

%prep
%setup -q
%patch0 -p1

%build
%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SBINDIR=%{_sbindir}

install -d $RPM_BUILD_ROOT{%{_mandir}/man8,%{_sysconfdir}/{sysconfig,rc.d/init.d}}
install rarpd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rarpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rarpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rarpd
%service rarpd restart "rarpd daemon"

%preun
if [ "$1" = "0" ];then
	%service rarpd stop
	/sbin/chkconfig --del rarpd
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%{_mandir}/man8/rarpd*
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rarpd
%attr(755,root,root) %{_sbindir}/rarpd
%attr(754,root,root) /etc/rc.d/init.d/rarpd
