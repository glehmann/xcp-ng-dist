Name:           xcp-clipboardd
Version:        1.0.3
Release:        6%{?dist}
Summary:        Daemon to share a virtualized Windows clipboard
License:        GPLv3
URL:            https://github.com/xcp-ng/xcp-clipboardd
Source0:        https://github.com/xcp-ng/xcp-clipboardd/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  xen-libs-devel

Obsoletes:      xs-clipboardd

%description
Share clipboard between guest Windows and host with VNC.

%prep
%autosetup -p1

%build
mkdir build && cd build
%cmake3 .. -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/xensource
make

%install
cd build
make install

%files
%doc LICENSE README.md
/opt/xensource/libexec/xcp-clipboardd

%changelog
* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.3-6
- Rebuild for XCP-ng 8.2

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.3-5
- Rebuild for XCP-ng 8.1

* Thu May 02 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.3-4
- Rebuild for XCP-ng 8.0.0

* Thu Mar 28 2019 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.3-1
- Initial package
