Summary:	Utilities for IPv4/IPv6 networking
Summary(pl.UTF-8):	Narzędzia przeznaczone dla pracy z siecią IPv4/IPv6
Summary(ru.UTF-8):	Набор базовых сетевых утилит (ping, tracepath etc.)
Summary(uk.UTF-8):	Набір базових мережевих утиліт (ping, tracepath etc.)
Name:		iputils
Version:	20231222
Release:	1
Epoch:		3
License:	GPL v2+ (arping, tracepath), BSD (the rest)
Group:		Networking/Admin
# TODO: use
Source0:	https://github.com/iputils/iputils/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a9741e46dcb11457a32287470b0ce365
URL:		https://github.com/iputils/iputils
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-utils >= 0.6.10
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-tools
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libgpg-error-devel
BuildRequires:	libidn2-devel
BuildRequires:	libxslt-progs
BuildRequires:	linux-libc-headers
BuildRequires:	meson >= 0.40
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	arping
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPv4/IPv6 networking utils:
- clockdiff - measures clock difference between us and destination
  with 1msec resolution,
- tracepath/tracepath6 - trace path to destination discovering MTU
  along this path using UDP packets

%description -l pl.UTF-8
Narzędzia przeznaczone dla sieci IPv4/IPv6:
- clockdiff - sprawdza różnicę czasu/daty pomiędzy nami a innym
  komputerem z rozdzielczością 1ms,
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

%package -n ping
Summary:	IPv4 and IPv6 ping commands
Summary(pl.UTF-8):	Programy ping wykorzystujące IPv4 i IPv6
License:	BSD
Group:		Networking/Admin
Obsoletes:	inetutils-ping
Obsoletes:	iputils-ping < 2:s20151218-2

%description -n ping
IPv4 and IPv6 ping commands.

%description -n ping -l pl.UTF-8
Programy ping wykorzystujące IPv4 i IPv6.

%package arping
Summary:	arping utility
Summary(pl.UTF-8):	Narzędzie arping
License:	GPL v2+
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

# disable IPv6 tests (we don't run tests anyway)
%{__sed} -i -e "/run_command/ s/'ip'/'false'/" ping/meson.build

%build
%meson build \
	--bindir=%{_sbindir} \
	-DBUILD_ARPING=true \
	-DBUILD_CLOCKDIFF=true \
	-DBUILD_MANS=true \
	-DBUILD_PING=true \
	-DBUILD_TRACEPATH=true \
	-DUSE_CAP=true \
	-DUSE_GETTEXT=true \
	-DUSE_IDN=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/bin,/sbin}

%ninja_install -C build

%{__mv} $RPM_BUILD_ROOT{%{_sbindir}/ping,/bin}
%{__mv} $RPM_BUILD_ROOT{%{_sbindir}/arping,/sbin}

ln -s ping $RPM_BUILD_ROOT/bin/ping4
ln -s ping $RPM_BUILD_ROOT/bin/ping6
ln -s tracepath $RPM_BUILD_ROOT%{_sbindir}/tracepath4
ln -s tracepath $RPM_BUILD_ROOT%{_sbindir}/tracepath6

echo ".so ping.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ping4.8
echo ".so ping.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ping6.8
echo ".so tracepath.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tracepath4.8
echo ".so tracepath.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tracepath6.8

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.md
# TODO: use capabilities (cap_net_raw,cap_sys_nice+ep)
%attr(4754,root,adm) %{_sbindir}/clockdiff
%attr(755,root,root) %{_sbindir}/tracepath
%attr(755,root,root) %{_sbindir}/tracepath4
%attr(755,root,root) %{_sbindir}/tracepath6
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/tracepath.8*
%{_mandir}/man8/tracepath4.8*
%{_mandir}/man8/tracepath6.8*

%files -n ping
%defattr(644,root,root,755)
# TODO: use capabilities (cap_net_raw+p)
%attr(4755,root,root) %verify(not mode) /bin/ping
%attr(4755,root,root) %verify(not mode) /bin/ping4
%attr(4755,root,root) %verify(not mode) /bin/ping6
%{_mandir}/man8/ping4.8*
%{_mandir}/man8/ping6.8*
%{_mandir}/man8/ping.8*

%files arping
%defattr(644,root,root,755)
# TODO: use capabilities (cap_net_raw+p)
%attr(4755,root,root) /sbin/arping
%{_mandir}/man8/arping.8*
