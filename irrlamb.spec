Summary:		irrlamb is a 3D game
Name:			irrlamb
Version:		0.0.4
Release:		%mkrel 1
License:		GPL
Group:			Games
URL:			http://code.google.com/p/irrlamb/
Source:			%{name}-%{version}-src.tar.bz2
Source1:		%{name}.png
BuildRequires:		libboost-devel
BuildRequires:		libbullet-devel
BuildRequires:		mesaglut-devel
BuildRequires:		libaudiere-devel
BuildRequires:		irrlicht-devel
BuildRequires:		lua-devel
BuildRequires:		pkgconfig
BuildRequires:		scons
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot

%description
irrlamb is a 3D game that probably involves a lot of physics and
frustrating gameplay.

%prep
%setup -q -n %{name}

# adjust lua5.1 paths
sed -i -e 's|lua5.1/||g' src/engine/scripting.h
sed -i -e 's|lua5.1|lua|g' SConstruct

%build
# Setup for parallel builds
numprocs=`egrep -c ^cpu[0-9]+ /proc/stat || :`
if [ "$numprocs" = "0" ]; then
	numprocs=1
fi

scons -j$numprocs

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_gamesbindir}
install -m 755 %{name} %{buildroot}%{_gamesbindir}/%{name}.real

install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}
for i in art fonts levels meshes scenes scripts terrain textures; do
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
Exec=%{name}-wrapper.sh
Icon=%{name}.png
Name=irrlamb
Path=
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
