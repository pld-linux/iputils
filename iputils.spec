#
# Conditional build
%bcond_without	doc	# don't build documentation
#
Summary:	Utilities for IPv4/IPv6 networking
Summary(pl):	U©ytki przeznaczone dla pracy z sieci╠ IPv4/IPv6
Summary(ru):	Набор базовых сетевых утилит (ping, tracepath etc.)
Summary(uk):	Наб╕р базових мережевих утил╕т (ping, tracepath etc.)
Name:		iputils
Version:	ss021109
Release:	6
Epoch:		1
License:	BSD
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}-try.tar.bz2
# Source0-md5:	dd10ef3d76480990a2174d2bb0daddaf
Patch0:		%{name}-ping6-no_cr_in_errors.patch
Patch1:		%{name}-ping_sparcfix.patch
Patch2:		%{name}-pmake.patch
Patch3:		%{name}-gkh.patch
Patch4:		%{name}-Makefile.patch
Patch5:		%{name}-pf.patch
Patch6:		%{name}-syserror.patch
Patch7:		%{name}-bindnow.patch
Patch8:		%{name}-gcc34.patch
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

%description -l pl
NarzЙdzia przeznaczone dla sieci IPv4/IPv6:
- clockdiff Sprawdza rС©nicЙ czasu/daty pomiЙdzy nami a innym
  komputerem z rozdzielczo╤ci╠ 1ms,
- ping/ping6,
- traceroute6,
- arping Pinguje <adres> na interfejsie <interfejs> wysyЁaj╠c pakiety
  ARP,
- rdisc Klasyczny serwer router discovery,
- tracepath/tracepath6 ╕ledzi drogЙ pakietСw do <przeznaczenia>
  wykorzystuj╠c MTU discovery.

%description -l ru
Пакет iputils содержит набор базовых сетевых утилит (ping, tracepath
etc.) от Алексея Кузнецова. Он НЕ включает классический traceroute,
который содержится в отдельном пакете.

%description -l uk
Пакет iputils м╕стить наб╕р базових мережевих утил╕т (ping, tracepath
etc.) в╕д Олекс╕я Кузн╓цова. В╕н НЕ м╕стить класичного traceroute,
який м╕ститься в окремому пакет╕.

%package ping
Summary:	IPv4 ping
Summary(pl):	ping wykorzystuj╠cy IPv4
Group:		Networking/Admin
Provides:	ping
Obsoletes:	inetutils-ping
Obsoletes:	ping

%description ping
IPv4 ping.

%description ping -l pl
ping wykorzystuj╠cy IPv4.

%package arping
Summary:	arping
Summary(pl):	arping
Group:		Networking/Admin
Provides:	arping
Obsoletes:	arping

%description
Ping <address> on device <interface> by ARP packets, using
source address <source>.

%description arping -l pl
Pinguje <adres> na interfejsie <interfejs> wysyЁaj╠c pakiety
ARP u©ywaj╠c ╪rСdЁowego adresu <╪rСdЁo>.

%prep
%setup  -q -n %{name}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p0
%patch8 -p1

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RELNOTES %{?with_doc:doc/*.html}
%attr(755,root,root) %{_sbindir}/tracepat*
%attr(755,root,root) %{_sbindir}/rdisc
%attr(4754,root,adm) %{_sbindir}/traceroute6
%attr(4754,root,adm) %{_sbindir}/clockdiff
%{_mandir}/man8/clockdiff.8*
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
