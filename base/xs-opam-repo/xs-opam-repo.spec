Name: xs-opam-repo
Version: 6.3.1
Release: 1%{?dist}
Summary: Build and install OCaml libraries from Opam repository
License: Various
URL:     https://github.com/xapi-project/xs-opam

Source0: https://repo.citrite.net/ctx-local-contrib/xs-opam/xs-opam-repo-6.3.1.tar.gz


Provides: gitsha(https://repo.citrite.net/ctx-local-contrib/xs-opam/xs-opam-repo-6.3.1.tar.gz) = c5af2c206e610bd6755758022a692eba2a11b7cb



# To "pin" a package during development, see below the example
# where qmp is pinned to its master branch. Note that currently
# you can pin to a repository outside Citrix.

AutoReqProv: no
BuildRequires: xs-opam-src >= 5.0.0

Requires:      opam >= 2.0.0
Requires:      ocaml
Requires:      gmp
Requires:      bubblewrap

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
BuildRequires: ocamldoc
BuildRequires: opam >= 2.0.0
BuildRequires: openssl-devel
BuildRequires: pciutils-devel
BuildRequires: perl
BuildRequires: rsync
BuildRequires: systemd-devel
BuildRequires: which
BuildRequires: xen-ocaml-devel
BuildRequires: zlib-devel

%description
Opam repository that contains all libraries necessary to compile the
Toolstack components of the Citrix Hypervisor.

%prep
%autosetup -p1 -n xs-opam-repo-%{version}

%build
%install

PKG=""
PKG="$PKG $(ls -1 packages/upstream)"
PKG="$PKG $(ls -1 packages/xs)"

# install into the real opam root to avoid problems with 
# embedded paths
export OPAMROOT=/usr/lib/opamroot
# sandbox is incompatible with the xenctrl package
opam init --disable-sandboxing -y local file://${PWD}
opam switch create ocaml-system
# opam pin add -n qmp 'https://github.com/xapi-project/ocaml-qmp.git#master'
# comment out the next line if you use the "opam pin"
export OPAMFETCH=/bin/false
opam config exec -- opam install %{?_smp_mflags} -y $PKG

mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}/usr/lib/opamroot
echo 'export OPAMROOT=/usr/lib/opamroot' > %{buildroot}/etc/profile.d/opam.sh
echo 'eval `opam config env`' >> %{buildroot}/etc/profile.d/opam.sh

rm -rf /usr/lib/opamroot/ocaml-system/.opam-switch/sources
rm -rf /usr/lib/opamroot/download-cache/*
rm -rf /usr/lib/opamroot/repo/local/cache/*
find   /usr/lib/opamroot/ocaml-system/lib -type f -name '*.cmt*' -delete

rsync -aW /usr/lib/opamroot/ %{buildroot}/usr/lib/opamroot/
strip %{buildroot}/usr/lib/opamroot/ocaml-system/bin/* || true

%files
%attr(644, root, root) /etc/profile.d/opam.sh
%defattr(-, root, wheel, 775)
%exclude /usr/lib/opamroot/download-cache
%exclude /usr/lib/opamroot/repo/local/cache
/usr/lib/opamroot

%changelog
* Tue Apr 02 2019 Christian Lindig <christian.lindig@citrix.com> - 6.3.1-1
- CA-314001, CA-310525: fsync runtime lock fix, and statvfs fix

* Tue Jan 22 2019 Christian Lindig <christian.lindig@citrix.com> - 6.3.0-1
- Update Dune to 1.6.3
- Use new xenctrl.master for Travis builds

* Tue Jan 15 2019 Christian Lindig <christian.lindig@citrix.com> - 6.2.0-1
- Update nbd to 4.0.0+beta3 for CA-307773

* Thu Jan 10 2019 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 6.1.0-1
- Catch up with upstream, Lwt 4.1
- xenctrl: add missing dependency
- ezxenstore.0.3.0 -> ezxenstore.0.3.1
- fd-send-recv.2.0.0 -> fd-send-recv.2.0.1
- opasswd.1.3.0 -> opasswd.1.3.1
- netlink 0.3.3 -> netlink.0.3.4
- qmp.0.15.0 -> qmp.0.15.1
- rrd.1.4.0 -> rrd.transition and xapi-rrd.1.4.0 -> xapi-rrd.1.4.1
- Some packages ported to Dune

* Fri Dec 14 2018 Christian Lindig <christian.lindig@citrix.com> - 5.7.0-1
- vhd-format.0.10.0 => vhd-format.0.11.0
- cdrom.0.9.3 => cdrom.0.9.4
- dlm.0.3.0 => dlm.0.3.1
- nbd.4.0.0+beta1 => nbd.4.0.0
- rrd.1.3.0 => rrd.1.4.0
- xapi-rrd.1.3.0 => xapi-rrd.1.4.0
- Many packages ported to Dune

* Fri Dec 07 2018 Christian Lindig <christian.lindig@citrix.com> - 5.6.1-2
- Block Opam from downloading packages; only use cache

* Thu Dec 06 2018 Christian Lindig <christian.lindig@citrix.com> - 5.6.1-1
- fix missing cache entries in 5.6.0

* Mon Dec 03 2018 Christian Lindig <christian.lindig@citrix.com> - 5.6.0-1
- Update xapi-inventory to 1.2.1'
- Fix Dockerfile
- Deprecate xcp and xcp-inventory

* Fri Nov 30 2018 Christian Lindig <christian.lindig@citrix.com> - 5.5.0-1
- menhir.20181026 => menhir.20181113
- crc.2.0.0 => crc.2.1.0
- ezxenstore.0.2.0 => ezxenstore.0.3.0
- netlink.0.3.1 => netlink.0.3.2
- mirage-random.1.1.0 => mirage-random.1.2.0
- various small changes

* Thu Nov 15 2018 Jon Ludlam <jonathan.ludlam@citrix.com> - 5.4.0-1
- bigstringaf 0.3.0 -> 0.4.0
- menhir 20181006 -> 20181026
- ppx_bin_prot v0.11.0 -> v0.11.1
- ppx_compare v0.11.0 -> v0.11.1
- ppx_enumerate v0.11.0 -> v0.11.1
- ppx_hash v0.11.0 -> v0.11.1
- ppx_sexp_conv v0.11.1 -> v0.11.2
- ppx_typerep_conv v0.11.0 -> v0.11.1
- ppx_variants_conv v0.11.0 -> v0.11.1
- ppxlib 0.2.2 -> 0.3.1
- rpclib 5.9.0 -> 6.0.0
- qmp 0.14.0 -> 0.15.0
- added utop and its dependencies
- removed ppx_type_conv and ppx_driver

* Mon Nov 05 2018 Christian Lindig <christian.lindig@citrix.com> - 5.3.0-1
- xapi-backtrace: v0.6 -> v0.7
- Sync opam files from component repositories
- Restored mustache in xapi-datamodel deps.
- Ported xen-api-sdk to dune.
- ssl.0.5.6 -> ssl.0.5.7


* Wed Oct 24 2018 Christian Lindig <christian.lindig@citrix.com> - 5.2.0-1
- catching up with upstream libraries: alcotest cohttp cohttp-async
  cohttp-lwt cohttp-lwt-unix conduit conduit-async conduit-lwt
  conduit-lwt-unix dune menhir rresult ssl topkg uri

* Tue Oct 09 2018 Christian Lindig <christian.lindig@citrix.com> - 5.1.0-1
- CA-297060 speculative patch for time functions in Core lib
- make opam depext work again in Travis
- simplify files section

* Tue Oct 02 2018 Christian Lindig <christian.lindig@citrix.com> - 5.0.0-1
- First xs-opam based on Opam 2 tooling
