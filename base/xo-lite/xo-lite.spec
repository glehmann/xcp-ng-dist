Summary: Xen Orchestra Lite
Name:    xo-lite
Version: 0.2.3
Release: 1%{?dist}
License: AGPL3-only
URL:     https://github.com/vatesfr/xen-orchestra

BuildArch: noarch

Source0: https://github.com/vatesfr/xen-orchestra/releases/download/%{name}-v%{version}/%{name}-%{version}.tar.gz

%description
This package contains Xen Orchestra Lite, a lightweight version of the Xen
Orchestra Appliance for single-host administration, running directly from your
browser without having to deploy anything.

%prep
%autosetup -p1

%install
install -d -m 755 %{buildroot}/opt/xensource/www
cp -a assets index.html favicon.svg manifest.webmanifest %{buildroot}/opt/xensource/www

%files
%license LICENSE
/opt/xensource/www/assets
/opt/xensource/www/index.html
/opt/xensource/www/favicon.svg
/opt/xensource/www/manifest.webmanifest
%doc CHANGELOG.md

%changelog
* Mon Jun 03 2024 Gael Duperrey <gduperrey@vates.tech> - 0.2.3-1
- Update to version 0.2.3

* Thu May 02 2024 Gael Duperrey <gduperrey@vates.tech> - 0.2.2-1
- Update to version 0.2.2

* Tue Apr 02 2024 Gael Duperrey <gduperrey@vates.tech> - 0.2.1-1
- Update to version 0.2.1

* Thu Feb 29 2024 Gael Duperrey <gduperrey@vates.tech> - 0.2.0-1
- Update to version 0.2.0

* Tue Sep 12 2023 Thierry Escande <thierry.escande@vates.tech> - 0.1.3-1
- Initial release
