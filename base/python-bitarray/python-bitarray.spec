%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 

Name:   python-bitarray          
Version:     0.3.5   
Release:        1%{?dist}
Summary:        Efficient Array of Booleans --C Extensions

Group:          Development/Languages
License:        Python
URL:            http://pypi.python.org/pypi/bitarray/
Source0:        http://pypi.python.org/packages/source/b/bitarray/bitarray-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel python-setuptools

%description
Bitarrays are sequence types and behave very much like usual lists.
Eight bits are represented by one byte in contiguous block of memory.
The user can select between two representations; little-endian and big-endian.
Most of the functionality is implemented in C.Methods for accessing the machine
representation are provided. This can be useful when bit level access to binary
files is required, such as portable bitmap image files (.pbm). Also, when 
dealing with compressed data which uses variable bit length encoding
you may find this module useful.

%prep
%setup -q -n bitarray-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE 

%{python_sitearch}/*
 


%changelog
* Wed Apr 08 2009 Ramakrishna Reddy Yekulla <ramkrsna@fedoraproject.org> 0.3.5-1
- Initial RPM release



