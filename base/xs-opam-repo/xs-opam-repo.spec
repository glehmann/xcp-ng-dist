## This has to match the declaration in xs-opam-src, which
## creates the directory and makes it WORLD WRITABLE
%global _opamroot %{_libdir}/opamroot

Name: xs-opam-repo
Version: 6.35.8
Release: 3%{?dist}
Summary: Build and install OCaml libraries from Opam repository
License: Various
URL:     https://github.com/xapi-project/xs-opam

Source0: https://repo.citrite.net/ctx-local-contrib/xs-opam/xs-opam-repo-6.35.8.tar.gz


Provides: gitsha(https://repo.citrite.net/ctx-local-contrib/xs-opam/xs-opam-repo-6.35.8.tar.gz) = aff7ba062f0924d7b51416d2bd81ba96e3d87106



# To "pin" a package during development, see below the example
# where qmp is pinned to its master branch. Note that currently
# you can pin to a repository outside Citrix.

AutoReqProv: no
BuildRequires: xs-opam-src >= 5.1.0

Requires:      opam >= 2.0.0
Requires:      ocaml
Requires:      gmp
Requires:      bubblewrap
Requires:      libev-devel

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
BuildRequires: libev-devel

%description
Opam repository that contains all libraries necessary to compile the
Toolstack components of the Citrix Hypervisor.

%prep
%autosetup -p1 -n xs-opam-repo-%{version}

%build
%install

PKG=""
PKG="$PKG $(ls -1 packages/upstream | grep -v 'ppx_tools.*4.06.0')"
PKG="$PKG $(ls -1 packages/xs)"

# install into the real opam root to avoid problems with 
# embedded paths.
export OPAMROOT=%{_opamroot}
# sandbox is incompatible with the xenctrl package
opam init --disable-sandboxing -y local file://${PWD}
opam switch create ocaml-system
# opam pin add -n qmp 'https://github.com/xapi-project/ocaml-qmp.git#master'
# comment out the next line if you use the "opam pin"
export OPAMFETCH=/bin/false
opam config exec -- opam install %{?_smp_mflags} -y $PKG

mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}%{_opamroot}
echo 'export OPAMROOT=%{_opamroot}' > %{buildroot}/etc/profile.d/opam.sh
echo 'eval `opam config env`' >> %{buildroot}/etc/profile.d/opam.sh

rm -rf %{_opamroot}/ocaml-system/.opam-switch/sources
rm -rf %{_opamroot}/download-cache/*
rm -rf %{_opamroot}/repo/local/cache/*
find   %{_opamroot}/ocaml-system/lib -type f -name '*.cmt*' -delete

rsync -aW %{_opamroot}/ %{buildroot}%{_opamroot}/
strip %{buildroot}%{_opamroot}/ocaml-system/bin/* || true

mkdir -p "%{buildroot}%{_rpmconfigdir}/macros.d"
echo '%%_opamroot %%{_libdir}/opamroot' >> "%{buildroot}%{_rpmconfigdir}/macros.d/macros.opam"

%files
%attr(644, root, root) /etc/profile.d/opam.sh
%defattr(-, root, wheel, 775)
%exclude %{_opamroot}/download-cache
%exclude %{_opamroot}/repo/local/cache
%{_rpmconfigdir}/macros.d/macros.opam
%{_opamroot}

%changelog
* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 6.35.8-3
- Bump package for libev dependency

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 6.35.8-2
- Bump package after xs-opam update

* Thu Sep 23 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 6.35.8-1
- CA-341597: add conf-libev
- CA-341597: Use the lcm branch for varstored-guard
- CA-341597: add libev as dependency
- CA-341597: make libev available to packages that depend on xs-opam-repo

* Mon Aug 23 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 6.35.7-1
- xs: update xapi-inventory to actually use dune
- maintenance: fix ocaml compilation with GCC 10 and later
- maintenance: fix depexts
- CP-38064: update ppxlib to 0.13.0 and dependents
- ci: use updated container images
- Rename stockholm to yangtze in xs-opam-ci.env
- Update workflow for yangtze branch
- CP-37282: Update mock xenctrl for TSX changes
- fix: broken links from inria's gitlab
- maintenance: pin stockholm branches in xs-extra

* Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 6.35.6-2
- CP-37236: rebuild for new Xenctrl

* Mon Feb 15 2021 Ben Anson <ben.anson@citrix.com> - 6.35.6-1
- UPD-678 bump ezxenstore to v0.4.1

* Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 6.35.5-1
- CA-350872: backport change in rsa check

* Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 6.35.4-1
- detect failed downloads

* Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 6.35.3-1
- maintenance: fix broken links for oasis, ocamlify, ocamlmod

* Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 6.35.2-1
- bump stdext to v4.11.2
- tools: change distro variable for travis CI
- stockholm: point to lcm branches

* Mon Sep 28 2020 Ben Anson <ben.anson@citrix.com> - 6.35.1-1
- CA-342171 bump stdext for Stockholm

* Tue May 12 2020 Christian Lindig <christian.lindig@citrix.com> - 6.35.0-1
- CA-338596: Update xe to use fpath
- CA-338596: Move fpath to upstream
- CP-33121: remove unused stdext-bigbuffer
- Sync opam dependencies for xs-extra/ from source repos
- upstream-extras: add ocamlformat

* Fri Apr 24 2020 Christian Lindig <christian.lindig@citrix.com> - 6.34.0-1
- CA-338243 bump stdext to fix date/time parsing and unparsing

* Mon Apr 20 2020 Christian Lindig <christian.lindig@citrix.com> - 6.32.0-1
- CA-333908 bump stdext with datetime changes
- CP-32669: add randomconv to be able to test mirage-crypto-pk
- CP-32669: update ppx_tools to 6.0
- CP-32669: update mirage-types packages to 3.6.0
- CP-3266: update mirage-protocols packages to 3.1.0
- CP-32669: synchronize ssl package with upstream
- CP-32669: update x509 to 0.11.0
- CP-32669: update menhir to 20200211
- CP-32669: update upstream-extra packages
- CP-32669: update ppx_tools_versioned to 5.3.0
- CP-32669: update base64 to 3.4.0
- CP-21669: update ocaml-migrate-parsetree to 1.7.1
- CP-32669: update bigstringaf to 0.6.1
- CP-32669: update ocplib-endian to 1.1
- CP-32669: update dune packages to 2.5.0
- CP-32669: update sha to use 1.13
- CP-32669: Add pci v1.0.2
- Don't use COPY --chown in Dockerfile

* Fri Apr 03 2020 Christian Lindig <christian.lindig@citrix.com> - 6.31.0-1
- Fix name of dependency

* Fri Apr 03 2020 Christian Lindig <christian.lindig@citrix.com> - 6.30.0-1
- CP-33380: Replace nocypto with mirage-crypto
- CP-32669: update xs-extra opam files

* Thu Apr 02 2020 Christian Lindig <christian.lindig@citrix.com> - 6.29.0-1
- fixup! REQ-811 pin nbd, and all opam files to xs
- REQ-811 pin nbd, and all opam files to xs

* Mon Mar 30 2020 Christian Lindig <christian.lindig@citrix.com> - 6.27.0-1
- CP-33380: Fix installation of dlm with dune 2
- CP-33354 bump xcp-rrd

* Fri Mar 27 2020 Christian Lindig <christian.lindig@citrix.com> - 6.26.0-1
- CP-33380: Update dune to 2.4.0
- travis: follow validator's suggestions
- CP-33380: update message-switch tests for dune 2
- CP-32669: remove craml package
- CP-32669: update travis-opam to 1.5.0
- CP-32669: update qtest to 2.10.1
- CP-32669: Update ppx_deriving_rpc to 6.1.0
- mainteance: update stdext's opam files
- merge rrddump with xcp-rrdd
- Print more log lines on build failures
- maintenance: rrddump pointing at incorrect repo
- maintenance: remove vncproxy
- maintenance: remove lindig from generate-opam-sources.sh
- maintenance: move xenctrl repo to xapi-project
- maintenance: remove rrd.transition

* Tue Mar 10 2020 Christian Lindig <christian.lindig@citrix.com> - 6.25.0-1
- CP-32663: Update x509 to 0.9.0
- CP-27904: nuke sha1 out of orbit
- maintenance: upgrade Dockerfile to ocaml 4.08

* Wed Feb 12 2020 Christian Lindig <christian.lindig@citrix.com> - 6.24.0-1
- maintenance: update metadata for xs-extra packages
- maintenance: update travis build instructions
- CP-29837: use odig so docs can be built
- CP-32669: update ctypes to 0.16.0
- CP-32669: update ounit packages
- CP-32669: update asn1-combinators

* Mon Jan 06 2020 Christian Lindig <christian.lindig@citrix.com> - 6.23.0-1
- CP-32669: update shared-block-ring to 2.5.0
- CP-32669: update ounit to 2.2.1
- CP-32669: update dune 1.11.4
- CP-32669: update xenstore to 2.1.1
- CP-32669: update uri packages to 3.1.0
- CP-32669: update rpclib packages to 6.1.0
- CP-32669: update lwt to 4.5.0
- CP-32669: update duration to 0.1.3
- CP-32669: update cstruct packages to 5.1.1
- CP-32669: update ocaml-migrate-parsetree to 1.5.0
- CP-32669: update num to 1.3
- CP-32669: update octavius to 1.2.2
- CP-32055: update x509 to 0.8.1
- maintenance: update merlin for ocaml 4.08.1
- Use OCaml 4.08 by default, 4.09 speculatively
- wsproxy: fix dependencies, add lwt_log
- Add fmt >= 0.8.8 to xapi-xenopsd

* Wed Dec 04 2019 Christian Lindig <christian.lindig@citrix.com> - 6.22.0-2
- Don't install ppx_tools.5.1 for OCaml 4.08 compatibility

* Mon Nov 04 2019 Pau Ruiz Safont  <pau.safont@citrix.com> - 6.22.0-1
- xs: bump xcp-rrd

* Tue Oct 29 2019 Pau Ruiz Safont <pau.safont@citrix.com> - 6.21.0-1
- xs-extra: sync metadata with repos
- xs: update xapi-rrd to v1.7.0

* Tue Oct 29 2019 Pau Ruiz Safont <pau.safont@citrix.com> - 6.20.0-1
- Add xenops-cli
- CP-32138: Add logs-syslog and dependencies
- upstream-extra: update ocp-indent checksum
- upstream-extra: add crowbar for testing
- xs-extra: sync metadata with repo

* Mon Sep 30 2019 Christian Lindig <christian.lindig@citrix.com> - 6.19.0-1
- CP-32055: Update angstrom to 0.12.1
- CP-32055: remove unused packages
- CP-32055: update diet to 0.4
- CP-32055: update opam-ed
- CP-32055: keep toolstack packages up-to-date
- CP-32055: update ssl to 0.5.9
- CP-32055: update lwt to 4.3.1
- CP-32055: update menhir to 20190924
- CP-32055: update ppxlib to 0.8.1
- CP-32055: update bigstringaf to 0.6.0
- CP-32055: update utop and ocp-indent
- CP-32055: update janestreet packages
- CP-32055: update utop to 2.4.1
- CP-32055: update camomile to 1.0.2
- CP-32055: update lwt_react to 1.1.3

* Fri Sep 06 2019 Christian Lindig <christian.lindig@citrix.com> - 6.18.0-1
- CP-32055: update x509 to 0.7.1
- CP-32055: update zarith to 1.9.1
- CP-32055: update ctypes to 0.15.1

* Tue Sep 03 2019 Christian Lindig <christian.lindig@citrix.com> - 6.16.0-2
- Avoid installing ppx_tools.5.3+4.08.0

* Tue Sep 03 2019 Christian Lindig <christian.lindig@citrix.com> - 6.16.0-1
- add ppx_tools 5.3+4.08.0 for OCaml 4.08
- Add 4.08 for testing
- CP-32055: move core_kernel to correct folder
- CP-32055: update bigstringaf to 0.5.3
- CP-32055: update magic-mime to 1.1.2
- CP-32055: update lwt_ssl to 1.1.3
- CP-32055: update lwt_log to 1.1.1
- CP-32055: update lwt to 4.3.0
- CP-32055: update menhir to 20190626
- CP-32055: update logs to 0.7.0
- CP-32055: update dune to 1.11.3
- CP-32055: update fmt to 0.8.8
- CP-32055: update mirage-protocol packages to 3.0.0
- CP-32055: update mirage-profile to 0.9.1
- CP-32055: update mirage-console packages to 2.4.3
- CP-32055: update cohttp packages to 2.3.0
- CP-32055: update mirage-types packages to 3.5.2
- CP-32055: update mirage-time packages to 1.3.0*

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 6.15.0
- CP-32055: update Jane Street ecosystem to v0.12
- CP-32055: update ppx_deriving to 4.4
- CP-32055: update ppx_tools_versioned to 5.2.3
- CP-32055: update mtime to 1.2.0
- CP-32055: update io-page packages to 2.3.0
- CP-32055: update ocam-migrate-parsetree to 1.4.0
- CP-32055: update ocamlfind to 1.8.1
- CP-32055: update biniou to 1.2.1
- CP-32055: update num to 1.2
- CP-32055: update topkg to 1.0.1
- CP-32055: update bigstringaf to 0.5.2
- CP-32055: update easy-format to 1.3.2
- CP-32055: update cmdliner to 1.0.4
- CP-32055: update dune to 1.11.1

* Wed Aug 07 2019 Christian Lindig <christian.lindig@citrix.com> - 6.14.0-1
- xcp-rrd update to 1.6.0 for CA-322008
- xs-toolstack: remove unused xapi-netdev dependency
- Remove unused xapi-netdev package
- xapi: remove unused netdev dependency
- Add a build that also runs the tests

* Fri Jul 26 2019 Rob Hoes <rob.hoes@citrix.com> - 6.13.0-1
- Fix xapi-test-utils opam dependencies

* Fri Jul 26 2019 Rob Hoes <rob.hoes@citrix.com> - 6.12.0-1
- Update xapi-test-utils to 1.3.0
- Update ezxenstore to 0.4.0
- Drop rpc completely from opam files, do not keep it as optional
- Update http-svr opam file from repo
- update dummy xapi-clusterd to latest
- Do depext after switching to 4.07
- use rpclib instead of rpc when available

* Mon Jul 01 2019 Christian Lindig <christian.lindig@citrix.com> - 6.11.0-1
- Update xenstore_transport to 1.1.0, fixes CA-289145

* Mon Jun 10 2019 Christian Lindig <christian.lindig@citrix.com> - 6.10.0-1
- Remove obsolete packages: cow, omd, caml2html
- CP-30756: update cstruct packages to 5.0.0
- CP-30756: update mirage-block-unix to 2.11.2
- CP-30756: update dune to 1.10.0
- CP-30756: update ppx_tools_versioned to 5.2.2
- CP-30756: update ppxlib to 0.8.0
- CP-30756: update ocaml-migrate-parsetree to 1.3.1
- CP-30756: update result to 1.4
- CP-30756: update uri to 2.2.1
- CP-30756: update ocaml-compiler-libs to v0.12.0
- CP-39756: update stringext to 1.6.0
- CP-30756: update cppo packages to 1.6.6
- CP-30756: update sapwn to v0.13.0
- CP-30756: update xen-gnt packages to 4.0.0

* Wed Jun 05 2019 Christian Lindig <christian.lindig@citrix.com> - 6.9.0-1
- Update stdext to 4.7.0
- CP-30756: Update base64
- maintenance: ignore files created for archiving

* Tue May 28 2019 Christian Lindig <christian.lindig@citrix.com> - 6.8.0-2
- explicitly require xs-opem-src > 5.1.0 which defines _opamroot

* Wed May 22 2019 Christian Lindig <christian.lindig@citrix.com> - 6.8.0-1
- CA-318579 update qmp to 0.18.0 for "query-chardev"
- CP-30756: update tar packages to 1.1.0
- CP-30756: update cstruct packages to 4.0.0
- CP-30756: update nocrypto to follow opam-repository
- xapi-rrd: update to 1.5.0 for CA-315952 XSI-335

* Thu May 16 2019 Christian Lindig <christian.lindig@citrix.com> - 6.7.0-1
- CP-30756: update hex to 1.4.0
- CP-30756: update mirage-console packages to 2.4.2
- CP-30756: upgrade mustache to 3.1.0
- CP-30756: upgrade ppxlib to 0.6.0
- CP-30756: update logs to 0.6.3
- CP-30756: update mirage-flow packages to 1.6.0
- CP-30756: update ezjsonm to 1.1.0
- CP-30756: update ppxfind to 1.3
- CP-30756: update fmt to 0.8.6
- CP-30756: update ptime to 0.8.5
- CP-30756: update io-page packages to 2.2.0
- CP-30756: update octavius to 1.2.1
- CP-30756: update lwt to 4.2.1
- CP-30756: update cpuid to 0.1.2
- CP-30756: update ppx_derivers to 1.2.1
- CP-30756: Update opam-depext to 1.1.3
- CP-30756: Update mmap to 1.1.0
- CP-30756: Update dune to 1.9.3
- CP-30756: Update re to 1.9.0
- rrd-transport: add ezjsonm dependency
- CP-30136: qmp.0.17.0
- Travis: use "opam switch 4.07"
- Travis: use debian-unstable
- xapi.master: add libxxhash-dev external deps
- xapi-test-utils: update to 1.2.0

* Tue Apr 02 2019 Christian Lindig <christian.lindig@citrix.com> - 6.6.0-1
- CA-314001: xapi-stdext 4.6.0
- CP-30756: update mirage-types packages to 3.5.0
- CP-30756: Update ipaddr to 3.1.0 and dependents
- CP-30756: Update mirage-clock packages to 2.0.0
- CP-30756: Update angstrom to 0.11.2
- CP-30756: Update lwt to 4.2.0
- CP-30756: Update bisect_ppx to 1.4.1
- Don't package upstream-extra packages

* Tue Mar 19 2019 Christian Lindig <christian.lindig@citrix.com> - 6.5.0-1
- CP-30756: update mirage-device to 1.2.0
- CP-30756: update mirage-block-unix to 2.11.1
- CP-30756: update xen-gnt packages to 3.1.0
- CP-30756: update mirage-stack packages to 1.4.0
- CP-30756: update vhd-format packages to 0.12.0
- CP-30756: update uuidm to 0.9.7
- CP-30756: update mirage-block packages to 2.4.1
- CP-30756: update mirage-console packages to 2.4.1
- CP-30756: update angstrong to 0.11.1
- CP-30756: Update mirage-channel packages to 3.2.0
- CP-30756: update bigstringaf to 0.5.0
- CP-30756: update xenstore to 2.1.0
- CP-30756: update uutf to 1.0.2
- CP-30756: update uri to 2.2.0
- CP-30756: update tar libraries to 1.0.1
- CP-30756: update ppxlib to 0.5.0
- CP-30756: update cstruct packages to 3.3.0
- CP-30756: Update ocaml-migrate-parsetree to 1.2.0
- CP-30756: update ocamlbuild to 0.14.0
- CP-30756: update magic-mime to 1.1.1
- CP-30756: update ipaddr to 2.9.0
- CP-30756: update io-page to 2.1.0
- CP-30756: update hex to 1.3.0
- CP-30756: update ezjsonm to 1.0.0
- CP-30756: update duration to 0.1.2
- CP-30756: updater alcotest to 0.8.5
- CP-30756: update dune to 1.8.2
- CP-30756: update yojson to 1.7.0
- fix: copy files as user opam instead of root

* Fri Mar 15 2019 Christian Lindig <christian.lindig@citrix.com> - 6.4.0-1
- stdext 4.5.0
- updated opam files in upstream/
- add back patch for CA-297060

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
