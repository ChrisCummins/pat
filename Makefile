# Use V=1 to see full verbosity
QUIET_  = @
QUIET   = $(QUIET_$(V))

conf_dir    := ~/.config
bin_dir     := ~/.local/bin
share_dir   := ~/.local/share/pat

conf_files  := patrc
bin_files   := pat
share_files := patrc pat.py

RM      := rm -f
MKDIR   := mkdir -p
INSTALL := install

# Make verbosity match the build
	ifeq ($(QUIET),@)
RM      += -v
MKDIR   += -v
INSTALL += -v
endif

install: uninstall
	$(QUIET)$(MKDIR) $(bin_dir) $(conf_dir) $(share_dir)
	$(QUIET)$(INSTALL) -m 755 $(bin_files) -t $(bin_dir)
	$(QUIET)$(INSTALL) -m 644 $(conf_files) -t $(conf_dir)
	$(QUIET)$(INSTALL) -m 644 $(share_files) -t $(share_dir)

uninstall:
	$(QUIET)$(RM) $(patsubst %,$(bin_dir)/%,$(bin_files))
	$(QUIET)$(RM) $(patsubst %,$(conf_dir)/%,$(conf_files))
	$(QUIET)$(RM) $(patsubst %,$(share_dir)/%,$(share_files))

help:
	@echo 'Usage: make <install | uninstall>'
