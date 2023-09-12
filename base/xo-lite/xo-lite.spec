Summary: Xen Orchestra Lite
Name:    xo-lite
Version: 0.1.3
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
cp -a assets index.html favicon.ico %{buildroot}/opt/xensource/www

%files
%license LICENSE
/opt/xensource/www/assets
/opt/xensource/www/index.html
/opt/xensource/www/favicon.ico

%changelog
* Tue Sep 12 2023 Thierry Escande <thierry.escande@vates.tech> - 0.1.3-1
- Initial release
