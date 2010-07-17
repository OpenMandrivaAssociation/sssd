%define servicename sssd
%define sssdstatedir %{_localstatedir}/lib/sss
%define dbpath %{sssdstatedir}/db
%define pipepath %{sssdstatedir}/pipes
%define pubconfpath %{sssdstatedir}/pubconf

%define dhash_version 0.4.0
%define path_utils_version 0.2.0
%define collection_version 0.4.0
%define ini_config_version 0.5.0
%define refarray_version 0.1.0

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

Name:       sssd
Version:    1.2.1
Release:    %mkrel 1
Group:      System/Libraries
Summary:    System Security Services Daemon
License:    GPLv3+
URL:        http://fedorahosted.org/sssd/
Source0:    https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
Patch0:     sssd-1.2.0-fix-linking.patch

Requires: libldb >= 0.9.3
Requires: libtdb >= 1.1.3
Requires: sssd-client = %{version}-%{release}
Requires: libdhash = %{dhash_version}-%{release}
Requires: libcollection = %{collection_version}-%{release}
Requires: libini_config = %{ini_config_version}-%{release}
Requires: cyrus-sasl-gssapi
Requires: keyutils-libs
Requires(post): python
Requires(preun):  initscripts chkconfig
Requires(postun): /sbin/service

BuildRequires: popt-devel
BuildRequires: talloc-devel
BuildRequires: tevent-devel
BuildRequires: tdb-devel
BuildRequires: ldb-devel
BuildRequires: semanage-devel
BuildRequires: dbus-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: pcre-devel
BuildRequires: xsltproc
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: krb5-devel
BuildRequires: c-ares-devel
BuildRequires: python-devel
BuildRequires: check-devel
BuildRequires: doxygen
BuildRequires: keyutils-devel
BuildRequires: bind-utils

BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

%package client
Summary: SSSD Client libraries for NSS and PAM
Group: System/Libraries
License: LGPLv3+

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%package -n libdhash
Summary: Dynamic hash table
Group: Development/Libraries
Version: %{dhash_version}
License: LGPLv3+

%description -n libdhash
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%package -n libdhash-devel
Summary: Development files for libdhash
Group: Development/Libraries
Version: %{dhash_version}
Requires: libdhash = %{dhash_version}-%{release}
License: LGPLv3+

%description -n libdhash-devel
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%package -n libpath_utils
Summary: Filesystem Path Utilities
Group: Development/Libraries
Version: %{path_utils_version}
License: LGPLv3+

%description -n libpath_utils
Utility functions to manipulate filesystem pathnames

%package -n libpath_utils-devel
Summary: Development files for libpath_utils
Group: Development/Libraries
Version: %{path_utils_version}
Requires: libpath_utils = %{path_utils_version}-%{release}
License: LGPLv3+

%description -n libpath_utils-devel
Utility functions to manipulate filesystem pathnames

%package -n libcollection
Summary: Collection data-type for C
Group: Development/Libraries
Version: %{collection_version}
License: LGPLv3+

%description -n libcollection
A data-type to collect data in a heirarchical structure for easy iteration
and serialization

%package -n libcollection-devel
Summary: Development files for libcollection
Group: Development/Libraries
Version: %{collection_version}
Requires: libcollection = %{collection_version}-%{release}
License: LGPLv3+

%description -n libcollection-devel
A data-type to collect data in a heirarchical structure for easy iteration
and serialization

%package -n libini_config
Summary: INI file parser for C
Group: Development/Libraries
Version: %{ini_config_version}
Requires: libcollection = %{collection_version}-%{release}
License: LGPLv3+

%description -n libini_config
Library to process config files in INI format into a libcollection data
structure

%package -n libini_config-devel
Summary: Development files for libini_config
Group: Development/Libraries
Version: %{ini_config_version}
Requires: libini_config = %{ini_config_version}-%{release}
License: LGPLv3+

%description -n libini_config-devel
Library to process config files in INI format into a libcollection data
structure

%package -n libref_array
Summary: A refcounted array for C
Group: Development/Libraries
Version: %{refarray_version}
License: LGPLv3+

%description -n libref_array
A dynamically-growing, reference-counted array

%package -n libref_array-devel
Summary: Development files for libref_array
Group: Development/Libraries
Version: %{refarray_version}
Requires: libref_array = %{refarray_version}-%{release}
License: LGPLv3+

%description -n libref_array-devel
A dynamically-growing, reference-counted array

%prep
%setup -q
#patch0 -p 1
#autoreconf

%build
%configure2_5x \
    --with-db-path=%{dbpath} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-init-dir=%{_initrddir} \
    --enable-nsslibdir=/%{_lib} \
    --disable-static \
    --disable-rpath

%make

pushd common
%make docs
popd

%check
%__make check

%install
rm -rf %{buildroot}

%makeinstall_std

# Remove the example files from the output directory
# We will copy them directly from the source directory
# for packaging
rm -f \
    %{buildroot}/usr/share/doc/dhash/README \
    %{buildroot}/usr/share/doc/dhash/examples/dhash_example.c \
    %{buildroot}/usr/share/doc/dhash/examples/dhash_test.c

# Prepare language files
%find_lang sss_daemon

# Copy default sssd.conf file
mkdir -p %{buildroot}/%{_sysconfdir}/sssd
install -m600 src/examples/sssd.conf %{buildroot}%{_sysconfdir}/sssd/sssd.conf
install -m400 src/config/etc/sssd.api.conf %{buildroot}%{_sysconfdir}/sssd/sssd.api.conf
install -m400 src/config/etc/sssd.api.d/* %{buildroot}%{_sysconfdir}/sssd/sssd.api.d/

# Copy default logrotate file
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p %{buildroot}/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab %{buildroot}%{_sysconfdir}/rwtab.d/sssd

# Remove .la files created by libtool
rm -f \
    %{buildroot}/%{_lib}/libnss_sss.la \
    %{buildroot}/%{_lib}/security/pam_sss.la \
    %{buildroot}/%{_libdir}/libdhash.la \
    %{buildroot}/%{_libdir}/libpath_utils.la \
    %{buildroot}/%{_libdir}/libcollection.la \
    %{buildroot}/%{_libdir}/libini_config.la \
    %{buildroot}/%{_libdir}/libref_array.la \
    %{buildroot}/%{_libdir}/ldb/memberof.la \
    %{buildroot}/%{_libdir}/sssd/libsss_ldap.la \
    %{buildroot}/%{_libdir}/sssd/libsss_proxy.la \
    %{buildroot}/%{_libdir}/sssd/libsss_krb5.la \
    %{buildroot}/%{_libdir}/sssd/libsss_ipa.la \
    %{buildroot}/%{_libdir}/sssd/libsss_simple.la \
    %{buildroot}/%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.la \
    %{buildroot}/%{python_sitearch}/pysss.la

%clean
rm -rf %{buildroot}

%post
%post_service %{servicename}

%preun
%preun_service %{servicename}

%files -f sss_daemon.lang
%defattr(-,root,root,-)
%doc COPYING
%{_initrddir}/%{name}
%{_sbindir}/sssd
%{_sbindir}/sss_useradd
%{_sbindir}/sss_userdel
%{_sbindir}/sss_usermod
%{_sbindir}/sss_groupadd
%{_sbindir}/sss_groupdel
%{_sbindir}/sss_groupmod
%{_sbindir}/sss_groupshow
%{_libexecdir}/%{servicename}/
%{_libdir}/%{name}
%{_libdir}/ldb/memberof.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%dir %{sssdstatedir}
%attr(700,root,root) %dir %{dbpath}
%attr(755,root,root) %dir %{pipepath}
%attr(755,root,root) %dir %{pubconfpath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%config %{_sysconfdir}/sssd/sssd.api.conf
%attr(700,root,root) %dir %{_sysconfdir}/sssd/sssd.api.d
%config %{_sysconfdir}/sssd/sssd.api.d/
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-ipa.5*
%{_mandir}/man5/sssd-krb5.5*
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man8/sssd.8*
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*
%{python_sitearch}/pysss.so
%{python_sitelib}/*.py*
%{python_sitelib}/SSSDConfig-1-py2.6.egg-info

%files client
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
/%{_lib}/libnss_sss.so.2
/%{_lib}/security/pam_sss.so
%{_mandir}/man8/pam_sss.8*

%files -n libdhash
%defattr(-,root,root,-)
%doc common/dhash/COPYING
%doc common/dhash/COPYING.LESSER
%{_libdir}/libdhash.so.1
%{_libdir}/libdhash.so.1.0.0

%files -n libdhash-devel
%defattr(-,root,root,-)
%{_includedir}/dhash.h
%{_libdir}/libdhash.so
%{_libdir}/pkgconfig/dhash.pc
%doc common/dhash/README
%doc common/dhash/examples

%files -n libpath_utils
%defattr(-,root,root,-)
%doc common/path_utils/COPYING
%doc common/path_utils/COPYING.LESSER
%{_libdir}/libpath_utils.so.1
%{_libdir}/libpath_utils.so.1.0.0

%files -n libpath_utils-devel
%defattr(-,root,root,-)
%{_includedir}/path_utils.h
%{_libdir}/libpath_utils.so
%{_libdir}/pkgconfig/path_utils.pc
%doc common/path_utils/README
%doc common/path_utils/doc/html/

%files -n libcollection
%defattr(-,root,root,-)
%doc common/collection/COPYING
%doc common/collection/COPYING.LESSER
%{_libdir}/libcollection.so.1
%{_libdir}/libcollection.so.1.0.0

%files -n libcollection-devel
%defattr(-,root,root,-)
%{_includedir}/collection.h
%{_includedir}/collection_tools.h
%{_includedir}/collection_queue.h
%{_includedir}/collection_stack.h
%{_libdir}/libcollection.so
%{_libdir}/pkgconfig/collection.pc
%doc common/collection/doc/html/

%files -n libini_config
%defattr(-,root,root,-)
%doc common/ini/COPYING
%doc common/ini/COPYING.LESSER
%{_libdir}/libini_config.so.1
%{_libdir}/libini_config.so.1.0.0

%files -n libini_config-devel
%defattr(-,root,root,-)
%{_includedir}/ini_config.h
%{_libdir}/libini_config.so
%{_libdir}/pkgconfig/ini_config.pc
%doc common/ini/doc/html/

%files -n libref_array
%defattr(-,root,root,-)
%doc common/refarray/COPYING
%doc common/refarray/COPYING.LESSER
%{_libdir}/libref_array.so.1
%{_libdir}/libref_array.so.1.0.0

%files -n libref_array-devel
%defattr(-,root,root,-)
%{_includedir}/ref_array.h
%{_libdir}/libref_array.so
%{_libdir}/pkgconfig/ref_array.pc
%doc common/refarray/README
%doc common/refarray/doc/html/

