Name: xs-opam-repo
Version: 3.9.1
Release: 1%{?dist}
Summary: Build and install OCaml libraries from Opam repository
License: Various
URL: https://github.com/xapi-project/xs-opam/archive/3.9.1/xs-opam-3.9.1.tar.gz

# To "pin" a package during development, see below the example
# where qmp is pinned to its master branch. Note that currently
# you can pin to a repository outside Citrix.

AutoReqProv: no
BuildRequires: xs-opam-src = %{version}

Requires:      opam
Requires:      ocaml
Requires:      gmp

BuildRequires: autoconf
BuildRequires: dlm-devel
BuildRequires: git
BuildRequires: gmp
BuildRequires: gmp-devel
BuildRequires: hwdata
BuildRequires: libffi-devel
BuildRequires: libnl3
BuildRequires: m4
BuildRequires: ocaml
BuildRequires: ocaml-camlp4
BuildRequires: ocaml-camlp4-devel
BuildRequires: ocamldoc
BuildRequires: opam
BuildRequires: openssl-devel
BuildRequires: pciutils-devel
BuildRequires: perl
BuildRequires: rsync
BuildRequires: systemd-devel
BuildRequires: which
BuildRequires: xen-ocaml-devel
BuildRequires: zlib-devel

%description
Opam repository that contains all libraries necessary to compile XenServer
Toolstack components.

%prep

%build

# this is a whitelist of packages that are built
PKG=""
PKG="$PKG $(ls -1 /usr/share/opam-repository/packages/upstream)"
PKG="$PKG $(ls -1 /usr/share/opam-repository/packages/xs)"

export OPAMROOT=/usr/lib/opamroot
opam init -y local file:///usr/share/opam-repository
# opam pin add -n qmp 'https://github.com/xapi-project/ocaml-qmp.git#master'

opam config exec -- opam repository list
opam config exec -- opam install %{?_smp_mflags} -y $PKG
opam config exec -- opam list

%install
mkdir -p %{buildroot}/etc/profile.d
echo 'export OPAMROOT=/usr/lib/opamroot' > %{buildroot}/etc/profile.d/opam.sh
echo 'eval `opam config env`' >> %{buildroot}/etc/profile.d/opam.sh

mkdir -p %{buildroot}/usr/lib/opamroot/
rsync -avW /usr/lib/opamroot/ %{buildroot}/usr/lib/opamroot/
rm -rf %{buildroot}/usr/lib/opamroot/log/*
rm -rf %{buildroot}/usr/lib/opamroot/system/build/*
strip  %{buildroot}/usr/lib/opamroot/system/bin/* || true

%files
%attr(664, root, wheel) /usr/lib/opamroot/system/installed
%attr(664, root, wheel) /usr/lib/opamroot/system/installed.roots
%attr(664, root, wheel) /usr/lib/opamroot/system/reinstall
%attr(644, root, root) /etc/profile.d/opam.sh
%defattr(-, root, wheel, 775)
%exclude /usr/lib/opamroot/system/lib/*/*.cmt
%exclude /usr/lib/opamroot/system/lib/*/*.cmti
%exclude /usr/lib/opamroot/system/lib/*/*.annot
%exclude /usr/lib/opamroot/repo/*/archives
%exclude /usr/lib/opamroot/archives
/usr/lib/opamroot

%changelog
* Tue Apr 24 2018 Christian Lindig <christian.lindig@citrix.com> - 3.9.1-1
- This file is auto-generated and the changelog currently does not
  reflect the changes.
