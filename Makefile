install:
	mkdir -p ~/.config
	mkdir -p ~/.local/bin
	mkdir -p ~/.local/share
	mkdir -p ~/bin
	install -m 755 pat ~/bin/pat
	install -m 755 pat.py ~/.local/bin/pat.py
	install -m 755 patrc ~/.config/patrc
	rm -f ~/.local/share/pat/cache
	touch ~/.local/share/pat/cache
	chmod 600 ~/.local/share/pat/cache

uninstall:
	rm -f ~/.config/patrc
	rm -f ~/.local/bin/pat.py
	rm -f ~/.local/share/cache
	rm -f ~/bin/pat
