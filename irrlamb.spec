Summary:	3D physics game
Name:		irrlamb
Version:	0.1.0
Release:	%mkrel 3
License:	GPLv3
Group:		Games/Arcade
URL:		http://code.google.com/p/irrlamb/
Source:		http://irrlamb.googlecode.com/files/%{name}-%{version}-src.tar.bz2
Source1:	%{name}.png
BuildRequires:	libboost-devel
BuildRequires:	libbullet-devel
BuildRequires:	mesaglut-devel
BuildRequires:	libaudiere-devel >= 1.9.4-6
BuildRequires:	irrlicht-devel
BuildRequires:	lua-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	scons
BuildRequires:	dos2unix
#BuildRequires:	tinyxml-devel
BuildRequires:	sqlite3-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
irrlamb is a 3D game that probably involves a lot of physics and
frustrating gameplay.

%prep
%setup -q -n %{name}

dos2unix *.txt
chmod 644 *.txt

# use system-installed tinyxml
#rm -r src/tinyxml
#find src -name '*.cpp' | xargs sed -i -e 's|../tinyxml/tinyxml.h|tinyxml.h|g'
#sed -i -e 's|glob.glob("src/tinyxml/*.cpp")||g' SConstruct

# use system-wide bullet library
rm -r src/bullet
sed -i -e 's|glob.glob("src/bullet/*.cpp")|"%{_includedir}/bullet/*.h"|g' SConstruct
find src -name '*.h' | xargs sed -i -e 's|btBulletCollisionCommon.h|bullet/btBulletCollisionCommon.h|g'
find src -name '*.h' | xargs sed -i -e 's|btBulletDynamicsCommon.h|bullet/btBulletDynamicsCommon.h|g'

# adjust lua5.1 paths
sed -i -e 's|lua5.1/||g' src/engine/scripting.h
sed -i -e 's|lua5.1|lua|g' SConstruct

# use system libraries one
rm -rf libraries
sed -i -e 's|./src/bullet|%{_includedir}/bullet|g' SConstruct
sed -i -e 's|/usr/local/lib|%{_libdir}|g' SConstruct
sed -i -e 's|Irrlicht sqlite3|Irrlicht sqlite3 GL bulletdynamics bulletcollision bulletmath|g' SConstruct

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS

%scons %{_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_gamesbindir}
install -m 755 %{name} %{buildroot}%{_gamesbindir}/%{name}.real

install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}
for i in art campaigns collision fonts levels meshes scenes scripts textures; do
	cp -R $i %{buildroot}%{_gamesdatadir}/%{name}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc changelog.txt readme.txt license.txt
%{_gamesbindir}/%{name}*
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
