CONFIG_DIR := ~/.config
BIN_DIR    := ~/.local/bin
SHARE_DIR  := ~/.local/share/pat

install:
	mkdir -p $(BIN_DIR)
	mkdir -p $(CONFIG_DIR)
	mkdir -p $(SHARE_DIR)
	install -m 755 pat $(BIN_DIR)/pat
	install -m 755 patrc $(CONFIG_DIR)/patrc
	install -m 755 pat.py $(SHARE_DIR)/pat.py
	rm -f $(SHARE_DIR)/cache
	touch $(SHARE_DIR)/cache
	chmod 600 $(SHARE_DIR)/cache

uninstall:
	rm -f $(BIN_DIR)/pat
	rm -f $(CONFIG_DIR)/patrc
	rm -f $(SHARE_DIR)/cache
	rm -f $(SHARE_DIR)/pat.py

help:
	@echo 'Usage: make <install | uninstall>'
