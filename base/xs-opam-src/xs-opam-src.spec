%global package_speccommit 164e9d7b32eda69f6712e6837575b8524aed5bfb
%global usver 5.1.0
%global xsver 6
%global xsrel %{xsver}%{?xscount}%{?xshash}
## This has to match the declaration in xs-opam-repo, which
## relies on this directory and being WORLD WRITABLE
%global _opamroot %{_libdir}/opamroot

Name: xs-opam-src
Version: 5.1.0
Release: %{?xsrel}%{?dist}
Summary: Opam repository
License: LGPL-2.0-or-later

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
* Tue Jan 21 2025 XenServer Rebuild <rebuild@xenserver.com> - 5.1.0-6
- CP-50033: Move ctx_metadata to https://code.citrite.net/projects/CICD/repos/metadata-defaults/browse/bitbucket/XSS
- CP-53241: XenServer 9 rebuild

* Thu Sep 15 2022 Pau Ruiz Safont <pau.safont@citrix.com> - 5.1.0-4
- Use a license that ensures source availability for building xapi

* Thu Apr 28 2022 Rob Hoes <rob.hoes@citrix.com> - 5.1.0-3
- Bump release and rebuild

* Tue Nov 17 2020 Edwin Török <edvin.torok@citrix.com> - 5.1.0-2
- Re-enabled automatic ocaml dependency generator

* Tue May 28 2019 Christian Lindig <christian.lindig@citrix.com> - 5.1.0-1
- CA-319332 defining _opamroot requires version bump

* Wed Oct 03 2018 Christian Lindig <christian.lindig@citrix.com> - 5.0.0-1
- Use Opam 2.0.0
