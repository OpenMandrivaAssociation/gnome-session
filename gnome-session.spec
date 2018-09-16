%define _disable_rebuild_configure 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	The gnome desktop programs for the GNOME GUI desktop environment
Name:		gnome-session
Version:	3.28.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/softwaremap/projects/gnome-session/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gnome-session/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source3:	gnome-session-startgnomeclassic

BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool >= 0.40.0
BuildRequires:	xmlto
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.76
BuildRequires:	pkgconfig(gio-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.90.7
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0) >= 0.10
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.0
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtrans)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	xmlto
BuildRequires:	meson
BuildRequires:  pkgconfig(glesv2)
#BuildRequires:  glesv3-devel

Requires:	desktop-common-data
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
Requires:	%{name}-bin >= %{version}-%{release}

Suggests:   x11-server-xwayland

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
%setup -q
%apply_patches

%build
%meson                     \
    -Dsystemd=true         \
    -Dsystemd_journal=true
%meson_build

%install
%meson_install

# wmsession session file
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/02GNOME
NAME=GNOME
ICON=gnome-logo-icon-transparent.png
DESC=GNOME Environment
EXEC=%{_bindir}/startgnome
SCRIPT:
exec %{_bindir}/startgnome
EOF

install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/startgnome
install -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/startgnomeclassic

mkdir -p %{buildroot}%{_sysconfdir}/gnome
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/gnome/gnomerc
# gw these produce rpmlint errors:
rm -rf %{buildroot}%{_datadir}/locale/{be@latin}
%find_lang %{name}-3.0

# remove unpackaged files
rm -rf %{buildroot}%{_datadir}/xsessions

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi
%{make_session}

#%postun
#%{make_session}

%files bin
%{_bindir}/gnome-session
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%{_datadir}/%{name}
#{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/gnome-session.*

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%doc %{_docdir}/%{name}
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_sysconfdir}/gnome/gnomerc
%{_bindir}/startgnome
%{_bindir}/startgnomeclassic
%{_bindir}/%{name}-custom-session
%{_bindir}/gnome-session-quit
%{_bindir}/gnome-session-inhibit
%{_libexecdir}/gnome-session-binary
%{_libexecdir}/gnome-session-failed
%{_libexecdir}/gnome-session-check-accelerated*
#{_libexecdir}/gnome-session-check-accelerated-helper
%{_datadir}/wayland-sessions
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_mandir}/man1/gnome-session-quit.*
%{_mandir}/man1/gnome-session-inhibit.*

%exclude /usr/lib/debug/usr/libexec/gnome-session-check-accelerated-gl-helper-3.28.1-1.x86_64.debug
%exclude /usr/lib/debug/usr/libexec/gnome-session-check-accelerated-gles-helper-3.28.1-1.x86_64.debug
