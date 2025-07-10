#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Command Line Interface Formulation Framework
Summary(pl.UTF-8):	Command Line Interface Formulation Framework - szkielet formułowania linii poleceń
Name:		python3-cliff
Version:	4.10.0
Release:	1
License:	Apache
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cliff/cliff-%{version}.tar.gz
# Source0-md5:	084aa6bc49a6c0d574de30ab60218b1a
URL:		https://pypi.org/project/cliff/
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-pbr >= 2.0.0
%if %{with tests}
BuildRequires:	python3-Sphinx >= 5.0.0
BuildRequires:	python3-PyYAML >= 3.12
BuildRequires:	python3-autopage >= 0.4.0
BuildRequires:	python3-cmd2 >= 1.0.0
BuildRequires:	python3-coverage >= 5.0
BuildRequires:	python3-fixtures >= 3.0.0
BuildRequires:	python3-prettytable >= 0.7.2
BuildRequires:	python3-stestr >= 1.0.0
BuildRequires:	python3-stevedore >= 2.0.1
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-openstackdocstheme >= 2.2.1
BuildRequires:	sphinx-pdg-3 >= 2.1.1
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cliff is a framework for building command line programs. It uses
setuptools entry points to provide subcommands, output formatters, and
other extensions.

%description -l pl.UTF-8
cliff to szkielet do budowania programów działających z linii poleceń.
Wykorzystuje punkty wejściowe setuptools do zapewnienia podpoleceń,
funkcje formatujące wyjścia i inne rozszerzenia.

%package apidocs
Summary:	API documentation for Python cliff module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona cliff
Group:		Documentation

%description apidocs
API documentation for Python cliff module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona cliff.

%prep
%setup -q -n cliff-%{version}

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' demoapp/setup.py

%build
export PYTHON="%{__python3}"
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest build-3
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html doc/source doc/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/cliff/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}
cp -a demoapp/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py3_sitescriptdir}/cliff
%{py3_sitescriptdir}/cliff-%{version}-py*.egg-info
%{_examplesdir}/python3-cliff-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,contributors,install,reference,user,*.html,*.js}
%endif
