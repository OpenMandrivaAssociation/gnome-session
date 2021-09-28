%define po_package gnome-session-40

%define _disable_rebuild_configure 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	The gnome desktop programs for the GNOME GUI desktop environment
Name:		gnome-session
Version:	40.1.1
Release:	2
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/softwaremap/projects/gnome-session/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gnome-session/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source3:	gnome-session-startgnomeclassic
# https://bugzilla.gnome.org/show_bug.cgi?id=772421
Patch4: 0001-check-accelerated-gles-Use-eglGetPlatformDisplay-EXT.patch

BuildRequires:  gettext
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool >= 0.40.0
BuildRequires:	xmlto
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.76
BuildRequires:	pkgconfig(gio-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(egl)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.90.7
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0) >= 0.10
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.0
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtrans)
BuildRequires:	pkgconfig(xtst)
BuildRequires:  pkgconfig(x11)
BuildRequires:	xmlto
BuildRequires:	meson
BuildRequires:  pkgconfig(glesv2)
#BuildRequires:  glesv3-devel

Requires:	desktop-common-data
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
Requires:	%{name}-bin >= %{version}-%{release}
Requires:	gsettings-desktop-schemas
Requires:	dconf
Requires:   x11-server-xwayland

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.

The GNOME Session Manager restores a set session (group of applications)
when you log into GNOME.

%package bin
Group:		%{group}
Summary:	%{summary}
Conflicts:	gnome-session < 2.30.2-2mdv

%description bin
This package contains the binaries for the GNOME Session Manager, but
no startup scripts. It is meant for applications such as GDM that use
gnome-session internally.

%prep
%setup -q -n %{name}-%{version}
%autopatch -p1

%build
%meson                     \
    -Dsystemd=true         \
    -Dsystemd_journal=true
%meson_build

%install
%meson_install


install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/startgnome

mkdir -p %{buildroot}%{_sysconfdir}/gnome
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/gnome/gnomerc
# gw these produce rpmlint errors:
rm -rf %buildroot%_datadir/locale/{be@latin}

%find_lang %{po_package}


%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi

%posttrans
if [ "$1" -eq 1 ]; then
        if [ -e %{_datadir}/xsessions/02GNOME.desktop ]; then
                rm -rf %{_datadir}/xsessions/02GNOME.desktop
        fi
        if [ -e %{_sysconfdir}/X11/dm/Sessions/02GNOME.desktop ]; then
                rm -rf  %{_sysconfdir}/X11/dm/Sessions/02GNOME.desktop
        fi
fi

%files bin
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%{_bindir}/%{name}
%{_mandir}/*/%{name}.*
%{_datadir}/%{name}

%files -f %{name}-40.lang
%{_datadir}/xsessions/*
%{_sysconfdir}/gnome/gnomerc
%{_bindir}/%{name}-inhibit
%{_bindir}/startgnome
%{_bindir}/%{name}-quit
%{_bindir}/%{name}-custom-session
%{_libexecdir}/%{name}-*
%{_datadir}/GConf/gsettings/%{name}.convert
%{_datadir}/wayland-sessions
%{_mandir}/*/%{name}-*
%doc %{_docdir}/%{name}

%{_userunitdir}/gnome-session-failed.service
%{_userunitdir}/gnome-session-failed.target
%{_userunitdir}/gnome-session-initialized.target
%{_userunitdir}/gnome-session-manager.target
%{_userunitdir}/gnome-session-manager@.service
%{_userunitdir}/gnome-session-monitor.service
%{_userunitdir}/gnome-session-pre.target
%{_userunitdir}/gnome-session-restart-dbus.service
%{_userunitdir}/gnome-session-shutdown.target
%{_userunitdir}/gnome-session-signal-init.service
%{_userunitdir}/gnome-session-wayland.target
%{_userunitdir}/gnome-session-wayland@.target
%{_userunitdir}/gnome-session-x11-services.target
%{_userunitdir}/gnome-session-x11.target
%{_userunitdir}/gnome-session-x11@.target
%{_userunitdir}/gnome-session.target
%{_userunitdir}/gnome-session@.target
%{_userunitdir}/gnome-launched-.scope.d/override.conf
%{_userunitdir}/gnome-session-x11-services-ready.target
%{_userunitdir}/gnome-session@gnome.target.d/gnome.session.conf
