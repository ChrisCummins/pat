AC_PREREQ([2.69])

m4_define([pat_major_version], [0])
m4_define([pat_minor_version], [0])
m4_define([pat_micro_version], [2])
m4_define([pat_version],
          [pat_major_version.pat_minor_version.pat_micro_version])

AC_INIT([pat],
	[pat_version],
	[chrisc.101@gmail.com])

AC_SUBST([PAT_VERSION_MAJOR], [pat_major_version])
AC_SUBST([PAT_VERSION_MINOR], [pat_minor_version])
AC_SUBST([PAT_VERSION_MICRO], [pat_micro_version])
AC_SUBST([PAT_VERSION], [pat_version])

# Check for programs.
AC_PROG_INSTALL
AC_PROG_MKDIR_P

# Set prefix.
if test "x$prefix" = "xNONE" ; then
  prefix="/usr/local"
fi
if test "x$exec_prefix" = "xNONE" ; then
  exec_prefix=$prefix
fi
PREFIX=$prefix
AC_SUBST([PREFIX])

# Locations of installed files
PATRC=$HOME/.patrc
AC_SUBST([PATRC])

DEFAULT_PATRC=$prefix/share/pat/patrc
AC_SUBST([DEFAULT_PATRC])

PAT_PY=$prefix/share/pat/pat.py
AC_SUBST([PAT_PY])

DATE="$(date +'%B %d, %Y')"
AC_SUBST([DATE])

AM_INIT_AUTOMAKE([1.11 foreign -Wall -Werror -Wno-portability])
AM_PATH_PYTHON([2.5])

AC_OUTPUT([
	Makefile
	pat.py
	README
])
