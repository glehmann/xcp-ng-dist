Name:           opam
Version:        2.0.0
Release:        2%{?dist}
Summary:        Source-based OCaml package manager
License:        LGPLv2.1
URL:            https://github.com/ocaml/opam

Source0: https://repo.citrite.net:443/ctx-local-contrib/xs-opam/opam-full-2.0.0.tar.gz



BuildRequires:  curl
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib

%description

%prep
%autosetup -n %{name}-full-%{version} -p1

%build
%configure
make lib-ext
make
make man

%install
%make_install LIBINSTALL_DIR=%{buildroot}/%{_libdir}/ocaml

%files
%doc README.md CHANGES AUTHORS CONTRIBUTING.md
%{_bindir}/opam
%{_bindir}/opam-installer
%{_libdir}/ocaml/opam-installer
%license LICENSE
%{_mandir}/man1/*.1*
%exclude /usr/doc/opam-installer/*

%changelog
* Wed Oct 03 2018 Christian Lindig <christian.lindig@citrix.com> - 2.0.0-2
- update License, use mirror for Source0

* Fri Sep 28 2018 Christian Lindig <christian.lindig@citrix.com> - 2.0.0-1
- First packaging of Opam 2

* Tue Sep 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.2.2-4
- Add patch to compile with -unsafe-string

* Tue Oct 3 2017 Edwin Török <edvin.torok@citrix.com> - 1.2.2-3
- CP-24976: Apply upstream patch to fix jbuilder install location of C stubs

* Mon Feb 27 2017 Christian Lindig <christian.lindig@citrix.com> - * 1.2.2-2
- Download sources from Artifactory

* Thu Dec 8 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-1
- Update to 1.2.2

* Fri Dec 26 2014 David Scott <dave.scott@citrix.com> - 1.2.0-1
- Update to 1.2.0

* Thu Oct 02 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1.2-2
- Force a rebuild

* Fri Aug 01 2014 Euan Harris <euan.harris@citrix.com> - 1.1.2-1
- Initial package
