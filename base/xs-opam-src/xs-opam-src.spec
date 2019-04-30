Name: xs-opam-src
Version: 5.0.0
Release: 1%{?dist}
Summary: Opam repository
License: Various
AutoReqProv: no

%description
Opam repository containing all upstream and development libraries
required for building the OCaml components in the XS Toolstack.

%prep
%build
%install

# create opam root
mkdir -p  %{buildroot}/usr/lib/opamroot
chmod 777 %{buildroot}/usr/lib/opamroot


%files
/usr/lib/opamroot
%attr(777, root, wheel) /usr/lib/opamroot

%changelog
* Wed Oct 03 2018 Christian Lindig <christian.lindig@citrix.com> - 5.0.0-1
- Use Opam 2.0.0
