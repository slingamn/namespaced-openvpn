PREFIX ?= /usr/local

.PHONY: test install

test:
	python3 -m flake8 ./namespaced-openvpn tests/
	python3 -m unittest discover

install:
	install -d -m 755 $(PREFIX)/sbin
	install -m 755 -v ./namespaced-openvpn $(PREFIX)/sbin/namespaced-openvpn
