Summary:	Utilities for IPv4/IPv6 networking
Summary(pl):	U¿ytki przeznaczone dla pracy z sieci± IPv4/IPv6
Name:		iputils
Version:	ss000121
Release:	1
Epoch:		1
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracyjne
Copyright:	GPL
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}.tar.gz
Patch0:		iputils-resolv.patch
Patch1:		iputils-opt.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	traceroute

%description
IPv4/IPv6 networking utils:
* clockdiff
        Measures clock difference between us and <destination> with 1msec
        resolution. Without -o option it uses icmp timestamps, with -o
        it uses icmp echo with timestamp IP option.
* ping/ping6
* traceroute6
* arping
        Ping <address> on device <interface> by ARP packets,
        using source address <source>.
* rdisc
	Classic router discovery daemon.
* tracepath/tracepath6
	It traces path to <destination> discovering MTU along this path.
	It uses UDP port <port> or some random port.

%description -l pl
Narzêdzia przeznaczone dla sieci IPv4/IPv6:
* clockdiff
	Sprawdza ró¿nicê czasu/daty pomiêdzy nami a innym komputerem
	z rozdzielczo¶ci± 1ms.
* ping/ping6
* traceroute6
* arping
	Pinguje <adres> na interfejsie <interfejs> wysy³aj±c pakiety ARP.
* rdisc
	Klasyczny serwer router discovery.
* tracepath/tracepath6
	¦ledzi drogê pakietów do <przeznaczenia> wykorzystuj±c MTU discovery.

%package ping
Summary:        IPv4 ping
Summary(pl):    ping wykorzystuj±cy IPv4
Group:          Networking/Admin
Group(pl):      Sieciowe/Administracyjne

%description ping
IPv4 ping

%description -l pl
ping wykorzystuj±cy IPv4

%prep
%setup  -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
make OPT="$RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install -s arping clockdiff ping ping6 rdisc tracepath tracepath6 traceroute6 \
	   $RPM_BUILD_ROOT%{_sbindir}

mv in.rdisc.8c rdisc.8
install *.8  $RPM_BUILD_ROOT%{_mandir}/man8
	
gzip -9nf README $RPM_BUILD_ROOT%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(0755,root,root) %{_sbindir}/tracepat*
%attr(4754,root,root) %{_sbindir}/traceroute6
%attr(0755,root,root) %{_sbindir}/rdisc
%attr(4754,root,root) %{_sbindir}/arping
%attr(4754,root,root) %{_sbindir}/clockdiff
%attr(4754,root,root) %{_sbindir}/ping6
%{_mandir}/man8/arping.8*
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/rdisc.8*
%{_mandir}/man8/tracepath.8*

%files ping
%defattr(644,root,root,755)
%attr(4754,root,root) %{_sbindir}/ping
%{_mandir}/man8/ping.8*
