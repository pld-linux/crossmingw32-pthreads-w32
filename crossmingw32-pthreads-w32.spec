Summary:	POSIX Threads component implementation for Win32 - MinGW32 cross version
Summary(pl.UTF-8):	Implementacja komponentu POSIX Threads dla Win32 - wersja skrośna dla MinGW32
Name:		crossmingw32-pthreads-w32
Version:	2.11.0
Release:	2
License:	LGPL v2.1
Group:		Development/Libraries
Source0:	https://downloads.sourceforge.net/pthreads4w/pthreads4w-code-v%{version}.zip
# Source0-md5:	75c3ade4fa6aeff1d1d25d33f6bbce12
Patch0:		pthreads4w-winsock.patch
URL:		https://sourceforge.net/p/pthreads4w/wiki/Home/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-runtime >= 1:5.4.2-2
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-runtime >= 1:5.4.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
Pthreads-win32 (AKA pthreads4w) is an Open Source Software
implementation of the Threads component of the POSIX 1003.1c 1995
Standard for Microsoft's Win32 environment. Some functions from POSIX
1003.1b are also supported including semaphores. Other related
functions include the set of read-write lock functions. The library
also supports some of the functionality of the Open Group's Single
Unix specification, version 2, namely mutex types.

This package contains the cross version for Win32.

%description -l pl.UTF-8
PThreads-win32 (nazywana także pthreads4w) to mająca otwarte źródła
implementacja komponentu Threads (wątków) ze specyfikacji standardu
POSIX 1003.1c z 1995 roku dla środowiska Win32 Microsoftu. Obsługiwane
są także niektóre funkcje z POSIX 1003.1b, w tym semafory. Inne
powiązane funkcje to zbiór funkcji blokad r/w. Biblioteka obsługuje
także część funkcjonalności specyfikacji Single Unix w wersji 2
wydanej przez Open Group, a konkretnie typy mutex.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static POSIX Threads library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka POSIX Threads (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static POSIX Threads library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka POSIX Threads (wersja skrośna MinGW32).

%package dll
Summary:	POSIX Threads - DLL library for Windows
Summary(pl.UTF-8):	POSIX Threads - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
POSIX Threads - DLL library for Windows.

%description dll -l pl.UTF-8
POSIX Threads - biblioteka DLL dla Windows.

%prep
%setup -q -n pthreads4w-code-9808f0b151e6c6efe2d57f3b54a1fb9a19d1eb88
%patch0 -p1

mkdir lib

%build
%{__autoconf}
%{__autoheader}
%configure \
	--target=%{target} \
	--host=%{target}

for type in GC GCE GC-static GCE-static ; do
%{__make} clean
%{__make} -j1 $type \
	CROSS="%{target}-" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT='%{rpmcflags} $(CLEANUP)'

case "$type" in
  GC)
	#%{__mv} libpthreadGC2.a lib/libpthreadGC2.dll.a
	%{__mv} pthreadGC2.dll libpthreadGC2.dll.a lib
	;;
  GCE)
	#%{__mv} libpthreadGCE2.a lib/libpthreadGCE2.dll.a
	%{__mv} pthreadGCE2.dll libpthreadGCE2.dll.a lib
	;;
  GC-static)
	%{__mv} libpthreadGC2.a lib
	;;
  GCE-static)
	%{__mv} libpthreadGCE2.a lib
esac
done

%if 0%{!?debug:1}
%{target}-strip -R.comment -R.note lib/*.dll
%{target}-strip -g -R.comment -R.note lib/*.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_dlldir}}

install lib/*.dll $RPM_BUILD_ROOT%{_dlldir}
cp -p lib/*.a $RPM_BUILD_ROOT%{_libdir}
ln -s libpthreadGC2.dll.a $RPM_BUILD_ROOT%{_libdir}/libpthread.dll.a
ln -s libpthreadGC2.a $RPM_BUILD_ROOT%{_libdir}/libpthread.a
cp -p _ptw32.h pthread.h sched.h semaphore.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCE BUGS CONTRIBUTORS COPYING ChangeLog FAQ MAINTAINERS NEWS PROGRESS README README.CV README.NONPORTABLE TODO
%{_libdir}/libpthread.dll.a
%{_libdir}/libpthreadGC2.dll.a
%{_libdir}/libpthreadGCE2.dll.a
%{_includedir}/_ptw32.h
%{_includedir}/pthread.h
%{_includedir}/sched.h
%{_includedir}/semaphore.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libpthreadGC2.a
%{_libdir}/libpthreadGCE2.a
%{_libdir}/libpthread.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/pthreadGC2.dll
%{_dlldir}/pthreadGCE2.dll
