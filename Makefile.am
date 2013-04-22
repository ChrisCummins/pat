#
#		Pat build file
#

bin_SCRIPTS = pat
CLEANFILES = $(bin_SCRIPTS)

patsharedir = $(datadir)/@PACKAGE@
patshare_DATA = pat.py patrc

%: %.sh
	install $< $@

docdir = $(datadir)/doc/@PACKAGE@
doc_DATA = README

user = $(shell logname)
userhomedir = $(shell echo ~$(user))
userdatadir = $(userhomedir)/.pat

EXTRA_DIST = autogen.sh patrc

install-data-local:
	$(INSTALL) --mode=644 --owner=$(user) --group=$(user) patrc --no-target-directory $(userhomedir)/.patrc
	$(MKDIR_P) $(userdatadir)
	echo -n '' > lock
	echo -n '' > cache
	echo -n '' > log
	$(INSTALL) --mode=600 --owner=$(user) --group=$(user) lock cache --target-directory=$(userdatadir)
	rm -f lock cache log

uninstall-local:
	rm -f $(userhomedir)/.patrc
	rm -rf $(userdatadir)/.pat
