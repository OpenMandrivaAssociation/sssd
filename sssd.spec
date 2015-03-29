%global ldb_modulesdir %(pkg-config --variable=modulesdir ldb)
%global ldb_version 1.1.4

%define servicename sssd
%define sssdstatedir %{_localstatedir}/lib/sss
%define dbpath %{sssdstatedir}/db
%define pipepath %{sssdstatedir}/pipes
%define pubconfpath %{sssdstatedir}/pubconf

%define major 0
%define libhbac %mklibname ipa_hbac %{major}
%define libsudo %mklibname sss_sudo %{major}
%define libautofs %mklibname sss_autofs %{major}

%define libsudodevel %mklibname -d sss_sudo %{major}
%define libautofsdevel %mklibname -d sss_autofs %{major}
%define libhbacdevel %mklibname -d ipa_hbac %{major}

%define libidmap %mklibname sss_idmap %{major}
%define libidmapdevel %mklibname -d sss_idmap %{major}

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

Summary:	System Security Services Daemon
Name:		sssd
Version:	1.9.6
Release:	1
License:	GPLv3+
Group:		System/Libraries
Url:		http://fedorahosted.org/sssd/
Source0:	https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
BuildRequires:	bind-utils
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	xsltproc
BuildRequires:	keyutils-devel
BuildRequires:	libunistring-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	semanage-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(collection)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dhash)
BuildRequires:	pkgconfig(gio-2.0)
# before update to 1.12.4 be sure that ini_config-devel is >= 1.1.1. Sflo
BuildRequires:	pkgconfig(ini_config)
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(ldb)
BuildRequires:	pkgconfig(libcares)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(path_utils)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(tevent)


Requires:	sssd-client2 = %{EVRD}
Requires:	sasl-plug-gssapi
Obsoletes:	sssd-client

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

%files -f sssd.lang
%doc COPYING
%doc src/examples/sssd-example.conf
%{_unitdir}/sssd.service
%{_sbindir}/sssd
%{_libexecdir}/%{servicename}/krb5_child
%{_libexecdir}/%{servicename}/ldap_child
%{_libexecdir}/%{servicename}/proxy_child
%{_libexecdir}/%{servicename}/sssd_be
%{_libexecdir}/%{servicename}/sssd_nss
%{_libexecdir}/%{servicename}/sssd_pam
%{_libexecdir}/%{servicename}/sssd_autofs
%{_libexecdir}/%{servicename}/sssd_ssh
%{_libexecdir}/%{servicename}/sssd_sudo
%{_libdir}/%{name}/libsss_ipa.so
%{_libdir}/%{name}/libsss_krb5.so
%{_libdir}/%{name}/libsss_ldap.so
%{_libdir}/%{name}/libsss_proxy.so
%{_libdir}/%{name}/libsss_simple.so
%{_libdir}/%{name}/libsss_ad.so
%{ldb_modulesdir}/memberof.so
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,root,root) %dir %{dbpath}
%attr(755,root,root) %dir %{pipepath}
%attr(755,root,root) %dir %{pubconfpath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%ghost %attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-ipa.5*
%{_mandir}/man5/sssd-krb5.5*
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man5/sssd-ad.5*
%{_mandir}/man8/sssd.8*
%{python2_sitearch}/pysss.so
%{python2_sitearch}/pysss_murmur.so
%dir %{python2_sitelib}/SSSDConfig/*.py*

%post
%_post_service %{servicename}

%preun
%_preun_service %{servicename}

#----------------------------------------------------------------------------

%package client2
Summary:	SSSD Client libraries for NSS and PAM
License:	LGPLv3+
Group:		System/Libraries

%description client2
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%files client2 -f sssd_client.lang
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
/%{_lib}/libnss_sss.so.2
/%{_lib}/security/pam_sss.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

#----------------------------------------------------------------------------

%package tools
Summary:	Userspace tools for use with the SSSD
License:	GPLv3+
Group:		System/Base
Requires:	%{name} = %{EVRD}

%description tools
Provides userspace tools for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides a userspace tool for generating an obfuscated LDAP password for
use with ldap_default_authtok_type = obfuscated_password.

%files tools -f sssd_tools.lang
%doc COPYING
%{_sbindir}/sss_useradd
%{_sbindir}/sss_seed
%{_sbindir}/sss_userdel
%{_sbindir}/sss_usermod
%{_sbindir}/sss_groupadd
%{_sbindir}/sss_groupdel
%{_sbindir}/sss_groupmod
%{_sbindir}/sss_groupshow
%{_sbindir}/sss_obfuscate
%{_sbindir}/sss_cache
%{_sbindir}/sss_debuglevel
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_cache.8*
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_seed.8*

#----------------------------------------------------------------------------

%package -n %{libhbac}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libhbac}
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%files -n %{libhbac}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_libdir}/libipa_hbac.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libautofs}
Summary:	A library to allow communication between Autofs and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libautofs}
A utility library to allow communication between Autofs and SSSD

%files -n %{libautofs}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_libdir}/sssd/modules/libsss_autofs.so*

#----------------------------------------------------------------------------

%package -n %{libidmap}
Summary:	A library to allow communication between idmap and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libautofs}
A utility library to allow communication between Autofs and SSSD

%files -n %{libidmap}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_libdir}/libsss_idmap.so.*

#----------------------------------------------------------------------------

%package -n %{libsudo}
Summary:	A library to allow communication between SUDO and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libsudo}
A utility library to allow communication between SUDO and SSSD

%files -n %{libsudo}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_libdir}/libsss_sudo.so

#----------------------------------------------------------------------------

%package -n %{libhbacdevel}
Summary:	FreeIPA HBAC Evaluator library
License:	LGPLv3+
Group:		Development/C

%description -n %{libhbacdevel}
Utility library to validate FreeIPA HBAC rules for authorization requests

%files -n %{libhbacdevel}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/ipa_hbac.pc

#----------------------------------------------------------------------------

%package -n %{libautofsdevel}
Summary:	A library to allow communication between Autofs and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libautofsdevel}
A utility library to allow communication between Autofs and SSSD

#----------------------------------------------------------------------------

%package -n %{libsudodevel}
Summary:	A library to allow communication between SUDO and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libsudodevel}
A utility library to allow communication between SUDO and SSSD

%files -n %{libsudodevel}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_includedir}/sss_idmap.h
%{_libdir}/libsss_idmap.so

#----------------------------------------------------------------------------

%package -n %{libidmapdevel}
Summary:	A library to allow communication between idmap and SSSD
License:	LGPLv3+
Group:		Development/C

%description -n %{libidmapdevel}
A utility library to allow communication between Autofs and SSSD

%files -n %{libidmapdevel}
%doc COPYING
%doc src/examples/sssd-example.conf
%{_includedir}/sss_sudo.h
%{_libdir}/pkgconfig/sss_idmap.pc
# %{_libdir}/libsss_sudo.so
# %{_libdir}/pkgconfig/libsss_sudo.pc

#----------------------------------------------------------------------------

%package -n libhbac-python
Summary:	Python bindings for the FreeIPA HBAC Evaluator library
License:	LGPLv3+
Group:		Development/C
Requires:	%{libhbac} = %{EVRD}

%description -n libhbac-python
The libipa_hbac-python contains the bindings so that libipa_hbac can be
used by Python applications.

%files -n libhbac-python
%doc COPYING
%doc src/examples/sssd-example.conf
%{python2_sitearch}/pyhbac.so

#----------------------------------------------------------------------------

%prep
%setup -q

%build
export PYTHON=/usr/bin/python2
%configure \
    --with-db-path=%{dbpath} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-init-dir=%{_initrddir} \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --enable-nsslibdir=/%{_lib} \
    --with-python-bindings \
    --with-sudo \
    --enable-pammoddir=/%{_lib}/security \
    --disable-static \
    --disable-rpath \
    --with-test-dir=/dev/shm \
    --enable-all-experimental-features


%make

%install

%makeinstall_std

# Prepare language files
/usr/lib/rpm/find-lang.sh %{buildroot} sssd

# Prepare empty config file
mkdir -p %{buildroot}/%{_sysconfdir}/sssd
touch %{buildroot}/%{_sysconfdir}/sssd/sssd.conf

# Copy default logrotate file
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p %{buildroot}/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab %{buildroot}%{_sysconfdir}/rwtab.d/sssd

# Replace sysv init script with systemd unit file
rm -f %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/%{_unitdir}/
cp src/sysv/systemd/sssd.service %{buildroot}/%{_unitdir}/

# Remove .la files created by libtool
find %{buildroot} -name "*.la" -exec rm -f {} \;

# Suppress developer-only documentation
rm -Rf %{buildroot}%{_docdir}/%{name}/doc

# Older versions of rpmbuild can only handle one -f option
# So we need to append to the sssd.lang file
for file in `ls %{buildroot}/%{python2_sitelib}/*.egg-info 2> /dev/null`
do
    echo %{python2_sitelib}/`basename $file` >> sssd.lang
done

touch sssd_tools.lang
for man in `find %{buildroot}/%{_mandir}/??/man?/ -type f | sed -e "s#%{buildroot}/%{_mandir}/##"`
do
    lang=`echo $man | cut -c 1-2`
    case `basename $man` in
        sss_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        pam_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        sssd_krb5_locator_plugin*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        *)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
    esac
done

# Print these to the rpmbuild log
echo "sssd.lang:"
cat sssd.lang

echo "sssd_client.lang:"
cat sssd_client.lang

echo "sssd_tools.lang:"
cat sssd_tools.lang
