# Update this if build fails with "LDB module path is incorrect".
%define ldb_modulesdir %{_libdir}/ldb

%define __noautoprov 'py(sss|hbac).*\\.so'

%define sssdstatedir %{_localstatedir}/lib/sss
%define dbpath %{sssdstatedir}/db
%define pipepath %{sssdstatedir}/pipes
%define pubconfpath %{sssdstatedir}/pubconf
%define cachepath %{sssdstatedir}/mc

%define major 0
%define libname %mklibname sssd %{major}
%define devname %mklibname %{name} -d
%define libsimpleifp %mklibname sss_simpleifp %{major}
%define libidmap %mklibname sss_idmap %{major}
%define libipahbac %mklibname sss_ipa_hbac %{major}
%define libwbclient %mklibname sss_wbclient %{major}
%define libidmapnss %mklibname sss_idmap_nss %{major}

%define libnssmajor 2
%define libnsssss %mklibname nss_sss %{libnssmajor}

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

Summary:	System Security Services Daemon
Name:		sssd
Version:	1.12.4
Release:	1
License:	GPLv3+
Group:		System/Libraries
Url:		http://fedorahosted.org/sssd/
Source0:	https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
Source10:	sssd.service
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
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(tevent)
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	ini_config-devel
BuildRequires:	nfsidmap-devel
BuildRequires:	augeas-devel
BuildRequires:	pkgconfig(ndr)
BuildRequires:	cifs-utils-devel
BuildRequires:	samba-util-devel
BuildRequires:	samba-devel
BuildRequires:	samba-common
BuildRequires:	pkgconfig(libsystemd)
Requires:	sssd-client = %{EVRD}
Requires:	sasl-plug-gssapi
Requires(pre):	rpm-helper

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

%files -f sssd.lang
%doc COPYING
%doc src/examples/sssd-example.conf
%{_presetdir}/86-sssd.preset
%{_systemunitdir}/sssd.service
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/systemd/sssd.service.d/journal.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datarootdir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service
%{_sbindir}/sssd
%{_libexecdir}/%{name}/krb5_child
%{_libexecdir}/%{name}/ldap_child
%{_libexecdir}/%{name}/proxy_child
%{_libexecdir}/%{name}/selinux_child
%{_libexecdir}/%{name}/gpo_child
%{_libexecdir}/%{name}/sssd_be
%{_libexecdir}/%{name}/sssd_nss
%{_libexecdir}/%{name}/sssd_pam
%{_libexecdir}/%{name}/sssd_autofs
%{_libexecdir}/%{name}/sssd_ssh
%{_libexecdir}/%{name}/sssd_sudo
%{_libexecdir}/%{name}/sssd_ifp
%{_libexecdir}/%{name}/sssd_pac
%{_libexecdir}/%{name}/sss_signal
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,root,root) %dir %{dbpath}
%attr(755,root,root) %dir %{pipepath}
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{pubconfpath}/krb5.include.d
%attr(755,root,root) %dir %{cachepath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d
%{_mandir}/man1/sss_ssh_authorizedkeys.1.xz
%{_mandir}/man1/sss_ssh_knownhostsproxy.1.xz
%{_mandir}/man5/sssd.conf.5.xz
%{_mandir}/man8/sssd.8.xz
%{_mandir}/man5/sssd-ipa.5.xz
%{_mandir}/man5/sssd-krb5.5.xz
%{_mandir}/man5/sssd-ldap.5.xz
%{_mandir}/man5/sssd-simple.5.xz
%{_mandir}/man5/sssd-sudo.5.xz
%{_mandir}/man5/sssd-ad.5.xz
%{_mandir}/man5/sssd-ifp.5.xz

%post
# Touch files to avoid misleading warnings in journald logs:
# '... sssd_*[PID]: chown failed for [sssd_*]: [2]'
# Messages appear on first start of sssd as daemon can't chown
# log files which do not exist yet.
if [ $1 -eq 1 ] ; then
# Initial installation
    for i in `ls -1 %{_libexecdir}/%{name}/sssd_*`
    do
	touch %{_logdir}/%{name}/`basename $i`.log
    done
fi

#----------------------------------------------------------------------------

%package client
Summary:	SSSD Client libraries for NSS and PAM
Group:		System/Base
Requires:	nss_sss = %{EVRD}

%description client
Provides the plugins needed by the PAM and NSS stacks to connect to the SSSD
service.

%files client -f sssd-client.lang
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/%{name}/modules/sssd_krb5_localauth_plugin.so
%{_libdir}/%{name}/modules/libsss_autofs.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_libdir}/krb5/plugins/authdata/sssd_pac_plugin.so
%{_libdir}/cifs-utils/cifs_idmap_sss.so
%{_libdir}/libnfsidmap/sss.so
/%{_lib}/security/pam_sss.so
%{ldb_modulesdir}/memberof.so
%{_mandir}/man8/pam_sss.8.xz
%{_mandir}/man8/sssd_krb5_locator_plugin.8.xz

# This package may require post and postun jobs to register/activate plugins.
# If we ever come up with default configuration of course. To be considered.

#----------------------------------------------------------------------------

%package tools
Summary:	Userspace tools for use with the SSSD
License:	GPLv3+
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires(pre):	rpm-helper

%description tools
Provides userspace tools for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other administrative tools:
    * sss_debuglevel to change the debug level on the fly
    * sss_seed which pre-creates a user entry for use in kickstarts
    * sss_obfuscate for generating an obfuscated LDAP password

%files tools -f sssd-tools.lang
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
%{_mandir}/man8/sss_groupadd.8.xz
%{_mandir}/man8/sss_groupdel.8.xz
%{_mandir}/man8/sss_groupmod.8.xz
%{_mandir}/man8/sss_groupshow.8.xz
%{_mandir}/man8/sss_useradd.8.xz
%{_mandir}/man8/sss_userdel.8.xz
%{_mandir}/man8/sss_usermod.8.xz
%{_mandir}/man8/sss_obfuscate.8.xz
%{_mandir}/man8/sss_cache.8.xz
%{_mandir}/man8/sss_debuglevel.8.xz
%{_mandir}/man8/sss_seed.8.xz

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	SSSD Python modules
Group:		Development/Python

%description -n python-%{name}
System Security Services daemon (SSSD) Python modules.

%files -n python-%{name}
%doc COPYING
%dir %{python_sitelib}/SSSDConfig/*.py*
%{python_sitelib}/SSSDConfig-1.12.4-py2.7.egg-info
%{python_sitearch}/pysss_nss_idmap.so
%{python_sitearch}/pysss_murmur.so
%{python_sitearch}/pyhbac.so
%{python_sitearch}/pysss.so

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	SSSD development package
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
System Security Services daemon (SSSD) development files.

%files -n %{devname}
%doc COPYING
%{_includedir}/sss_sifp_dbus.h
%{_includedir}/sss_sifp.h
%{_includedir}/wbclient_sssd.h
%{_includedir}/sss_nss_idmap.h
%{_includedir}/sss_idmap.h
%{_includedir}/ipa_hbac.h
%{_libdir}/sssd/modules/libwbclient.so
%{_libdir}/libsss_simpleifp.so
%{_libdir}/libsss_nss_idmap.so
%{_libdir}/libsss_idmap.so
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/sss_simpleifp.pc
%{_libdir}/pkgconfig/wbclient_sssd.pc
%{_libdir}/pkgconfig/sss_nss_idmap.pc
%{_libdir}/pkgconfig/sss_idmap.pc
%{_libdir}/pkgconfig/ipa_hbac.pc
%{_mandir}/man5/sss_rpcidmapd.5.xz

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	SSSD daemon libraries
Group:		System/Libraries

%description -n %{libname}
Provides SSSD daemon set private libraries.

%files -n %{libname}
%doc COPYING
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libsss_ad.so
%{_libdir}/%{name}/libsss_ad_common.so
%{_libdir}/%{name}/libsss_child.so
%{_libdir}/%{name}/libsss_config.so
%{_libdir}/%{name}/libsss_crypt.so
%{_libdir}/%{name}/libsss_debug.so
%{_libdir}/%{name}/libsss_ipa.so
%{_libdir}/%{name}/libsss_krb5.so
%{_libdir}/%{name}/libsss_krb5_common.so
%{_libdir}/%{name}/libsss_ldap.so
%{_libdir}/%{name}/libsss_ldap_common.so
%{_libdir}/%{name}/libsss_proxy.so
%{_libdir}/%{name}/libsss_semanage.so
%{_libdir}/%{name}/libsss_simple.so
%{_libdir}/%{name}/libsss_util.so
%{_libdir}/%{name}/libsss_sudo.so
%{_libdir}/libsss_sudo.so

#----------------------------------------------------------------------------

%package -n %{libnsssss}
Summary:	SSSD plugin for NSS
Group:		System/Libraries
Provides:	nss_sss = %{EVRD}

%description -n %{libnsssss}
SSSD plugin for the Name Service Switch.

%files -n %{libnsssss}
%doc COPYING
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
/%{_lib}/libnss_sss.so.%{libnssmajor}

#----------------------------------------------------------------------------

%package -n %{libidmapnss}
Summary:	NSS Responder ID-mapping interface
Group:		System/Libraries

%description -n %{libidmapnss}
NSS Responder ID-mapping interface for SSSD NSS plugin.

%files -n %{libidmapnss}
%doc COPYING
%{_libdir}/libsss_nss_idmap.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libsimpleifp}
Summary:	SSSD InfoPipe responder library
Group:		System/Libraries

%description -n %{libsimpleifp}
A library that simplifies work with the InfoPipe responder.

%files -n %{libsimpleifp}
%doc COPYING
%{_libdir}/libsss_simpleifp.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libidmap}
Summary:	A library to allow communication between idmap and SSSD
Group:		System/Libraries

%description -n %{libidmap}
A utility library to allow communication between Autofs and SSSD.

%files -n %{libidmap}
%doc COPYING
%{_libdir}/libsss_idmap.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libipahbac}
Summary:	FreeIPA HBAC Evaluator library
Group:		System/Libraries

%description -n %{libipahbac}
Provides the FreeIPA HBAC Evaluator library for SSSD.

%files -n %{libipahbac}
%doc COPYING
%{_libdir}/libipa_hbac.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libwbclient}
Summary:	SSSD implementation of wbclient API
Group:		System/Libraries

%description -n %{libwbclient}
SSSD implementation of Samba wbclient API.

%files -n %{libwbclient}
%doc COPYING
%{_libdir}/%{name}/modules/libwbclient.so.%{major}*

# This plugin might require post and postun jobs to register/activate

#----------------------------------------------------------------------------

%prep
# Can't use %%{pkg-config..} macro directly. It fails as it is being called
# before Buildrequire'd package "ldb-devel" has a chance to get installed.
if [ "%{ldb_modulesdir}" == `pkg-config --variable=modulesdir ldb` ];
  then
	echo "LDB module path %{ldb_modulesdir} seems to be correct"
  else
	echo "LDB module path is incorrect. Please check and/or update spec file."
	exit 1
fi
%setup -q

%build
%configure \
    --with-db-path=%{dbpath} \
    --with-systemdconfdir=%{_systemdconfdir} \
    --with-systemdunitdir=%{_systemunitdir} \
    --with-initscript=systemd \
    --with-syslog=journald \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-init-dir=%{_initrddir} \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --enable-nsslibdir=/%{_lib} \
    --with-python-bindings \
    --with-sudo \
    --with-sudo-lib-path=%{_libdir}/%{name} \
    --enable-pammoddir=/%{_lib}/security \
    --disable-static \
    --disable-rpath \
    --with-test-dir=/dev/shm \
    --enable-all-experimental-features \
    --enable-ldb-version-check \
    --enable-sss-default-nss-plugin 

%make

%install

%makeinstall_std

# Prepare language files
%find_lang sssd

# Prepare config dir
mkdir -p %{buildroot}/%{_sysconfdir}/sssd

# Copy default logrotate file
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p %{buildroot}/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab %{buildroot}%{_sysconfdir}/rwtab.d/sssd

# Replace sysv init script with systemd unit file
rm -f %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/%{_systemunitdir}/
install -m644 %{SOURCE10} %{buildroot}/%{_systemunitdir}/

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-sssd.preset << EOF
enable sssd.service
EOF

# Suppress developer-only documentation
rm -Rf %{buildroot}%{_docdir}/%{name}/doc

# Find sssd native language man files
for man in `find %{buildroot}/%{_mandir}/??/man?/ -type f -name 'sss_ssh_*' -or -name 'sssd*' -and -not -name 'sssd_krb5_locator_plugin.*' | sed -e "s#%{buildroot}/%{_mandir}/##"`
do
	lang=`echo $man | cut -c 1-2` ; echo \%lang\(${lang}\) \%{_mandir}/${man}.xz >> sssd.lang
done

# Find sssd-tools native language man files
for man in `find %{buildroot}/%{_mandir}/??/man?/ -type f -name 'sss_*' -and -not -name 'sss_ssh_*' | sed -e "s#%{buildroot}/%{_mandir}/##"`
do
	lang=`echo $man | cut -c 1-2` ; echo \%lang\(${lang}\) \%{_mandir}/${man}.xz >> sssd-tools.lang
done

# Find sssd-client native language man files
for man in `find %{buildroot}/%{_mandir}/??/man?/ -type f -name 'pam_sss.*' -or -name 'sssd_krb5_locator_plugin.*' | sed -e "s#%{buildroot}/%{_mandir}/##"`
do
	lang=`echo $man | cut -c 1-2` ; echo \%lang\(${lang}\) \%{_mandir}/${man}.xz >> sssd-client.lang
done

# Fix E: non-standard-dir-perm (Badness: 1) /usr/src/debug/sssd-1.12.4 0775
find . -type d -perm 0775 -exec chmod 0755 {} \;

# http://bugs.rosalinux.ru/show_bug.cgi?id=6280
pushd %{buildroot}%{_libdir}
ln -s %{name}/libsss_sudo.so libsss_sudo.so
popd
