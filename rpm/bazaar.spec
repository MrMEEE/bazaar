Name:           bazaar
Version:        0.9.5
Release:        1%{?dist}
Summary:        Flatpak application store
License:        GPL-3.0-or-later
URL:            https://github.com/kolunmi/bazaar
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  vala
BuildRequires:  blueprint-compiler >= 0.20
BuildRequires:  pkgconfig(gtk4) >= 4.22.1
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(libdex-1)
BuildRequires:  pkgconfig(flatpak) >= 1.9
BuildRequires:  pkgconfig(appstream) >= 1.0
BuildRequires:  pkgconfig(xmlb) >= 0.3.4
BuildRequires:  pkgconfig(glycin-2) >= 2.0
BuildRequires:  pkgconfig(glycin-gtk4-2) >= 2.0
BuildRequires:  pkgconfig(yaml-0.1) >= 0.2.5
BuildRequires:  pkgconfig(libsoup-3.0) >= 3.6.0
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.10.0
BuildRequires:  pkgconfig(md4c) >= 0.5.1
BuildRequires:  pkgconfig(gtksourceview-5) >= 5.17
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.50.2
BuildRequires:  pkgconfig(libsecret-1) >= 0.20
BuildRequires:  pkgconfig(libproxy-1.0) >= 0.5
BuildRequires:  pkgconfig(malcontent-0) >= 0.12.0
BuildRequires:  pkgconfig(libsystemd) >= 245

Requires:       flatpak
Requires:       gtk4 >= 4.22.1
Requires:       libadwaita >= 1.8
Requires:       libdex
Requires:       appstream
Requires:       libxmlb
Requires:       glycin
Requires:       glycin-gtk4
Requires:       libyaml
Requires:       libsoup3
Requires:       json-glib
Requires:       gtksourceview5
Requires:       webkitgtk6.0
Requires:       libsecret
Requires:       libproxy
Requires:       malcontent
Requires:       systemd-libs

%description
Bazaar is a fast and modern app store for discovering and installing Flatpak
applications and add-ons.

%prep
%autosetup

%build
%meson \
  -Dlibdex:liburing=disabled \
  -Dlibdex:introspection=disabled \
  -Dlibdex:vapi=false \
  -Dlibdex:pygobject=false
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/bazaar
%{_bindir}/bazaar-daemon
%{_bindir}/bazaar-dl-worker
%{_datadir}/applications/io.github.kolunmi.Bazaar.desktop
%{_datadir}/dbus-1/services/io.github.kolunmi.Bazaar.service
%{_datadir}/glib-2.0/schemas/io.github.kolunmi.Bazaar.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/io.github.kolunmi.Bazaar.svg
%{_datadir}/metainfo/io.github.kolunmi.Bazaar.metainfo.xml
%{_datadir}/locale/*/LC_MESSAGES/bazaar.mo

%changelog
* Tue Aug 25 2026 Bazaar Contributors <noreply@example.com> - 0.9.5-1
- Initial RPM package.
