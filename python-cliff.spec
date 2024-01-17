#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Command Line Interface Formulation Framework
Summary(pl.UTF-8):	Command Line Interface Formulation Framework - szkielet formułowania linii poleceń
Name:		python-cliff
# keep 2.x here for python2 support
Version:	2.18.0
Release:	1
License:	Apache
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cliff/cliff-%{version}.tar.gz
# Source0-md5:	66490f2c437f543f32afe9e518e3c080
Patch0:		%{name}-prettytable.patch
Patch1:		%{name}-mock.patch
Patch2:		%{name}-py310.patch
Patch3:		%{name}-py2-test.patch
URL:		https://pypi.org/project/cliff/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr >= 2.0.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.12
BuildRequires:	python-cmd2 >= 0.8.0
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-mock >= 2.0
BuildRequires:	python-openstackdocstheme >= 1.11.0
BuildRequires:	python-prettytable >= 0.7.2
BuildRequires:	python-pyparsing >= 2.1.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-stevedore >= 1.20.0
BuildRequires:	python-subunit >= 1.0.0
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 2.2.0
BuildRequires:	python-unicodecsv >= 0.8.0
BuildRequires:	sphinx-pdg-2 >= 1.7.0
%endif
%endif
%if %{with python3}
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
BuildRequires:	python3-stevedore >= 1.20.0
BuildRequires:	python3-subunit >= 1.0.0
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
BuildRequires:	sphinx-pdg-3 >= 1.7.0
%endif
%endif
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.7
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

%package -n python3-cliff
Summary:	Command Line Interface Formulation Framework
Summary(pl.UTF-8):	Command Line Interface Formulation Framework - szkielet formułowania linii poleceń
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-cliff
cliff is a framework for building command line programs. It uses
setuptools entry points to provide subcommands, output formatters, and
other extensions.

%description -n python3-cliff -l pl.UTF-8
cliff to szkielet do budowania programów działających z linii poleceń.
Wykorzystuje punkty wejściowe setuptools do zapewnienia podpoleceń,
funkcje formatujące wyjścia i inne rozszerzenia.

%prep
%setup -q -n cliff-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%if %{with python2}
export PYTHON="%{__python}"
%py_build %{?with_tests:test}

%if %{with tests}
%{__rm} -r .testrepository
%endif
%endif

%if %{with python3}
export PYTHON="%{__python3}"
%py3_build %{?with_tests:test}

%if %{with tests}
%{__rm} -r .testrepository
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
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
