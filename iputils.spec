#
# Conditional build
%bcond_without	doc	# don't build documentation (man, HTML)
#
Summary:	Utilities for IPv4/IPv6 networking
Summary(pl.UTF-8):	Użytki przeznaczone dla pracy z siecią IPv4/IPv6
Summary(ru.UTF-8):	Набор базовых сетевых утилит (ping, tracepath etc.)
Summary(uk.UTF-8):	Набір базових мережевих утиліт (ping, tracepath etc.)
Name:		iputils
Version:	s20151218
Release:	1
Epoch:		2
License:	BSD
Group:		Networking/Admin
Source0:	http://www.skbuff.net/iputils/%{name}-%{version}.tar.bz2
# Source0-md5:	8aaa7395f27dff9f57ae016d4bc753ce
Patch0:		%{name}-pmake.patch
Patch1:		%{name}-pf.patch
Patch2:		%{name}-bindnow.patch
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/iputils
%if %{with doc}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils >= 0.6.10
%endif
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	linux-libc-headers
BuildRequires:	openssl-devel
BuildRequires:	sysfsutils-devel
Requires:	arping
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPv4/IPv6 networking utils:
- clockdiff - measures clock difference between us and destination
  with 1msec resolution,
- traceroute6,
- rdisc - classic router discovery daemon,
- tracepath/tracepath6 - trace path to destination discovering MTU
  along this path using UDP packets

%description -l pl.UTF-8
Narzędzia przeznaczone dla sieci IPv4/IPv6:
- clockdiff - sprawdza różnicę czasu/daty pomiędzy nami a innym
  komputerem z rozdzielczością 1ms,
- traceroute6,
- rdisc - klasyczny demon router discovery,
- tracepath/tracepath6 - śledzą drogę pakietów do celu przy użyciu
  pakietów UDP, sprawdzając MTU

%description -l ru.UTF-8
Пакет iputils содержит набор базовых сетевых утилит (ping, tracepath
etc.) от Алексея Кузнецова. Он НЕ включает классический traceroute,
который содержится в отдельном пакете.

%description -l uk.UTF-8
Пакет iputils містить набір базових мережевих утиліт (ping, tracepath
etc.) від Олексія Кузнєцова. Він НЕ містить класичного traceroute,
який міститься в окремому пакеті.

%package ping
Summary:	IPv4 and IPv6 ping commands
Summary(pl.UTF-8):	Programy ping wykorzystujące IPv4 i IPv6
Group:		Networking/Admin
Provides:	ping
Obsoletes:	inetutils-ping
Obsoletes:	ping

%description ping
IPv4 and IPv6 ping commands.

%description ping -l pl.UTF-8
Programy ping wykorzystujące IPv4 i IPv6.

%package arping
Summary:	arping utility
Summary(pl.UTF-8):	Narzędzie arping
Group:		Networking/Admin
Provides:	arping
Obsoletes:	arping

%description arping
Utility to ping given address on given device by ARP packets, using
given source address.

%description arping -l pl.UTF-8
Narzędzie pingujące podany adres na podanym interfejsie wysyłając
pakiety ARP z użyciem podanego adresu źródłowego.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} all \
	CC="%{__cc}" \
	CCOPT="%{rpmcflags} %{rpmcppflags} -D_GNU_SOURCE -DHAVE_SIN6_SCOPEID=1"

cd ninfod
%configure
%{__make}
cd ..

%if %{with doc}
%{__make} html
%{__make} man
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/bin,/sbin}

install -p clockdiff ipg rarpd rdisc tftpd tracepath tracepath6 traceroute6 \
	$RPM_BUILD_ROOT%{_sbindir}
install -p arping $RPM_BUILD_ROOT/sbin
install -p ping ping6 $RPM_BUILD_ROOT/bin

install -p ninfod/ninfod $RPM_BUILD_ROOT%{_sbindir}
# TODO: PLDify, subpackage?
#install ninfod/ninfod.sh $RPM_BUILD_ROOT/etc/rc.d/init.d

%if %{with doc}
cp -p doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo ".so tracepath.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tracepath6.8
%endif

# no tftpd
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/tftpd
%{?with_doc:%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/tftpd*}

# we don't build pg kernel module
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/ipg
%{?with_doc:%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/pg3*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RELNOTES %{?with_doc:doc/*.html}
%attr(4754,root,adm) %{_sbindir}/clockdiff
%attr(755,root,root) %{_sbindir}/ninfod
%attr(755,root,root) %{_sbindir}/rarpd
%attr(755,root,root) %{_sbindir}/rdisc
%attr(755,root,root) %{_sbindir}/tracepath
%attr(755,root,root) %{_sbindir}/tracepath6
%attr(4754,root,adm) %{_sbindir}/traceroute6
%if %{with doc}
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/ninfod.8*
%{_mandir}/man8/rarpd.8*
%{_mandir}/man8/rdisc.8*
%{_mandir}/man8/tracepath.8*
%{_mandir}/man8/tracepath6.8*
%{_mandir}/man8/traceroute6.8*
%endif

%files ping
%defattr(644,root,root,755)
%attr(4755,root,root) %verify(not mode) /bin/ping
%attr(4755,root,root) %verify(not mode) /bin/ping6
%if %{with doc}
%{_mandir}/man8/ping.8*
%endif

%files arping
%defattr(644,root,root,755)
%attr(4755,root,root) /sbin/arping
%if %{with doc}
%{_mandir}/man8/arping.8*
%endif
