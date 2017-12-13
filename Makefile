.PHONY: test install

test:
	python2 -m flake8 ./namespaced-openvpn tests/
	python3 -m flake8 ./namespaced-openvpn tests/
	python2 -m unittest discover
	python3 -m unittest discover

install:
	cp -v ./namespaced-openvpn /usr/local/sbin/namespaced-openvpn
