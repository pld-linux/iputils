#
# Conditional build
%bcond_without	docs	# don't build documentation

Summary:	Utilities for IPv4/IPv6 networking
Summary(pl):	U¿ytki przeznaczone dla pracy z sieci± IPv4/IPv6
Summary(ru):	îÁÂÏÒ ÂÁÚÏ×ÙÈ ÓÅÔÅ×ÙÈ ÕÔÉÌÉÔ (ping, tracepath etc.)
Summary(uk):	îÁÂ¦Ò ÂÁÚÏ×ÉÈ ÍÅÒÅÖÅ×ÉÈ ÕÔÉÌ¦Ô (ping, tracepath etc.)
Name:		iputils
Version:	ss021109
Release:	1
Epoch:		1
License:	BSD
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}-try.tar.bz2
# Source0-md5:	dd10ef3d76480990a2174d2bb0daddaf
Patch0:		%{name}-ping6-no_cr_in_errors.patch
Patch1:		%{name}-ping_sparcfix.patch
Patch2:		%{name}-pmake.patch
Patch3:		%{name}-Makefile.patch
Patch4:		%{name}-gkh.patch
BuildRequires:	glibc-kernel-headers >= 7:2.6.1.1-1
%if %{with docs}
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils >= 0.6.10
%endif
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
Narzêdzia przeznaczone dla sieci IPv4/IPv6:
- clockdiff Sprawdza ró¿nicê czasu/daty pomiêdzy nami a innym
  komputerem z rozdzielczo¶ci± 1ms,
- ping/ping6,
- traceroute6,
- arping Pinguje <adres> na interfejsie <interfejs> wysy³aj±c pakiety
  ARP,
- rdisc Klasyczny serwer router discovery,
- tracepath/tracepath6 ¦ledzi drogê pakietów do <przeznaczenia>
  wykorzystuj±c MTU discovery.

%description -l ru
ðÁËÅÔ iputils ÓÏÄÅÒÖÉÔ ÎÁÂÏÒ ÂÁÚÏ×ÙÈ ÓÅÔÅ×ÙÈ ÕÔÉÌÉÔ (ping, tracepath
etc.) ÏÔ áÌÅËÓÅÑ ëÕÚÎÅÃÏ×Á. ïÎ îå ×ËÌÀÞÁÅÔ ËÌÁÓÓÉÞÅÓËÉÊ traceroute,
ËÏÔÏÒÙÊ ÓÏÄÅÒÖÉÔÓÑ × ÏÔÄÅÌØÎÏÍ ÐÁËÅÔÅ.

%description -l uk
ðÁËÅÔ iputils Í¦ÓÔÉÔØ ÎÁÂ¦Ò ÂÁÚÏ×ÉÈ ÍÅÒÅÖÅ×ÉÈ ÕÔÉÌ¦Ô (ping, tracepath
etc.) ×¦Ä ïÌÅËÓ¦Ñ ëÕÚÎ¤ÃÏ×Á. ÷¦Î îå Í¦ÓÔÉÔØ ËÌÁÓÉÞÎÏÇÏ traceroute,
ÑËÉÊ Í¦ÓÔÉÔØÓÑ × ÏËÒÅÍÏÍÕ ÐÁËÅÔ¦.

%package ping
Summary:	IPv4 ping
Summary(pl):	ping wykorzystuj±cy IPv4
Group:		Networking/Admin

%description ping
IPv4 ping.

%description ping -l pl
ping wykorzystuj±cy IPv4.

%prep
%setup  -q -n %{name}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1

%build
# empty LDLIBS - don't link with -lresolv, it's not necessary
%{__make} all \
	CCOPT="%{rpmcflags} -D_GNU_SOURCE -DHAVE_SIN6_SCOPEID=1" \
	LDLIBS=""

%{?with_docs:	%{__make} html}
%{__make} man

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/bin}

install arping clockdiff rdisc tracepath tracepath6 traceroute6 \
	$RPM_BUILD_ROOT%{_sbindir}

install ping ping6 $RPM_BUILD_ROOT/bin

install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo ".so tracepath.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tracepath6.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RELNOTES %{?with_docs: doc/*.html}
%attr(0755,root,root) %{_sbindir}/tracepat*
%attr(0755,root,root) %{_sbindir}/rdisc
%attr(4754,root,adm) %{_sbindir}/traceroute6
%attr(4754,root,adm) %{_sbindir}/arping
%attr(4754,root,adm) %{_sbindir}/clockdiff
%{_mandir}/man8/arping.8*
%{_mandir}/man8/clockdiff.8*
%{_mandir}/man8/rdisc.8*
%{_mandir}/man8/tracepath*.8*
%{_mandir}/man8/traceroute6.8*

%files ping
%defattr(644,root,root,755)
%attr(4754,root,adm) /bin/ping*
%{_mandir}/man8/ping.8*
