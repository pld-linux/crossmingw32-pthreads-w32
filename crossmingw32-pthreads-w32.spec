Summary:	POSIX Threads component implementation for Win32 - MinGW32 cross version
Summary(pl.UTF-8):	Implementacja komponentu POSIX Threads dla Win32 - wersja skrośna dla MinGW32
Name:		crossmingw32-pthreads-w32
Version:	2.9.1
%define	dver	%(echo %{version} | tr . -)
Release:	2
License:	LGPL v2.1
Group:		Development/Libraries
Source0:	ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-%{dver}-release.tar.gz
# Source0-md5:	36ba827d6aa0fa9f9ae740a35626e2e3
URL:		http://www.sourceware.org/pthreads-win32/
BuildRequires:	crossmingw32-gcc
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Pthreads-win32 is an Open Source Software implementation of the
Threads component of the POSIX 1003.1c 1995 Standard for Microsoft's
Win32 environment. Some functions from POSIX 1003.1b are also
supported including semaphores. Other related functions include the
set of read-write lock functions. The library also supports some of
the functionality of the Open Group's Single Unix specification,
version 2, namely mutex types.

This package contains the cross version for Win32.

%description -l pl.UTF-8
PThreads-win32 to mająca otwarte źródła implementacja komponentu
Threads (wątków) ze specyfikacji standardu POSIX 1003.1c z 1995 roku
dla środowiska Win32 Microsoftu. Obsługiwane są także niektóre funkcje
z POSIX 1003.1b, w tym semafory. Inne powiązane funkcje to zbiór
funkcji blokad r/w. Biblioteka obsługuje także część funkcjonalności
specyfikacji Single Unix w wersji 2 wydanej przez Open Group, a
konkretnie typy mutex.

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
%setup -q -n pthreads-w32-%{dver}-release

mkdir lib

%build
for type in GC-inlined GCE-inlined GC-static ; do
%{__make} clean
%{__make} $type \
	CROSS="%{target}-" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT='%{rpmcflags} $(CLEANUP)'

case "$type" in
  GC-inlined)
	%{__mv} libpthreadGC2.a lib/libpthreadGC2.dll.a
	%{__mv} pthreadGC2.dll lib
	;;
  GCE-inlined)
	%{__mv} libpthreadGCE2.a lib/libpthreadGCE2.dll.a
	%{__mv} pthreadGCE2.dll lib
	;;
  GC-static)
	%{__mv} libpthreadGC2.a lib
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
install lib/*.a $RPM_BUILD_ROOT%{_libdir}
ln -s libpthreadGC2.dll.a $RPM_BUILD_ROOT%{_libdir}/libpthread.dll.a
ln -s libpthreadGC2.a $RPM_BUILD_ROOT%{_libdir}/libpthread.a
cp -p pthread.h sched.h semaphore.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCE BUGS CONTRIBUTORS COPYING ChangeLog FAQ MAINTAINERS NEWS PROGRESS README README.CV README.NONPORTABLE TODO
%{_libdir}/libpthread.dll.a
%{_libdir}/libpthreadGC2.dll.a
%{_libdir}/libpthreadGCE2.dll.a
%{_includedir}/pthread.h
%{_includedir}/sched.h
%{_includedir}/semaphore.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libpthreadGC2.a
%{_libdir}/libpthread.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/pthreadGC2.dll
%{_dlldir}/pthreadGCE2.dll
