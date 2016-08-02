.PHONY: test install

LINELEN=99

test:
	flake8 --max-line-len $(LINELEN) ./namespaced-openvpn tests/
	python3-flake8 --max-line-len $(LINELEN) ./namespaced-openvpn tests/
	python -m unittest discover
	python3 -m unittest discover

install:
	cp -v ./namespaced-openvpn /usr/local/sbin/namespaced-openvpn
