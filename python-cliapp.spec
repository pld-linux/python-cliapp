#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	cliapp
Summary:	Python framework for Unix command line programs
Name:		python-%{module}
Version:	1.20130808
Release:	1
License:	GPL v2+
Group:		Libraries/Python
Source0:	http://ftp.debian.org/debian/pool/main/p/python-%{module}/%{name}_%{version}.orig.tar.gz
# Source0-md5:	1ba6cab0430c4a85687b2fa48a646059
URL:		http://liw.fi/cliapp
BuildRequires:	python-Sphinx
BuildRequires:	python-coverage-test-runner
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cliapp is a Python framework for Unix-like command line programs. It
contains the typical stuff such programs need to do, such as parsing
the command line for options, and iterating over input files.

%package doc
Summary:	Documentation for %{module}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the documentation for %{module}, a Python
framework for Unix command line programs.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with tests}
# CoverageTestRunner trips up on build directory
# so need to run this before setup.py
rm -rf build
%{__make} check
%endif

%{__python} setup.py build

# Build documentation
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# don't package internal tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/cliapp/*_tests.py*

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%{_mandir}/man5/cliapp.5*
%dir %{py_sitescriptdir}/cliapp
%{py_sitescriptdir}/cliapp/*.py[co]
%{py_sitescriptdir}/cliapp-%{version}-py*.egg-info

%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/*
