Summary:	3D physics game
Name:		irrlamb
Version:	0.2.0
Release:	1
License:	GPLv3+
Group:		Games/Arcade
Url:		http://code.google.com/p/irrlamb/
# obtaining the source :git clone https://github.com/jazztickets/irrlamb.git
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	dos2unix
BuildRequires:	audiere-devel
BuildRequires:	irrlicht-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(lua) >= 5.2
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(freetype2)

%description
irrlamb is a 3D game that probably involves a lot of physics and
frustrating gameplay.

%files
%doc %{_docdir}/%{name}/
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
#----------------------------------------------------------------------------

%prep
%setup -q

%build
%cmake
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Comment=irrlamb is a 3D game
Exec=%{name}
Icon=%{name}
Name=irrlamb
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

mkdir -p %{buildroot}%{_gamesbindir}
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_gamesbindir}/
rm -fr %{buildroot}%{_bindir}