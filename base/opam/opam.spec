Name:           opam
Version:        1.2.2
Release:        3%{?dist}
Summary:        Source-based OCaml package manager
License:        LGPLv3
URL:            https://github.com/ocaml/opam
Source0:        https://repo.citrite.net:443/ctx-local-contrib/xs-opam/opam-full-1.2.2.tar.gz
Patch0:         opam-installer-stublibs.patch
BuildRequires:  curl
BuildRequires:  ocaml

%description
Source-based OCaml package manager

%prep
%autosetup -n %{name}-full-%{version} -p1

%build
%configure
make lib-ext
make

%install
make install DESTDIR=%{buildroot}

%files
%doc AUTHORS
%doc CHANGES
%doc CONTRIBUTING.md
%doc LICENSE
%doc README.md
%{_bindir}/opam
%{_bindir}/opam-admin
%{_bindir}/opam-installer

%changelog
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

