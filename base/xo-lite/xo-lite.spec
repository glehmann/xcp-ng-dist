Summary: Xen Orchestra Lite
Name:    xo-lite
Version: 0.14.0
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
cp -a * %{buildroot}/opt/xensource/www
# We are removing unnecessary files.
rm %{buildroot}/opt/xensource/www/LICENSE %{buildroot}/opt/xensource/www/CHANGELOG.md
# The build.json file is a temporary file that appeared in August 2025, with version 0.14.0. It should disappear eventually.
rm %{buildroot}/opt/xensource/www/build.json

%files
%license LICENSE
/opt/xensource/www/assets
/opt/xensource/www/index.html
/opt/xensource/www/favicon.svg
/opt/xensource/www/manifest.webmanifest
/opt/xensource/www/xolite.html
%doc CHANGELOG.md

%changelog
* Thu Aug 28 2025 Gael Duperrey <gduperrey@vates.tech> - 0.14.0-1
- Update to version 0.14.0

* Thu Aug 07 2025 Gael Duperrey <gduperrey@vates.tech> - 0.13.1-1
- Update to version 0.13.1

* Fri Aug 01 2025 Gael Duperrey <gduperrey@vates.tech> - 0.13.0-1
- Update to version 0.13.0

* Fri Jul 04 2025 Gael Duperrey <gduperrey@vates.tech> - 0.12.1-1
- Update to version 0.12.1

* Tue Jul 01 2025 Gael Duperrey <gduperrey@vates.tech> - 0.12.0-1
- Update to version 0.12.0

* Wed May 28 2025 Gael Duperrey <gduperrey@vates.tech> - 0.11.0-1
- Update to version 0.11.0

* Mon May 12 2025 Gael Duperrey <gduperrey@vates.tech> - 0.10.1-1
- Update to version 0.10.1

* Wed Apr 02 2025 Gael Duperrey <gduperrey@vates.tech> - 0.9.1-1
- Update to version 0.9.1

* Thu Feb 27 2025 Gael Duperrey <gduperrey@vates.tech> - 0.8.0-1
- Update to version 0.8.0

* Wed Feb 05 2025 Gael Duperrey <gduperrey@vates.tech> - 0.7.1-1
- Update to version 0.7.1

* Thu Jan 30 2025 Gael Duperrey <gduperrey@vates.tech> - 0.7.0-1
- Update to version 0.7.0

* Mon Dec 02 2024 Gael Duperrey <gduperrey@vates.tech> - 0.6.0-1
- Update to version 0.6.0

* Thu Oct 31 2024 Gael Duperrey <gduperrey@vates.tech> - 0.5.0-1
- Update to version 0.5.0

* Mon Oct 14 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.7-2
- Add missing xolite.html

* Thu Aug 01 2024 Gael Duperrey <gduperrey@vates.tech> - 0.2.7-1
- Update to version 0.2.7

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
