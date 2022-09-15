## This has to match the declaration in xs-opam-repo, which
## relies on this directory and being WORLD WRITABLE
%global _opamroot %{_libdir}/opamroot

Name: xs-opam-src
Version: 5.1.0
Release: 1.1%{?dist}
Summary: Opam repository
License: Various
AutoReqProv: no

%description
Opam repository containing all upstream and development libraries
required for building the OCaml components in the XS Toolstack.

%prep
%build
%install

# create opam root
mkdir -p  %{buildroot}%{_opamroot}
chmod 777 %{buildroot}%{_opamroot}


%files
%{_opamroot}
%attr(777, root, wheel) %{_opamroot}

%changelog
* Thu Sep 15 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 5.1.0-1.1
- Rebuild for XCP-ng 8.3. Citrix did not provide the SRPM in their source ISO.

* Tue May 28 2019 Christian Lindig <christian.lindig@citrix.com> - 5.1.0-1
- CA-319332 defining _opamroot requires version bump

* Wed Oct 03 2018 Christian Lindig <christian.lindig@citrix.com> - 5.0.0-1
- Use Opam 2.0.0
