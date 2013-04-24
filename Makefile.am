#
#		Pat build file
#

bin_SCRIPTS = pat
CLEANFILES = $(bin_SCRIPTS)

patsharedir = $(datadir)/@PACKAGE@
patshare_DATA = patrc

%: %.py
	$(INSTALL) $< $@

docdir = $(datadir)/doc/@PACKAGE@
doc_DATA = README

user = $(shell logname)
userhomedir = $(shell echo ~$(user))
userdatadir = $(userhomedir)/.pat

EXTRA_DIST = autogen.sh patrc

install-data-local:
	$(INSTALL) --mode=644 --owner=$(user) --group=$(user) patrc --no-target-directory $(userhomedir)/.patrc
	$(MKDIR_P) $(userdatadir)
	echo -n '' > cache
	echo -n '' > log
	$(INSTALL) --mode=600 --owner=$(user) --group=$(user) cache log --target-directory=$(userdatadir)
	rm -f cache log

uninstall-local:
	rm -f $(userhomedir)/.patrc
	rm -rf $(userdatadir)/.pat
