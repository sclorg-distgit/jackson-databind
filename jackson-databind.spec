%{?scl:%scl_package jackson-databind}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:          %{?scl_prefix}jackson-databind
Version:       2.6.3
Release:       2.%{baserelease}%{?dist}
Summary:       General data-binding package for Jackson (2.x)
License:       ASL 2.0 and LGPLv2+
URL:           http://wiki.fasterxml.com/JacksonHome
Source0:       https://github.com/FasterXML/jackson-databind/archive/%{pkg_name}-%{version}.tar.gz

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson:jackson-parent:pom:)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-annotations) >= 2.4.1
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-core) >= 2.4.1
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-antrun-plugin)

BuildArch:     noarch

%description
General data-binding functionality for Jackson:
works on core streaming API.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

cp -p src/main/resources/META-INF/LICENSE .
cp -p src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

# unavailable test deps
%pom_remove_dep javax.measure:jsr-275
rm src/test/java/com/fasterxml/jackson/databind/introspect/NoClassDefFoundWorkaroundTest.java
%pom_xpath_remove pom:classpathDependencyExcludes

%pom_xpath_inject "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:configuration" "<additionalparam>-Xdoclint:none</additionalparam>"
%pom_xpath_remove pom:failOnError

# org.powermock.reflect.exceptions.FieldNotFoundException: Field 'fTestClass' was not found in class org.junit.internal.runners.MethodValidator.
rm src/test/java/com/fasterxml/jackson/databind/type/TestTypeFactoryWithClassLoader.java

# Off test that require connection with the web
rm src/test/java/com/fasterxml/jackson/databind/ser/TestJdkTypes.java \
 src/test/java/com/fasterxml/jackson/databind/deser/TestJdkTypes.java \
 src/test/java/com/fasterxml/jackson/databind/TestJDKSerialization.java

%mvn_file : %{pkg_name}
%pom_remove_plugin com.google.code.maven-replacer-plugin:replacer
%pom_add_plugin org.apache.maven.plugins:maven-antrun-plugin \
  "<executions><execution><id>process-packageVersion</id><phase>generate-sources</phase></execution></executions>"
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x

%mvn_build -f -- -Dmaven.test.failure.ignore=true
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc README.md release-notes/*
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 2.6.3-2.2
- Avoid usage of unavailable powermock testing lib

* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 2.6.3-2.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 gil cattaneo <puntogil@libero.it> 2.6.3-1
- update to 2.6.3

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 2.6.2-1
- update to 2.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Sat Sep 20 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Wed Jul 23 2014 gil cattaneo <puntogil@libero.it> 2.4.1.3-1
- update to 2.4.1.3

* Thu Jul 03 2014 gil cattaneo <puntogil@libero.it> 2.4.1.1-1
- update to 2.4.1.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-databind

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-databind

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm
