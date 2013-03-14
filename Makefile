CONFIG_DIR := ~/.config
BIN_DIR    := ~/bin
EXEC_DIR   := ~/.local/bin
SHARE_DIR  := ~/.local/share/pat

install:
	mkdir -p $(CONFIG_DIR)
	mkdir -p $(EXEC_DIR)
	mkdir -p $(SHARE_DIR)
	mkdir -p $(BIN_DIR)
	install -m 755 pat $(BIN_DIR)/pat
	install -m 755 pat.py $(EXEC_DIR)/pat.py
	install -m 755 patrc $(CONFIG_DIR)/patrc
	rm -f $(SHARE_DIR)/cache
	touch $(SHARE_DIR)/cache
	chmod 600 $(SHARE_DIR)/cache

uninstall:
	rm -f $(CONFIG_DIR)/patrc
	rm -f $(EXEC_DIR)/pat.py
	rm -f $(SHARE_DIR)/cache
	rm -f $(BIN_DIR)/pat

help:
	@echo 'Usage: make <install | uninstall>'
