Summary:	3D game
Name:		irrlamb
Version:	0.0.5
Release:	%mkrel 2
License:	GPLv2+
Group:		Games/Arcade
URL:		http://code.google.com/p/irrlamb/
Source:		%{name}-%{version}-src.tar.bz2
Source1:	%{name}.png
Patch1:		%{name}-0.0.5-fix-irrlicht.patch
Patch2:		%{name}-0.0.5-various-fixes.patch
BuildRequires:	libboost-devel
BuildRequires:	libbullet-devel
BuildRequires:	mesaglut-devel
BuildRequires:	libaudiere-devel >= 1.9.4-6
BuildRequires:	irrlicht-devel
BuildRequires:	lua-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	scons
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
irrlamb is a 3D game that probably involves a lot of physics and
frustrating gameplay.

%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1

# adjust lua5.1 paths
sed -i -e 's|lua5.1/||g' src/engine/scripting.h
sed -i -e 's|lua5.1|lua|g' SConstruct

# use system libraries one
rm -rf libraries
sed -i -e 's|./libraries/include|%{_includedir}|g' SConstruct 
sed -i -e 's|./libraries/include/bullet|%{_includedir}/bullet|g' SConstruct
sed -i -e 's|./libraries/lib|%{_libdir}|g' SConstruct
sed -i -e 's|-O3 -DNDEBUG||g' SConstruct

%build
export CFLAGS="%{optflags}"
export CXXFLAGS=$CFLAGS

scons %{_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_gamesbindir}
install -m 755 %{name} %{buildroot}%{_gamesbindir}/%{name}.real

install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}
for i in art campaigns fonts levels meshes scenes scripts sounds terrain textures; do
	cp -R $i \
		%{buildroot}%{_gamesdatadir}/%{name}
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
