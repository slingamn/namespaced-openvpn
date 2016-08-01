.PHONY: test install

test:
	pyflakes ./namespaced-openvpn tests/
	python3-pyflakes ./namespaced-openvpn tests/
	python -m unittest discover
	python3 -m unittest discover

install:
	cp -v ./namespaced-openvpn /usr/local/sbin/namespaced-openvpn
