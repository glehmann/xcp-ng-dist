Summary: blktap user space utilities
Name: blktap
Version: 3.5.0
Release: 1.17
License: BSD
Group: System/Hypervisor
URL: https://github.com/xapi-project/blktap
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
Patch0: pull_request_228__CA-222124_Handle_race_condition_in_tap-ctl_spawn
Patch1: pull_request_229__ca-223652__add_delay_to_reduce_number_of_syslog_messages
Patch2: pull_request_231__cp-14449__fix_version_and_release_tag_in_specfile
Patch3: pull_request_232__CA-227162_enable_tapdisk_forced_shutdown_mode
Patch4: pull_request_188__introduce_a_new_block_backend_called_ntnx
Patch5: pull_request_191__CA-220042_sigact.sa_mask_is_not_initialized_CID-5755
Patch6: pull_request_227__CA-217394-Handle-scheduler-uuid-data-type-overflow-in-tapdisk
Patch7: pull_request_215__CP-18038_fix_multiple_resource_leaks
Patch8: pull_request_219__ca-221904__vhd_create_einval_report_errors
Patch9: pull_request_233__CP-19856_add_a_check_to_force_o_dsync_if_needed
Patch10: add_coverity_model.c_to_support_asprintf
Patch11: pull_request_230__CA-225067-tap_ctl_-spawn-create-move-tapdisk-to-cgro
Patch12: pull_request_236_1__clean-up_maintainers_file
Patch13: pull_request_236_2__cp-16813__package_basic_doc_files
Patch14: pull_request_240__CA-253485__Fix_udev_rules_to_prevent_td_devices_being_bound_by_Dom0
Patch15: pull_request_235__ca-220608__corrected_potential_memory_leak
Patch16: CA-250385-Check-if-vbd-image-is-in-chain-before-retr.patch
Patch17: ca-220510__initialsed_vhd_file_table_pointer_before_use.patch
Patch18: CP-23825__Structure_lvm-util_as_a_business_logic_library_with_an_execution_wrapper
Patch19: CP-20827__Enable-block-log-layer
Patch20: CP-21766__Cleaned-up-bitmap-ops-for-CBT
Patch21: CP-21443__Implement-metadata-file-memory-mapping
Patch22: CP-22175__enhance_tap-ctl_pause_to_accept_additional_parameters
Patch23: CP-22206__added_log-util_tool_for_cbt_metadata_manipulation
Patch24: CP-22489__extend_cbt-util_to_read_cbt_log
Patch25: CA-255200__correct_error_handling_for_file_operations
Patch26: break_cbt-util_up_into_a_main_and_a_convenience_function
Patch27: Add_unit_test_foundations_for_blktap_and_cbtutil
Patch28: Fix-unit-test-build-in-rpmbuild-mock
Patch29: CA-255448__ensure_tapdisk_unmaps_the_logfile_on_pause
Patch30: Enable_coverage_for_mockatests
Patch31: Refactor_CBT_unit_test_code_into_separate_compilation_modules
Patch32: CP-22685__Add_unit_tests_for_cbt-util_get
Patch33: CP-22685__add_test_results_to_results_RPM
Patch34: CP-22686__Add_unit_tests_for_cbt-util_create
Patch35: CP-22601__Calculate_log_bit_based_CBT_block_size
Patch36: Fill_in_missing_unit_tests_for_command_lookup
Patch37: CP-22833__Extend_cbt-util_to_read_bitmap_from_log_file
Patch38: CP-22972__Added_unit_tests_for_cbt-util_get_bitmap
Patch39: CP-23274__Move_wrappers_to_a_separate_library
Patch40: CP-23564__Add_size_field_to_metadata_log
Patch41: CP-23548__Implement_cbt_util_coalesce
Patch42: CP-23548__Unit_tests_for_cbt-util_coalesce
Patch43: CA-263485__Debug_logs_for_bitmap_file_operations
Patch44: cp-23918__create_unit_tests_for_cbt-util_set.patch
Patch45: cp-23545__extend_tap-ctl_create_to_consider_cbt_parameters.patch
Patch46: cp-23920__unit_test_increase_coverage_for_cbt-util_coalesce.patch
Patch47: cp-24547__unit_test_increase_test_coverage_for_cbt-util_set.patch
Patch48: CA-268288__Send_logpath_as_an_additional_write
Patch49: CA-260195__Tidy_up_indentation
Patch50: CA-260195__only_log_once_on_watchdog_alert
Patch51: CA-254690__Fix_indentation_prior_to_change
Patch52: CA-254690__Add_a_flag_to_control_logging_based_on_call_context
Patch53: CA-260298__log_the_device_with_no_pe_start
Patch54: add_GCOV_flags.patch
Patch55: pull_request_191__CA-220042_sigact.sa_mask_is_not_initialized_CID-5755_2
Patch56: CP-26852__support-linux-upstream.patch
Patch57: Gather_the_gcov_coverage_files_during_build
Patch58: CA-277128__remove_redundant_broken_RRD_code_from_tapdisk
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/blktap.pg/archive?at=1.17&format=tar#/blktap.patches.tar) = 2d8730dda5145d43e65a4fcd03acf0cfb6682fac

BuildRoot: %{_tmppath}/%{name}-%{release}-buildroot
Obsoletes: xen-blktap
BuildRequires: e2fsprogs-devel, libaio-devel, systemd, autogen, autoconf, automake, libtool, libuuid-devel
BuildRequires: xen-devel, kernel-headers, xen-dom0-libs-devel, zlib-devel, xen-libs-devel, libcmocka-devel, lcov, git
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

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
Obsoletes: xen-blktap

%description devel
Blktap and VHD development files.

%prep
%autosetup -p1 -S git

%build
sh autogen.sh
%configure
%{?cov_wrap} make %{?coverage:GCOV=true}

%check
make check || (find mockatests -name \*.log -print -exec cat {} \; && false)
./collect-test-results.sh %{buildroot}/testresults

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
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
%{_libdir}/*.so
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
%{_sbindir}/part-util
%{_sbindir}/vhdpartx
%{_libexecdir}/tapdisk
%{_sysconfdir}/logrotate.d/blktap
%{_sysconfdir}/xensource/bugtool/tapdisk-logs.xml
%{_sysconfdir}/xensource/bugtool/tapdisk-logs/description.xml
%{_localstatedir}/log/blktap
%{_unitdir}/tapback.service
%{_unitdir}/cpumond.service

%files devel
%defattr(-,root,root,-)
%doc
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/vhd/*
%{_includedir}/blktap/*
%if 0%{?coverage:1}
/%{name}-%{version}.gcno.tar.bz2
%endif

%post
%systemd_post tapback.service
%systemd_post cpumond.service

%preun
%systemd_preun tapback.service
%systemd_preun cpumond.service

%postun
%systemd_postun tapback.service
%systemd_postun cpumond.service
if [ $1 -eq 0 ]; then
    rm -f %{_sysconfdir}/udev/rules.d/65-md-incremental.rules
fi

%changelog
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


%package testresults
Group:    System/Hypervisor
Summary:  test results for blktap package

%description testresults
The package contains the build time test results for the blktap package

%files testresults
/testresults
