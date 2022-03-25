#
# Conditional build:
%bcond_with	tests	# do perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Command Line Interface Formulation Framework
Name:		python-cliff
Version:	2.8.0
Release:	5
License:	Apache
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/9e/26/7db86b6fb7bcf335e691a274b8f5141006ea87e7783e43d7ef5a498a09da/cliff-%{version}.tar.gz
# Source0-md5:	6f1fcd6deb8068984f3f0e594f02f2b7
URL:		https://pypi.python.org/pypi/cliff
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-pbr >= 2.0.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.10.0
BuildRequires:	python-cmd2 >= 0.6.7
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-mock >= 2.0
BuildRequires:	python-openstackdocstheme >= 1.11.0
BuildRequires:	python-prettytable >= 0.7.1
BuildRequires:	python-pyparsing >= 2.1.0
BuildRequires:	python-six >= 1.9.0
BuildRequires:	python-stevedore >= 1.20.0
BuildRequires:	python-subunit >= 0.0.18
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 1.4.0
BuildRequires:	python-unicodecsv >= 0.8.0
BuildRequires:	sphinx-pdg-2 >= 1.6.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-pbr >= 2.0.0
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10.0
BuildRequires:	python3-cmd2 >= 0.6.7
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-mock >= 2.0
BuildRequires:	python3-openstackdocstheme >= 1.11.0
BuildRequires:	python3-prettytable >= 0.7.1
BuildRequires:	python3-pyparsing >= 2.1.0
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-stevedore >= 1.20.0
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 1.4.0
BuildRequires:	sphinx-pdg-3 >= 1.6.2
%endif
%endif
BuildRequires:	sed >= 4.0
Requires:	python-PyYAML >= 3.10.0
Requires:	python-cmd2 >= 0.6.7
Requires:	python-prettytable >= 0.7.1
Requires:	python-pyparsing >= 2.1.0
Requires:	python-six >= 1.9.0
Requires:	python-stevedore >= 1.20.0
Requires:	python-unicodecsv >= 0.8.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cliff is a framework for building command line programs. It uses
setuptools entry points to provide subcommands, output formatters, and
other extensions.

%package -n python3-cliff
Summary:	Command Line Interface Formulation Framework
Group:		Libraries/Python
Requires:	python3-PyYAML >= 3.10.0
Requires:	python3-cmd2 >= 0.6.7
Requires:	python3-prettytable >= 0.7.1
Requires:	python3-pyparsing >= 2.1.0
Requires:	python3-six >= 1.9.0
Requires:	python3-stevedore >= 1.20.0

%description -n python3-cliff
cliff is a framework for building command line programs. It uses
setuptools entry points to provide subcommands, output formatters, and
other extensions.

%prep
%setup -q -n cliff-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install

# python dependency generator does not support conditionals
# remove python2-only dependencies here
sed -i -e"/python_version<'3.0'/,+1 d" $RPM_BUILD_ROOT%{py3_sitescriptdir}/cliff-%{version}-py*.egg-info/requires.txt
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version}
cp -a demoapp/* $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}
cp -a demoapp/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py_sitescriptdir}/cliff
%{py_sitescriptdir}/cliff-%{version}-py*.egg-info
%{_examplesdir}/python-cliff-%{version}
%endif

%if %{with python3}
%files -n python3-cliff
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py3_sitescriptdir}/cliff
%{py3_sitescriptdir}/cliff-%{version}-py*.egg-info
%{_examplesdir}/python3-cliff-%{version}
%endif
