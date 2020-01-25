#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	java_sun	# build with java-sun

%define		shortname	looks
%define		srcname		jgoodies-%{shortname}
%define		ver	%(echo %{version} | tr . _)
Summary:	Free high-fidelity Windows and multi-platform appearance
Name:		java-%{srcname}
Version:	2.2.1
Release:	2
License:	BSD
Group:		Libraries/Java
URL:		http://www.jgoodies.com/freeware/looks/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{shortname}-%{ver}.zip
# Source0-md5:	0d191029f45b81a90c835263e0c5af2e
Patch0:		build.patch
Patch1:		no-com-sun.patch
Patch2:		remove-jdk-stuff.patch
Patch3:		demo-manifest.patch
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils >= 1.6
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The JGoodies look&feels make your Swing applications and applets look
better. They have been optimized for readability, precise micro-design
and usability.

Main Benefits:

- Improved readability, legibility and in turn usability.
- Improved aesthetics - looks good on the majority of desktops
- Simplified multi-platform support
- Precise micro-design

%package javadoc
Summary:	Javadoc documentation for JGoodies Looks
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description javadoc
The JGoodies look&feels make your Swing applications and applets look
better. They have been optimized for readability, precise micro-design
and usability.

This package contains the Javadoc documentation for JGoodies Looks.

%package doc
Summary:	Manual for %{srcname}
Summary(fr.UTF-8):	Documentation pour %{srcname}
Summary(it.UTF-8):	Documentazione di %{srcname}
Summary(pl.UTF-8):	Podręcznik dla %{srcname}
Group:		Documentation

%description doc
Documentation for %{srcname}.

%description doc -l fr.UTF-8
Documentation pour %{srcname}.

%description doc -l it.UTF-8
Documentazione di %{srcname}.

%description doc -l pl.UTF-8
Dokumentacja do %{srcname}.

%package demo
Summary:	Demo applications for the JGoodies look&feels
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description demo
This package contains demo applications for the JGoodies look&feels,
including the "uif_lite" classes.

%prep
%setup -q -n %{shortname}-%{version}
%undos build.xml
%undos *.txt *.html docs/*.* docs/guide/*.*
find -name '*.java' -print0 | xargs -0 %undos

%patch0 -p1

# unzip the look&feel settings from bundled jar before we delete it
# (taken from Gentoo ebuild)
unzip -j %{shortname}-%{version}.jar META-INF/services/javax.swing.LookAndFeel \
|| die "unzip of javax.swing.LookAndFeel failed"
# and rename it to what build.xml expects
mv javax.swing.LookAndFeel all.txt

# Delete pre-generated stuff we don't want
rm %{shortname}-%{version}.jar
rm -r docs/api

# Delete the whole Windows L&F because it depends on com.sun.java packages
# (Unless we're compiling with a Sun JVM)
%if %{with java_sun}
%else
%patch1 -p1
rm -r src/core/com/jgoodies/looks/windows
%endif

# Delete a file that's a copy of something distributed by Sun, and patch the files that
# use it so they don't.
rm src/core/com/jgoodies/looks/common/ExtBasicArrowButtonHandler.java
%patch2 -p1

%patch3 -p1

%build
%ant -Ddescriptors.dir=. compile jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -dp $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{shortname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
cp -p build/demo.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-demo-%{version}.jar
ln -s %{srcname}-demo-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-demo.jar

%if %{with javadoc}
install -dp $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc RELEASE-NOTES.txt LICENSE.txt README.html
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%files doc
%defattr(644,root,root,755)
%doc docs/*

%files demo
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-demo.jar
%{_javadir}/%{srcname}-demo-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
