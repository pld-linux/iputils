Summary:	Utilities for IPv4/IPv6 networking
Summary(pl):	U©ytki przeznaczone dla pracy z sieci╠ IPv4/IPv6
Summary(ru):	Набор базовых сетевых утилит (ping, tracepath etc.)
Summary(uk):	Наб╕р базових мережевих утил╕т (ping, tracepath etc.)
Name:		iputils
Version:	ss011002
Release:	3
Epoch:		1
License:	BSD
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}.tar.gz
Patch0:		%{name}-no_cr_in_errors.patch
Patch1:		%{name}-kernel_is_fresh.patch
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

%description ping
IPv4 ping.

%description ping -l pl
ping wykorzystuj╠cy IPv4.

%prep
%setup  -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__make} CCOPT="%{rpmcflags} -D_GNU_SOURCE -DHAVE_SIN6_SCOPEID=1" all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install arping clockdiff ping ping6 rdisc tracepath tracepath6 traceroute6 \
	$RPM_BUILD_ROOT%{_sbindir}

mv -f in.rdisc.8c rdisc.8
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(0755,root,root) %{_sbindir}/tracepat*
%attr(4754,root,adm) %{_sbindir}/traceroute6
%attr(0755,root,root) %{_sbindir}/rdisc
%attr(4754,root,adm) %{_sbindir}/arping
%attr(4754,root,adm) %{_sbindir}/clockdiff
%{_mandir}/man8/arping.8*
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/rdisc.8*
%{_mandir}/man8/tracepath.8*

%files ping
%defattr(644,root,root,755)
%attr(4754,root,adm) %{_sbindir}/ping*
%{_mandir}/man8/ping.8*
