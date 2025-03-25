#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Command Line Interface Formulation Framework
Summary(pl.UTF-8):	Command Line Interface Formulation Framework - szkielet formułowania linii poleceń
Name:		python3-cliff
Version:	4.9.1
Release:	1
License:	Apache
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cliff/cliff-%{version}.tar.gz
# Source0-md5:	7f6a2a8046eb190aaaff1adf5fed2f27
URL:		https://pypi.org/project/cliff/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-pbr >= 2.0.0
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.12
BuildRequires:	python3-cmd2 >= 0.8.0
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-openstackdocstheme >= 1.11.0
BuildRequires:	python3-prettytable >= 0.7.2
BuildRequires:	python3-pyparsing >= 2.1.0
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-stevedore >= 2.0.1
BuildRequires:	python3-subunit >= 1.0.0
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
BuildRequires:	sphinx-pdg-3 >= 1.7.0
%endif
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.9
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

%prep
%setup -q -n cliff-%{version}

%build
export PYTHON="%{__python3}"
%py3_build %{?with_tests:test}

%if %{with tests}
%{__rm} -r .testrepository
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/cliff/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}
cp -a demoapp/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-cliff-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py3_sitescriptdir}/cliff
%{py3_sitescriptdir}/cliff-%{version}-py*.egg-info
%{_examplesdir}/python3-cliff-%{version}
