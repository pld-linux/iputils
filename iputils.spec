#
# Conditional build
%bcond_without	doc	# don't build documentation
#
Summary:	Utilities for IPv4/IPv6 networking
Summary(pl.UTF-8):	Użytki przeznaczone dla pracy z siecią IPv4/IPv6
Summary(ru.UTF-8):	Набор базовых сетевых утилит (ping, tracepath etc.)
Summary(uk.UTF-8):	Набір базових мережевих утиліт (ping, tracepath etc.)
Name:		iputils
Version:	s20071127
Release:	1
Epoch:		2
License:	BSD
Group:		Networking/Admin
Source0:	http://www.skbuff.net/iputils/iputils-%{version}.tar.bz2
# Source0-md5:	12245e9927d60ff5cf4a99d265bcb7d3
Patch0:		%{name}-ping6-no_cr_in_errors.patch
Patch1:		%{name}-ping_sparcfix.patch
Patch2:		%{name}-pmake.patch
Patch3:		%{name}-gkh.patch
Patch4:		%{name}-Makefile.patch
Patch5:		%{name}-pf.patch
Patch6:		%{name}-syserror.patch
Patch7:		%{name}-bindnow.patch
Patch8:		%{name}-gcc34.patch
Patch9:		%{name}-OPEN_MAX.patch
URL:		http://linux-net.osdl.org/index.php/Iputils
%if %{with doc}
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils >= 0.6.10
%endif
BuildRequires:	linux-libc-headers
Requires:	arping
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPv4/IPv6 networking utils:
- clockdiff Measures clock difference between us and <destination>
  with 1msec resolution. Without -o option it uses icmp timestamps, with
  -o it uses icmp echo with timestamp IP option,
- ping/ping6,
- traceroute6,
- arping Ping <address> on device <interface> by ARP packets, using
  source address <source>,
- rdisc Classic router discovery daemon,
- tracepath/tracepath6 It traces path to <destination> discovering MTU
  along this path. It uses UDP port <port> or some random port.

%description -l pl.UTF-8
Narzędzia przeznaczone dla sieci IPv4/IPv6:
- clockdiff Sprawdza różnicę czasu/daty pomiędzy nami a innym
  komputerem z rozdzielczością 1ms,
- ping/ping6,
- traceroute6,
- arping Pinguje <adres> na interfejsie <interfejs> wysyłając pakiety
  ARP,
- rdisc Klasyczny serwer router discovery,
- tracepath/tracepath6 Śledzi drogę pakietów do <przeznaczenia>
  wykorzystując MTU discovery.

%description -l ru.UTF-8
Пакет iputils содержит набор базовых сетевых утилит (ping, tracepath
etc.) от Алексея Кузнецова. Он НЕ включает классический traceroute,
который содержится в отдельном пакете.

%description -l uk.UTF-8
Пакет iputils містить набір базових мережевих утиліт (ping, tracepath
etc.) від Олексія Кузнєцова. Він НЕ містить класичного traceroute,
який міститься в окремому пакеті.

%package ping
Summary:	IPv4 ping
Summary(pl.UTF-8):	ping wykorzystujący IPv4
Group:		Networking/Admin
Provides:	ping
Obsoletes:	inetutils-ping
Obsoletes:	ping

%description ping
IPv4 ping.

%description ping -l pl.UTF-8
ping wykorzystujący IPv4.

%package arping
Summary:	arping
Summary(pl.UTF-8):	arping
Group:		Networking/Admin
Provides:	arping
Obsoletes:	arping

%description arping
Ping <address> on device <interface> by ARP packets, using
source address <source>.

%description arping -l pl.UTF-8
Pinguje <adres> na interfejsie <interfejs> wysyłając pakiety
ARP używając źródłowego adresu <źródło>.

%prep
%setup  -q
#%patch0 -p0
#%patch1 -p1
%patch2 -p1
# obsolete
# %patch3 -p1
#%patch4 -p0
%patch5 -p1
# obsolete
#%patch6 -p1
%patch7 -p0
%patch8 -p1
%patch9 -p1

%build
# empty LDLIBS - don't link with -lresolv, it's not necessary
%{__make} all \
	CC="%{__cc}" \
	CCOPT="%{rpmcflags} -D_GNU_SOURCE -DHAVE_SIN6_SCOPEID=1" \
	LDLIBS=""

%{?with_doc:%{__make} html}
%{__make} man

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/bin,/sbin}

install clockdiff ipg rarpd rdisc tftpd tracepath tracepath6 traceroute6 \
	$RPM_BUILD_ROOT%{_sbindir}

install arping $RPM_BUILD_ROOT/sbin

install ping ping6 $RPM_BUILD_ROOT/bin

install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo ".so tracepath.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tracepath6.8

# no tftpd
rm -f $RPM_BUILD_ROOT%{_sbindir}/tftpd
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/tftpd*

# we don't build pg kernel module
rm -f $RPM_BUILD_ROOT%{_sbindir}/ipg
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/pg3*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RELNOTES %{?with_doc:doc/*.html}
%attr(755,root,root) %{_sbindir}/tracepat*
%attr(755,root,root) %{_sbindir}/rarpd
%attr(755,root,root) %{_sbindir}/rdisc
%attr(4754,root,adm) %{_sbindir}/traceroute6
%attr(4754,root,adm) %{_sbindir}/clockdiff
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/rarpd.8*
%{_mandir}/man8/rdisc.8*
%{_mandir}/man8/tracepath*.8*
%{_mandir}/man8/traceroute6.8*

%files ping
%defattr(644,root,root,755)
%attr(4754,root,adm) %verify(not mode) /bin/ping
%attr(4754,root,adm) %verify(not mode) /bin/ping6
%{_mandir}/man8/ping.8*

%files arping
%defattr(644,root,root,755)
%attr(4754,root,adm) /sbin/arping
%{_mandir}/man8/arping.8*
