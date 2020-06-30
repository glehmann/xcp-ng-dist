Summary: A library of functions for running an emp server
Name: libempserver
Version: 1.1.0
Release: 1%{?dist}
License: BSD

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/libempserver/archive?at=v1.1.0&prefix=libempserver-1.1.0&format=tar.gz#/libempserver-1.1.0.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/libempserver/archive?at=v1.1.0&prefix=libempserver-1.1.0&format=tar.gz#/libempserver-1.1.0.tar.gz) = 35d7c3fa13b60bb3d9863d98a92ae05398211acc


BuildRequires: gcc
BuildRequires: json-c-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
libempserver is a library of functions for creating an
emp server, to allow an emp client (such as emu-manager) to connect
and control the process.  The emp protocol is intended to be used by
hardware emulators used to support a virtual machine.

%prep
%autosetup -p1

%build
%{make_build}

%install
%{makeinstall}

%files
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.1.1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/libempserver/archive?at=v1.1.0&prefix=libempserver-1.1.0&format=tar.gz#/libempserver-1.1.0.tar.gz) = 35d7c3fa13b60bb3d9863d98a92ae05398211acc
Summary: Development headers for libempserver
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
libempserver is a library of functions for creating an
emp server, to allow an emp client (such as emu-manager) to connect
and control the process.  The emp protocol is intended to be used by
hardware emulators used to support a virtual machine.

This package provides documentation and development headers for
libempserver

%files devel
%doc LICENSE
%{_includedir}/emp.h
%{_includedir}/%{name}.h
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so

%changelog
* Thu Mar 19 2020 Jennifer Herbert <jennifer.herbert@citrix.com> - 1.1.0-1
- CA-326958 - Add function to provide default path

* Wed Jul 18 2018 Tim Smith <tim.smith@citrix.com> - 1.0.4-2
- Add ldconfig pre/post scriptlets

* Tue Jul 03 2018 Simon Rowe <simon.rowe@citrix.com> - 1.0.4-1
- CA-293082 - Build libempserver as a dynamic object
- CA-293082 - Set the library SONAME

* Thu Jun 28 2018 Andrew Cooper <andrew.cooper3@citrix.com> - 1.0.3-3
- Build libempserver as a dynamic library

* Wed Jun 20 2018 Tim Smith <tim.smith@citrix.com> - 1.0.3-2
- Create static and devel subpackages to reflect the fact that this is a static
  library used only at build time.

* Mon Apr 09 2018 Simon Rowe <simon.rowe@citrix.com> - 1.0.3-1
- CA-285283: Allow poll to be used in place of select.

* Wed Jan 03 2018 Bob Ball <bob.ball@citrix.com> - 1.0.2-1
- CP-25488: Improve libemp locking

* Wed Dec 13 2017 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.1-1
- Code tidy-ups

* Thu Nov 30 2017 Jennifer Herbert <jennifer.herbert@citrix.com> - 1.0.0-1
- Initial version of libempserver
