%global package_speccommit 4ab8cced446078da985cdf9f7e6778abe16f2914
%global usver 2.0.10
%global xsver 5
%global xsrel %{xsver}%{?xscount}%{?xshash}

Name:           opam
Version:        2.0.10
Release:        %{?xsrel}%{?dist}
Summary:        Source-based OCaml package manager
License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception
URL:            https://github.com/ocaml/opam
Source0: opam-full-2.0.10.tar.gz
BuildRequires:  curl
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib

%description
Opam is a source-based package manager for OCaml. It supports multiple
simultaneous compiler installations, flexible package constraints, and
a Git-friendly development workflow.

%prep
%autosetup -n %{name}-full-%{version} -p1

%build
%configure
make lib-ext
make

%install
# The makefile looks like it tries to invoke ocamlfind but only if DESTDIR
# isn't set. If it is set (which it is) LIBINSTALLDIR must be set too
# for installing opam-installer metadata.
%make_install LIBINSTALL_DIR=%{buildroot}/%{_libdir}/ocaml

# However it looks like some (extra) documentation gets
# installed in the wrong place so... delete it.
rm -rf %{buildroot}%{_prefix}/doc

%files
%doc README.md CHANGES AUTHORS CONTRIBUTING.md
%{_bindir}/opam
%{_bindir}/opam-installer
%license LICENSE
%{_mandir}/man1/*.1*
%exclude /usr/doc/opam-installer/*

%changelog
* Thu Aug 04 2022 Pau Ruiz Safont <pau.safont@citrix.com> - 2.0.10-5
- Bump release and rebuild

* Tue Feb 15 2022 Rob Hoes <rob.hoes@citrix.com> - 2.0.10-4
- Bump release and rebuild

* Wed Feb 02 2022 Pau Ruiz Safont <pau.safont@citrix.com> - 2.0.10-3
- Update to 2.0.10
- Fix packaging issues around versions
- Use correct SPDX identifier for the license

* Fri Feb 26 2021 Rob Hoes <rob.hoes@citrix.com> - 2.0.7-2
- Bump release to rebuild

* Fri Nov 20 2020 Pau Ruiz Safont <pau.safont@citrix.com> - 2.0.7-1
- Update to 2.0.7, include some comments from the fedora package

* Thu Nov 19 2020 Rob Hoes <rob.hoes@citrix.com> - 2.0.5-3
- Revision bump for koji migration

* Tue Jan 14 2020 Tim Smith <tim.smith@citrix.com> - 2.0.5-2
- Rebuild for ocaml-4.08

* Wed Dec 04 2019 Christian Lindig <christian.lindig@citrix.com> - 2.0.5-1
- update for compatibility with OCaml 4.08

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
