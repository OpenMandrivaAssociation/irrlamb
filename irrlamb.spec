Summary:	3D physics game
Name:		irrlamb
Version:	0.1.1
Release:	1
License:	GPLv3
Group:		Games/Arcade
URL:		http://code.google.com/p/irrlamb/
Source0:	http://irrlamb.googlecode.com/files/%{name}-%{version}-src.tar.gz
Source1:	%{name}.png
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	boost-devel
BuildRequires:	freeglut-devel
BuildRequires:	audiere-devel >= 1.9.4-6
BuildRequires:	irrlicht-devel
BuildRequires:	lua-devel >= 5.1
BuildRequires:	cmake
BuildRequires:	dos2unix

%description
irrlamb is a 3D game that probably involves a lot of physics and
frustrating gameplay.

%prep
%setup -q -n %{name}-%{version}-src

# use system-wide bullet library
find src -name '*.h' | xargs sed -i -e 's|btBulletCollisionCommon.h|bullet/btBulletCollisionCommon.h|g'
find src -name '*.h' | xargs sed -i -e 's|btBulletDynamicsCommon.h|bullet/btBulletDynamicsCommon.h|g'

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS
export LDFLAGS="-ldl"

%cmake
%make

%install
pwd
install -dm 755 %{buildroot}%{_gamesbindir}
install -m 755 bin/Release/%{name} %{buildroot}%{_gamesbindir}/%{name}.real

install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}

for i in art fonts levels meshes scenes scripts shaders sounds textures; do
	cp -R working/$i %{buildroot}%{_gamesdatadir}/%{name}
done

# startscript
cat > %{name}-wrapper.sh << EOF
#!/bin/sh
if [ ! -d ~/.%{name} ]; then
	mkdir ~/.%{name}
	cd ~/.%{name}
	ln -s %{_gamesdatadir}/%{name}/* .
	cd ..
fi

cd ~/.%{name}
exec %{name}.real "$@"
EOF

install -m 755 %{name}-wrapper.sh %{buildroot}%{_gamesbindir}/%{name}

# icon and menu-entry
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps

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

%files
%doc deployment/*txt
%{_gamesbindir}/%{name}*
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
