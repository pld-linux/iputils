Summary:	-
Summary(de):	-
Summary(fr):	-
Summary(pl):	-
Summary(tr):	-
Name:		iputils
Version:	ss990417
Release:	1
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracyjne
Copyright:	GPL
Source0:	ftp://ftp.inr.ac.ru:/ip-routing/%{name}-%{version}.tar.gz
Patch0:		iputils-resolv.patch
Patch1:		iputils-opt.patch
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
-

%description -l de
-

%description -l fr
-

%description -l pl
-

%description -l tr
-

%prep
%setup  -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
make OPT="$RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

install -s arping tracepath tracepath6 rdisc clockdiff \
	$RPM_BUILD_ROOT%{_sbindir}
	
gzip -9nf README

%pre

%preun

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(0755,root,root) %{_sbindir}/tracepath*
%attr(0755,root,root) %{_sbindir}/rdisc
%attr(4755,root,root) %{_sbindir}/arping
%attr(4755,root,root) %{_sbindir}/clockdiff

%changelog
