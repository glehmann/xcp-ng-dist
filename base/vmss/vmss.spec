Name: vmss
Version: 1.1.0
Release: 1
Summary: REQ-277 schedule snapshots feature 
License: GNU / GPLv2

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/vmss/archive?at=1.1.0&prefix=vmss-1.1.0&format=tar.gz#/vmss-1.1.0.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/vmss/archive?at=1.1.0&prefix=vmss-1.1.0&format=tar.gz#/vmss-1.1.0.tar.gz) = 191899405f39790b2c5bad466c8e8ed1c56ed0cb

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
* Mon Feb 20 2017 Sharath Babu <sharath.babu@citrix.com> 1.0.0-1
- Initial Commit
