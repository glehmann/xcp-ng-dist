Name:           xcp-featured
Version:        1.1.0
Release:        2%{?dist}
Summary:        XCP-ng feature daemon
Group:          System/Hypervisor
License:        ISC
URL:            https://github.com/xcp-ng/xcp-featured
Source0:        https://github.com/xcp-ng/xcp-featured/archive/v%{version}/xcp-featured-%{version}.tar.gz
Source1:        v6d.service
BuildRequires:  systemd-devel
BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  xapi-client-devel

%{systemd_requires}

%description
This package contains an RPC serving daemon, which reports the features
available on an xcp-ng host.

%prep
%autosetup -p1

%build
eval $(opam config env --root=/usr/lib/opamroot)
DESTDIR=%{buildroot} %{__make}

%install
eval $(opam config env --root=/usr/lib/opamroot)
DESTDIR=%{buildroot} LIBEXECDIR=/opt/xensource/libexec %{__make} install
ln -s /opt/xensource/libexec/xcp-featured %{buildroot}/opt/xensource/libexec/v6d
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/v6d.service

%post
%systemd_post v6d.service

%preun
%systemd_preun v6d.service

%postun
%systemd_postun v6d.service

%files
/opt/xensource/libexec/v6d
/opt/xensource/libexec/xcp-featured
%{_unitdir}/v6d.service

%changelog
* Tue Jul 24 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-2
- Fix upgrade from previous version (no more removed symlink)
- Add systemd requires for scriptlets
- Fix paths

* Mon Jul 02 2018 John Else <john.else@gmail.com> - 1.1.0-1
- Update to build against new RPC library

* Wed Apr 25 2018 John Else <john.else@gmail.com> - 1.0.1-2
- Prevent symlink deletion on upgrade

* Mon Apr 09 2018 John Else <john.else@gmail.com> - 1.0.1-1
- Add additional feature flags

* Sun Mar 25 2018 John Else <john.else@gmail.com> - 1.0.0-1
- Initial package
