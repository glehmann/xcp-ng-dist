Name:           xcp-emu-manager
Version:        0.0.9
Release:        1%{dist}
Summary:        Tool used for managing xenguest
License:        LGPL
URL:            https://github.com/xcp-ng/xcp-emu-manager
Source0:        https://github.com/xcp-ng/xcp-emu-manager/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xcp-idl-devel

Provides:	emu-manager
Obsoletes:	emu-manager

%description
Simple host networking management service for the xapi toolstack.

Handles suspend, resume and migrate.

%prep
%autosetup -p1

%build
make

%install
make install DESTDIR=%{buildroot} BINDIR=%{_libdir}/xen/bin

%files
%{_libdir}/xen/bin/emu-manager

%changelog
* Thu Jan 10 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.9-1
- New version 0.0.9
- Better logs in case of unexpected end of process
- Migration of PV guests fixed

* Tue Jan 08 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.8-2
- Fix live migration of PV guests

* Wed Dec 19 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.8-1
- Live migration fixes, with new loop logic.

* Mon Nov 19 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.7-1
- Live migration fixes.

* Thu Nov 08 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.6-2
- Update to 0.0.6 to improve migration of VMs under load.
- In most cases migration will now resume when the VM's CPU and/or IO usage decreases.

* Tue Oct 02 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.5-1
- New version 0.0.5 to fix suspend, resume and migrate in XCP-ng 7.6

* Thu Sep 13 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.4-1
- New version 0.0.4 to fix build for XCP-ng 7.6.0

* Mon Jul 23 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.0.3-1
- Update to 0.0.3 with migration support!

* Mon Jul 23 2018 John Else <john.else@gmail.com> - 0.0.2-1
- Initial package
