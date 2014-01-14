%{?_javapackages_macros:%_javapackages_macros}
Name:       jbosscache-core
Version:    3.2.8
Release:    9.0%{?dist}
Summary:    JBoss objects cache


License:    LGPLv2+
URL:        http://jboss.org/jbosscache
# svn export http://anonsvn.jboss.org/repos/jbosscache/core/tags/3.2.8.GA jbosscache-core-3.2.8
# tar cJf jbosscache-core-3.2.8.tar.xz jbosscache-core-3.2.8
Source0:    %{name}-%{version}.tar.xz
Patch0:     %{name}-jgroups212.patch

BuildRequires:  maven-local
BuildRequires:  maven-install-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-surefire
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  jbosscache-common-parent
BuildRequires:  jdbm
BuildRequires:  c3p0
BuildRequires:  jcip-annotations
BuildRequires:  jgroups212
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  jboss-common-core
BuildRequires:  apache-commons-logging
BuildRequires:  jboss-transaction-1.1-api

Requires:       java
Requires:       jpackage-utils
Requires:       jgroups212
Requires:       jboss-transaction-1.1-api
Requires:       jboss-common-core
Requires:       jdbm
Requires:       c3p0
Requires:       jcip-annotations
Requires:       apache-commons-logging

BuildArch:      noarch

%description
A library that caches frequently accessed Java objects in order to
dramatically improve the performance of applications.

%package javadoc
Summary:   Javadoc for %{name}

Requires:  jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q
find . -name \*.jar -exec rm -f {} \;

# Remove optional dependencies
%pom_remove_dep com.sleepycat:je
%pom_remove_dep net.noderunner:amazon-s3
# Test dependencies
%pom_remove_dep hsqldb:hsqldb
%pom_remove_dep jboss.jbossts:jbossjta
%pom_remove_dep jboss.jbossts:jbossjts
%pom_remove_dep jboss.jbossts:jbossts-common
%pom_remove_dep net.noderunner:http
%pom_remove_dep org.jboss.logging:jboss-logging-spi

# Remove code for amazon-s3 and berkleydb-je dependencies
rm -rf src/main/java/org/jboss/cache/loader/{s3,bdbje}

# Fix JBoss transaction API dependency
sed -i -e "s|<groupId>org.jboss.javaee</groupId>|<groupId>org.jboss.spec.javax.transaction</groupId>|" \
    -e "s|<artifactId>jboss-transaction-api</artifactId>|<artifactId>jboss-transaction-api_1.1_spec</artifactId>|" \
    -e "s|<version>1.0.1.GA</version>|<version>1.0.1-SNAPSHOT</version>|" pom.xml

%patch0 -p1

%build
# Not running tests due to missing dependencies
mvn-rpmbuild install -Dmaven.test.skip=true \
    -Dproject.build.sourceEncoding=UTF-8 \
    javadoc:aggregate

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 target/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if 0%{?fedora}
%else
sed -i 's|${jbosscache-core-version}|%{version}.GA|' %{buildroot}%{_mavendepmapfragdir}/*
%endif

%files
%doc README-*.txt src/main/release/LICENSE-lgpl-2.1.txt src/main/release/README.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc src/main/release/LICENSE-lgpl-2.1.txt
%{_javadocdir}/%{name}

%changelog
* Sun Aug 11 2013 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-9
- Add BR for maven-install-plugin
- Remove pom test dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.2.8-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Oct 01 2012 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-5
- Remove custom depmap file (now using pom macros and editing pom file)
- Add license file to javadoc package

* Thu Aug 23 2012 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-4
- Updated pom reference to jgroups to use jgroups212 instead

* Wed Aug 08 2012 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-3
- Using custom depmap
- Corrected license type

* Tue Aug 07 2012 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-2
- Updated Requires section

* Tue Jul 24 2012 Matt Spaulding <mspaulding06@gmail.com> - 3.2.8-1
- Initial package

