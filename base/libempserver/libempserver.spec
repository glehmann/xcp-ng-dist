Summary: A library of functions for running an emp server
Name: libempserver
Version: 1.0.3
Release: 1
License: BSD
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&prefix=%{name}-%{version}&format=tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: json-c-devel

%description
libempserver is a library of functions for creating an
emp server, to allow an emp client (such as emu-manager) to connect
and control the process.  The emp protocol is intended to be used by
hardware emulators used to support a virtual machine.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
%{__install} -d %{buildroot}/%{_libdir}
%{__install} %{name}.a %{buildroot}/%{_libdir}/

%{__install} -d %{buildroot}/%{_includedir}
%{__install} %{name}.h %{buildroot}/%{_includedir}/
%{__install} emp.h %{buildroot}/%{_includedir}/

%files
%doc LICENSE
%{_libdir}/*
%{_includedir}/*

%changelog
* Mon Apr 09 2018 Simon Rowe <simon.rowe@citrix.com> - 1.0.3-1
- CA-285283: Allow poll to be used in place of select.

* Wed Jan 03 2018 Bob Ball <bob.ball@citrix.com> - 1.0.2-1
- CP-25488: Improve libemp locking

* Wed Dec 13 2017 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.1-1
- Code tidy-ups

* Thu Nov 30 2017 Jennifer Herbert <jennifer.herbert@citrix.com> - 1.0.0-1
- Initial version of libempserver
