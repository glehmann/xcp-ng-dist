%global package_speccommit c087a0f56097eab1a2ed9ea8a30c36cc9010221e
%global package_srccommit v1.1.1
Name: vmss
Version: 1.1.1
Release: 2%{?xsrel}%{?dist}
Summary: REQ-277 schedule snapshots feature
License: GNU / GPLv2
Source0: vmss-1.1.1.tar.gz
BuildArch: noarch
BuildRequires: python-devel


%description
This package contains scheduled snapshots feature plugins and the associated cron job

%prep

%autosetup -p1

%build
DESTDIR=$RPM_BUILD_ROOT make

%install
DESTDIR=$RPM_BUILD_ROOT make install

%clean
rm -rf $RPM_BUILD_ROOT

%post

%preun

%files
%defattr(-,root,root,-)
/etc/xapi.d/plugins/vmss
/etc/cron.d/vmss.cron
/etc/xensource/bugtool/VM-snapshot-schedule/vmss.xml
/etc/xensource/bugtool/VM-snapshot-schedule.xml

%config /etc/logrotate.d/VMSSlog

%changelog
* Thu Apr 28 2022 Rob Hoes <rob.hoes@citrix.com> - 1.1.1-2
- Bump release and rebuild

* Wed Jul 28 2020 Ben Sims <ben.sims@citrix.com> - 1.1.1-1
- CA-342874 Correct error warning levels.

* Mon Feb 20 2017 Sharath Babu <sharath.babu@citrix.com> 1.0.0-1
- Initial Commit
