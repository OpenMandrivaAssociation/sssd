%define servicename sssd
%define sssdstatedir %{_localstatedir}/lib/sss
%define dbpath %{sssdstatedir}/db
%define pipepath %{sssdstatedir}/pipes
%define pubconfpath %{sssdstatedir}/pubconf

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

Name:       sssd
Version:    1.4.0
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
BuildRequires: libnl-devel
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
BuildRequires: docbook-dtd44-xml
BuildRequires: krb5-devel
BuildRequires: c-ares-devel
BuildRequires: python-devel
BuildRequires: check-devel
BuildRequires: doxygen
BuildRequires: keyutils-devel
BuildRequires: bind-utils
BuildRequires: dhash-devel
BuildRequires: collection-devel
BuildRequires: ini_config-devel
BuildRequires: path_utils-devel

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
    --enable-pammoddir=/%{_lib}/security \
    --disable-static \
    --disable-rpath
%make

%check
%__make check

%install
rm -rf %{buildroot}

%makeinstall_std

# Prepare language files
%find_lang sssd

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
    %{buildroot}/%{_libdir}/ldb/memberof.la \
    %{buildroot}/%{_libdir}/sssd/libsss_ldap.la \
    %{buildroot}/%{_libdir}/sssd/libsss_proxy.la \
    %{buildroot}/%{_libdir}/sssd/libsss_krb5.la \
    %{buildroot}/%{_libdir}/sssd/libsss_ipa.la \
    %{buildroot}/%{_libdir}/sssd/libsss_simple.la \
    %{buildroot}/%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.la \
    %{buildroot}/%{python_sitearch}/pysss.la \
    %{buildroot}/%{_libdir}/libref_array.la \

%clean
rm -rf %{buildroot}

%post
%post_service %{servicename}

%preun
%preun_service %{servicename}

%files -f sssd.lang
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
%{_sbindir}/sss_obfuscate
%{_libexecdir}/%{servicename}/
%dir %{_libdir}/%{name}
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
%{_mandir}/man8/sss_obfuscate.8*
%{python_sitearch}/pysss.so
%{python_sitelib}/*.py*
%{python_sitelib}/SSSDConfig-1-py2.6.egg-info

%files client
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
/%{_lib}/libnss_sss.so.2
/%{_lib}/security/pam_sss.so
%{_mandir}/man8/pam_sss.8*
