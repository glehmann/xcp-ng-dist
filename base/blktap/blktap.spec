%global package_speccommit d43c80f248a6875436549a5f42d3dc9edc52c0e0
%global usver 3.54.6
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v3.54.6

Summary: blktap user space utilities
Name: blktap
Version: 3.54.6
Release: %{?xsrel}%{?dist}
License: BSD
Group: System/Hypervisor
URL: https://github.com/xapi-project/blktap
Source0: blktap-3.54.6.tar.gz
Patch0: CP-37221__only_write_footer_when_extending_BAT
Patch1: CP-34438__no_error_from_valve_validate-parent
Patch2: CP-34438__extend_tap-ctl_unpause_to_allow_adding_IO_restriction
Patch3: CP-34834__Add_foreground_mode_to_td-rated
Patch4: CP-34834__ensure_that_pselect_timeout_is_never_NULL
Patch5: CP-34834__unregister_retry_event_on_close_if_set
Patch6: CP-34834__dont_warn_on_no_timer_value

BuildRoot: %{_tmppath}/%{name}-%{release}-buildroot
Obsoletes: xen-blktap < 4
BuildRequires: e2fsprogs-devel, libaio-devel, systemd, autogen, autoconf, automake, libtool, libuuid-devel
BuildRequires: xen-devel, kernel-headers, xen-dom0-libs-devel, zlib-devel, xen-libs-devel, libcmocka-devel, lcov, git
BuildRequires: xs-openssl-devel >= 1.1.1
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-binutils
BuildRequires: devtoolset-11-liblsan-devel
%{?_cov_buildrequires}
Requires(post): systemd
Requires(post): /sbin/ldconfig
Requires(preun): systemd
Requires(postun): systemd
Requires(postun): /sbin/ldconfig

Conflicts: sm < 3.0.1

Provides: blktap(nbd) = 2.0

%description
Blktap creates kernel block devices which realize I/O requests to
processes implementing virtual hard disk images entirely in user
space.

Typical disk images may be implemented as files, in memory, or
stored on other hosts across the network. The image drivers included
with tapdisk can map disk I/O to sparse file images accessed through
Linux DIO/AIO and VHD images with snapshot functionality.

This packages includes the control utilities needed to create
destroy and manipulate devices ('tap-ctl'), the 'tapdisk' driver
program to perform tap devices I/O, and a number of image drivers.

%package devel
Summary: BlkTap Development Headers and Libraries
Requires: blktap = %{version}
Group: Development/Libraries

%description devel
Blktap and VHD development files.

%prep
%autosetup -p1 -S git
%{?_cov_prepare}

%build
source /opt/rh/devtoolset-11/enable

%{?_cov_make_model:%{_cov_make_model misc/coverity/model.c}}
echo -n %{version} > VERSION
sh autogen.sh
# The following can be used for leak tracing
#%%configure LDFLAGS="$LDFLAGS -Wl,-rpath=/lib64/citrix -lrt -static-liblsan" CFLAGS="$CFLAGS  -Wno-stringop-truncation -fsanitize=leak -ggdb -fno-omit-frame-pointer"
#%%configure LDFLAGS="$LDFLAGS -Wl,-rpath=/lib64/citrix" CFLAGS="$CFLAGS -Wno-stringop-truncation -Wno-error=analyzer-malloc-leak -Wno-error=analyzer-use-after-free -Wno-error=analyzer-double-free -Wno-error=analyzer-null-dereference -fanalyzer"
%configure LDFLAGS="$LDFLAGS -Wl,-rpath=/lib64/citrix" CFLAGS="$CFLAGS -Wno-stringop-truncation"
%{?_cov_wrap} make %{?coverage:GCOV=true}

%check
make check || (find mockatests -name \*.log -print -exec cat {} \; && false)
./collect-test-results.sh %{buildroot}/testresults

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{?_cov_install}
mkdir -p %{buildroot}%{_localstatedir}/log/blktap
%if 0%{?coverage:1}
cd ../ && find -name "*.gcno" | grep -v '.libs/' | xargs -d "\n" tar -cvjSf %{buildroot}/%{name}-%{version}.gcno.tar.bz2
%endif

%triggerin -- mdadm
echo 'KERNEL=="td[a-z]*", GOTO="md_end"' > /etc/udev/rules.d/65-md-incremental.rules
cat /usr/lib/udev/rules.d/65-md-incremental.rules >> /etc/udev/rules.d/65-md-incremental.rules

%files
%defattr(-,root,root,-)
%docdir /usr/share/doc/%{name}
/usr/share/doc/%{name}
%{_libdir}/*.so.*
%{_bindir}/vhd-util
%{_bindir}/vhd-update
%{_bindir}/vhd-index
%{_bindir}/tapback
%{_bindir}/cpumond
%{_sbindir}/cbt-util
%{_sbindir}/lvm-util
%{_sbindir}/tap-ctl
%{_sbindir}/td-util
%{_sbindir}/td-rated
%{_libexecdir}/tapdisk
%{_sysconfdir}/logrotate.d/blktap
%{_sysconfdir}/cron.daily/prune_tapdisk_logs
%{_sysconfdir}/xensource/bugtool/tapdisk-logs.xml
%{_sysconfdir}/xensource/bugtool/tapdisk-logs/description.xml
%{_localstatedir}/log/blktap
%{_unitdir}/tapback.service
%{_unitdir}/cpumond.service

%files devel
%defattr(-,root,root,-)
%doc
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/vhd/*
%{_includedir}/blktap/*
%if 0%{?coverage:1}
/%{name}-%{version}.gcno.tar.bz2
%endif

%post
/sbin/ldconfig
%systemd_post tapback.service
%systemd_post cpumond.service

%preun
%systemd_preun tapback.service
%systemd_preun cpumond.service

%postun
/sbin/ldconfig
%systemd_postun tapback.service
%systemd_postun cpumond.service
if [ $1 -eq 0 ]; then
    rm -f %{_sysconfdir}/udev/rules.d/65-md-incremental.rules
fi

# The posttrans invocation of ldconfig is needed because older
# versions of blktap did not have ldconfig in their postun script.
%posttrans -p /sbin/ldconfig

%{?_cov_results_package}

%package testresults
Group:    System/Hypervisor
Summary:  test results for blktap package

%description testresults
The package contains the build time test results for the blktap package

%files testresults
/testresults

%package -n vhd-util-standalone
Group:   System/Hypervisor
Summary: Standalone vhd-util binary
Conflicts: blktap

%description -n vhd-util-standalone
The package contains a standalone vhd-util binary which can be installed
without requiring other libraries

%files -n vhd-util-standalone
%{_bindir}/vhd-util
%{_libdir}/libvhd.so.*
%{_libdir}/libblockcrypto.so.*

%changelog
* Fri Jan 26 2024 Mark Syms <mark.syms@citrix.com> - 3.54.6-3
- Rebuild against libxenstore.so.4

* Thu Sep 28 2023 Mark Syms <mark.syms@citrix.com> - 3.54.6-2
- CP-40871: Enable rate limit control on unpause

* Thu Sep 07 2023 Mark Syms <mark.syms@citrix.com> - 3.54.6-1
- CP-40871: return the number of sectors coalesced from vhd-util
- CP-45025: Avoid retries except in a few specific cases
- CA-382087: Only write the bitmap if the contents have changed

* Tue Aug 01 2023 Mark Syms <mark.syms@citrix.com> - 3.54.5-1
- Report control timeouts correctly

* Wed Jun 21 2023 Mark Syms <mark.syms@citrix.com> - 3.54.4-1
- Remove unused and broken libvhdio
- CA-377624: Guard against NULL tiocb in lio event handler

* Wed Apr 12 2023 Mark Syms <mark.syms@citrix.com> - 3.54.3-2
- Rebuild

* Wed Mar 29 2023 Mark Syms <mark.syms@citrix.com> - 3.54.3-1
- Rebuild

* Mon Feb 27 2023 Mark Syms <mark.syms@citrix.com> - 3.54.2-1
- Add configurure options for -fanalyzer
- Fix use after free in NBD client handling

* Fri Feb 17 2023 Mark Syms <mark.syms@citrix.com> - 3.54.1-1
- Rebuild

* Thu Feb 16 2023 Mark Syms <mark.syms@citrix.com> - 3.54.0-1
- Release 3.54.0
- Update compiler set
- Various NBD server improvements

* Thu Jan 12 2023 Mark Syms <mark.syms@citrix.com> - 3.53.0-1
- Use NBD in IntelliCache
- Use optimized SMP barriers

* Mon Oct 03 2022 Mark Syms <mark.syms@citrix.com> - 3.52.0-1
- CP-40769: make NBD server listen correctly after open

* Tue Sep 20 2022 Mark Syms <mark.syms@citrix.com> - 3.51.7-1
- Remvoe deprecated support for Nutanix HC storage.

* Wed May 18 2022 Mark Syms <mark.syms@citrix.com> - 3.51.6-1
- CA-366761: fix off by one size calculation in snprintf

* Fri May 13 2022 Mark Syms <mark.syms@citrix.com> - 3.51.5-1
- CA-366761: fix coverity issues

* Tue May 03 2022 Mark Syms <mark.syms@citrix.com> - 3.51.4-1
- CA-366614: prune old blktap logs

* Wed Mar 09 2022 Mark Syms <mark.syms@citrix.com> - 3.51.3-1
- Various bugfixes from OpenXT

* Wed Nov 17 2021 Mark Syms <mark.syms@citrix.com> - 3.51.2-4
- Rebuild

* Mon Aug 23 2021 Mark Syms <mark.syms@citrix.com> - 3.51.2-3
- Revert "CA-356983: move udev rules for td devices to sm"

* Thu Aug 12 2021 Mark Syms <mark.syms@citrix.com> - 3.51.2-2
- CA-356983: move udev rules for td devices to sm

* Thu Jul 15 2021 Mark Syms <mark.syms@citrix.com> - 3.51.2-1
- CA-356180: ensure queue is valid before debug dumping it
- CA-356215: Add more error logs to vhd-util and report on stderr
- CA-356508: handle EINTR in tap-ctl IPC

* Mon Jun 07 2021 Tim Smith <tim.smith@citrix.com> - 3.51.1-1
- CA-353265 Disable posix AIO backend

* Wed Jun 02 2021 Mark Syms <mark.syms@citrix.com> - 3.51.0-1
- CA-355145: guard vbd_stats
- CA-183182: Don't error if there are no tapdisks to signal

* Thu Mar 11 2021 Mark Syms <mark.syms@citrix.com> - 3.50.0-1
- CA-35250 - Fix Coverity issues introduced by CP-32853

* Thu Mar 04 2021 Mark Syms <mark.syms@citrix.com> - 3.49.0-1
- CP-32853 - Add posixaio io backend for read only files.

* Mon Jan 18 2021 Mark Syms <mark.syms@citrix.com> - 3.48.0-1
- CP-35115: implement "New fixed style" nbd option negotiation.

* Mon Jan 04 2021 Mark Syms <mark.syms@citrix.com> - 3.47.0-1
- Update to v3.47.0
- CA-350300: remove duplicated and unchecked call to canonpath

* Fri Dec 11 2020 Mark Syms <mark.syms@citrix.com> - 3.46.0-1
- More coverity fixes

* Fri Dec 04 2020 Mark Syms <mark.syms@citrix.com> - 3.45.0-1
- Various coverity fixes

* Fri Nov 06 2020 Mark Syms <mark.syms@citrix.com> - 3.44.0-1
- CA-347165: validate the VHD header blocksize

* Wed Sep 30 2020 Mark Syms <mark.syms@citrix.com> - 3.43.0-1
- CA-345193: allocate sufficient space in normalize_path
- CA-345193: add unit test to exercise memory allocation error

* Tue Sep 15 2020 Mark Syms <mark.syms@citrix.com> - 3.42.0-1
- CA-343797: (Coverity) fix set of Unintentional integer overflow issues
- CA-343796: (Coverity) exit when insufficient args supplied
- Errno model removal.
- CP-34900: remove command lookup by environment
- feat(vhd/canonpath): add support for DRBD resource path
- feat(libvhd): try to open DRBD devices using the LVM layer
- feat(libvhd): when a DRBD device path is given, do not use LVM layer if device is not up to date
- libvhd: properly check data alignment
- CA-344119: return correct error, snprintf doesn't set errno
- CA-344424: ensure we don't get division by 0

* Tue Sep 01 2020 Mark Syms <mark.syms@citrix.com> - 3.41.0-1
- CP-34221 - Remove unused obsolete MD5
- CP-32988 - In CA-225067 it was discovered cgexec which used to wrap
- CA-343704: Correct the error return for vhd_footer_offset_at_eof
- CP-34867: Reduce use of lseek by storing the current offset in the vhd context

* Tue Jul 21 2020 Mark Syms <mark.syms@citrix.com> - 3.40.0-1
- CA-342553: don't try to read encryption key from raw parent
- CA-342578: fix switch case fall through error

* Mon Jul 13 2020 Mark Syms <mark.syms@citrix.com> - 3.39.0-1
- CP-34313: Fix Coverity Nesting_Indent_Mismatch error
- CP-34313: Coverity: correctly check for non-writeable file
- CP-34313: Coverity: refactor to remove dead code
- CP-34313: Coverity: #if out unused code
- CP-34313: Coverity: remove dead code for ctx_match
- CP-34313: Coverity: call driver td_validate function
- CP-34313: Coverity: remove unreachable code in block_cache_hash
- CP-34313: Coverity: fix STACK_USE errors
- CP-34313: Coverity: ensure nbd id is terminated
- CP-34313: Coverity: use PAGESIZE instead of reading sysconf on each request
- CP-34313: Coverity: use valid printf format string
- CP-34313: Coverity: check that event->fd is valid
- CP-34313: Coverity: close sock in error path
- CP-34313: Coverity: ensure sfd is closed
- CP-34313: Coverity: fix several unused value errors
- Coverity: add model for posix_memalign
- CP-34313: free prv->remote in error path

* Wed Jun 17 2020 Mark Syms <mark.syms@citrix.com> - 3.38.0-1
- CA-340619 - Propagate errors from snaphot creation

* Wed May 20 2020 Mark Syms <mark.syms@citrix.com> - 3.37.0-1
- CA-338603: fix out of band write in tapdisk-control

* Tue Apr 21 2020 Mark Syms <mark.syms@citrix.com> - 3.36.0-1
- CA-338080: prevent segfault if stats have been freed
- CA-338180: Ensure string is terminated
- CA-338180: Correct return type of tapdisk_stats_length
- CA-338176: fix resource leaks in vhd-util copy

* Tue Apr 07 2020 Mark Syms <mark.syms@citrix.com> - 3.35.0-1
- Add some unit tests for tap-ctl
- CA-337493: Fix bug in find minors.

* Wed Mar 25 2020 Mark Syms <mark.syms@citrix.com> - 3.34.0-1
- feat(vhd-util-scan): '-m' supports style brace expressions and pattern list
- fix(vhd-util-scan): compare fnmatch return to FNM_NOMATCH instead of FNM_PATHNAME
- CA-335771: timeouts are deltas not absolute deadlines

* Wed Mar 11 2020 marksy <mark.syms@citrix.com> - 3.33.0-1
- CA-335771: correct missing usage info

* Wed Feb 19 2020 Ming Lu <ming.lu@citrix.com> - 3.32.0-1
- CP-32123: Integrate blktap with CCM openssl 1.1.1

* Tue Dec 10 2019 Mark Syms <mark.syms@citrix.com> - 3.31.0-1
- CP-32675 Use the stable Xen interfaces

* Tue Oct 29 2019 Mark Syms <mark.syms@citrix.com> - 3.30.0-1
- CA-327558: add user-space io_getevents() implementation
- CA-327558: switch to user-space io_getevents
- CA-327558: Do not call fadvise on read cached FD
- Drop libaio-compat.h: libaio.h has everything we need now
- Drop tapdisk-filter.c: dead code
- Drop rwio dead code
- Fix debug mode
- Fix build when TEST is defined
- CA-327558: save and restore entire iocb
- CA-327558: iocb union helper functions
- CA-327558: io merge using pread/pwritev

* Fri Oct 11 2019 Mark Syms <mark.syms@citrix.com> - 3.29.0-1
- Unify definition of LIBBLOCKCRYPTO_NAME
- Add major version to LIBBLOCKCRYPTO_NAME
- CP-30739: enable multi-page rings for tapdisk
- CP-30739: mask the ring events while in polling mode

* Wed Sep 11 2019 Mark Syms <mark.syms@citrix.com> - 3.28.0-1
- CA-326370 Check return code from io_getevents()

* Mon Jun 17 2019 Mark Syms <mark.syms@citrix.com> - 3.27.0-1
- CA-318654: set dependency on xenstored

* Mon Jun 10 2019 Mark Syms <mark.syms@citrix.com> - 3.26.0-1
- CA-320241: remove NBD mirror timeouts, they just add fragility
- CP-27247: Move tapdisk to a blkio cgroup

* Mon May 13 2019 Mark Syms <mark.syms@citrix.com> - 3.25.0-1
- CA-314653: add tracing to nbd failure paths
- CA-314653: log if nbd requests take over 20 seconds to complete

* Tue Apr 16 2019 Mark Syms <mark.syms@citrix.com> - 3.24.0-1
- fix vhd-util keypath validation

* Tue Apr 09 2019 Mark Syms <mark.syms@citrix.com> - 3.23.0-1
- Optimise allocate-and-fill of full blocks

* Wed Mar 06 2019 Mark Syms <mark.syms@citrix.com> - 3.22.0-1
- CA-312256: remove extraneous tracing from libvhd

* Fri Feb 08 2019 Mark Syms <mark.syms@citrix.com> - 3.21.0-1
- Address coverity issue in vhd_cache_load
- CA-307886: add tracing for failure cases
- Fix coverity issues in tests
- CA-310477: fix race in create tap-ctl directory

* Wed Jan 23 2019 Mark Syms <mark.syms@citrix.com> - 3.20.0-1
- CA-306397: amend tracing in physical_device_changed.
- CA-306397: consider empty string read from xs_read to be equiv to NULL

* Tue Jan 08 2019 Mark Syms <mark.syms@citrix.com> - 3.19.0-1
- CA-305951: change xattr_get to tolerate ENOTSUP error

* Mon Dec 17 2018 Mark Syms <mark.syms@citrix.com> - 3.18.0-1
- CA-304648: add guard asserts to prevent overwriting the header
- CA-304653: round up the required number of BAT entries so that the entire data size is accomodated
- CA-304945: Only load crypto library when encryption is used
- CA-304562 Stats use-after-free

* Wed Nov 28 2018 Mark Syms <mark.syms@citrix.com> - 3.17.0-1
- CA-303668: check that both name and new name are passed to vhd-util copy
- CA-303671: initialise variable so that -B functions
- CA-302889: Correct vhd-util copy help strings

* Tue Nov 27 2018 Bob Ball <bob.ball@citrix.com> - 3.16.0-2
- CP-30093: Separate sub-package for vhd-util and dependencies

* Fri Nov 16 2018 Mark Syms <mark.syms@citrix.com> - 3.16.0-1
- CA-299175 Guard against NULL devices
- VHD keyhash support
- VHD encryption support
- remove unused functions
- Only set the image keyhash if we've loaded it
- CP-29602:  remove replication of check for vhd encrpyption
- CP-29690: Update tap-ctl open to take encryption key
- CP-29690: Pass encryption key data down to block-crypto
- CP-29777: VDI.snapshot for encrypted VDIs
- CP-29812: split crypto routines into shared library and dynamically load
- CP-29890: Implement vhd-util copy with optional encryption.

* Mon Oct 15 2018 Mark Syms <mark.syms@citrix.com> - 3.15.0-1
- CP-24320: fix resource leak in vhd-journal.c
- CP-24319: fix resource leak in tapdisk_vbd_add_block_cache
- CP-24321: fix resource leak in vhd_w2u_decode_location
- CP-24323: fix resource leak in vhd_journal_read_batmap_header
- CA-299656: use sizeof(struct sockaddr_in) not the pointer
- Address coverity issues in tapdisk-control.c

* Mon Oct 01 2018 Mark Syms <mark.syms@citrix.com> - 3.14.0-1
- CA-295527: more logging for tap-ctl allocate failures

* Fri Sep 07 2018 Mark Syms <mark.syms@citrix.com> - 3.13.0-1
- CA-295527: Add some more diagnostics so that we know which bit of allocate errors

* Mon Aug 06 2018 Mark Syms <mark.syms@citrix.com> - 3.12.0-1
- CA-227096 Allow stashed passed fds to overwrite with the same name

* Wed Jul 25 2018 Mark Syms <mark.syms@citrix.com> - 3.11.0-1
- CA-294079 Revert "CA-205513: Removing bad fds from the fdset passed to select call."

* Thu Jul 19 2018 Tim Smith <tim.smith@citrix.com> - 3.10.0-2.0
- Add ldconfig in posttrans to support update from older versions

* Mon Jul 16 2018 Mark Syms <mark.syms@citrix.com> - 3.10.0-1
- valve: fix duplicated forwarding

* Wed Jul 11 2018 Mark Syms <mark.syms@citrix.com> - 3.9.0-1
- XOP-944 Fix crashes and errors in stats
- CP-24318: Closed resource leak in vhd_macx_decode_location()
- CA-293563 prevent race when creating blktap/control device node
- Update coverage profile dirs so that product and test code match
- make O_DIRECT optional

* Thu Jun 28 2018 Tim Smith <tim.smith@citrix.com> - 3.8.0-2.0
- Run ldconfig on install/uninstall

* Mon Jun 18 2018 Mark Syms <mark.syms@citrix.com> - 3.8.0-1
- Update specfile template
- Remove VERSION and WHATS_NEW files, this information is in git history and tags
- Remove WHATS_NEW from Makefile.am

* Fri May 25 2018 marksy <mark.syms@citrix.com> - 3.7.0-1.0
- CA-285194: ensure that tapdisk logs if it exits and also on opening its control

* Fri May 25 2018 marksy <mark.syms@citrix.com> - 3.6.0-1.0
- Release 3.6.0

* Tue Apr 10 2018 marksy <mark.syms@citrix.com> - 3.5.0-1.17
- CA-277128: remove redundant, broken RRD code from tapdisk

* Tue Mar 27 2018 marksy <mark.syms@citrix.com> - 3.5.0-1.16
- Gather the gcov coverage files during build

* Fri Feb 16 2018 marksy <mark.syms@citrix.com> - 3.5.0-1.15
- CP-26852: Support building with upstream Linux

* Tue Jan 30 2018 marksy <mark.syms@citrix.com> - 3.5.0-1.14
- Convert patch to use tabs for merge to github
- Reorder patchqueue with patches commited to github
- CA-220042: Add missing half of pull request 191 to patchqueue
- Update patchqueue patch to match the github pull request

* Wed Dec 06 2017 marksy <mark.syms@citrix.com> - 3.5.0-1.13
- CP-20541 Enable conditional coverage build

* Thu Oct 12 2017 marksy <mark.syms@citrix.com> - 3.5.0-1.12
- Patch cleanup

* Wed Oct 11 2017 marksy <mark.syms@citrix.com> - 3.5.0-1.11
- CA-268288: Send logpath as an additional write

* Wed Sep 27 2017 marksy <mark.syms@citrix.com> - 3.5.0-xs.1+1.10
- CP-23545: Extend tap-ctl create to consider CBT parameters
- CP-23920: [Unit test] Increase test coverage for cbt-util coalesce
- CP-24547: [Unit test] Increase test coverage for cbt-util set
