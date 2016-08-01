from __future__ import print_function
from __future__ import unicode_literals

import base64
import unittest

from .namespaced_openvpn import parse_dhcp_opts
from .namespaced_openvpn import parse_validate_args


class TestDHCPOpts(unittest.TestCase):

    def test_basic(self):
        env = {
            'foreign_option_1': 'dhcp-option DNS 8.8.8.8',
            'foreign_option_2': 'dhcp-option DNS 8.8.4.4',
            'foreign_option_3': 'dhcp-option DISABLE-NBT',
            'foreign_option_4': 'dhcp-option DOMAIN example.com',
        }
        self.assertEqual(
            parse_dhcp_opts(env),
            {
                'DNS': ['8.8.8.8', '8.8.4.4'],
                'DOMAIN': ['example.com'],
            }
        )


class TestParseValidateArgs(unittest.TestCase):

    def test_basic(self):
        args, openvpn_args, preexisting_routeup = parse_validate_args([
            '--remote', 'vpn.example.com', '--route-up', '/usr/bin/echo 1 2 3',
            '--config', '/dev/null', '--nobind', '--namespace', 'protected2',
            '--ping-restart', '0'
        ])
        self.assertEqual(args.dns, 'push')
        self.assertEqual(args.namespace, 'protected2')
        self.assertEqual(openvpn_args, [
            '--remote', 'vpn.example.com', '--config', '/dev/null',
            '--nobind', '--ping-restart', '0',
        ])
        self.assertEqual(
            base64.b64decode(preexisting_routeup),
            b'/usr/bin/echo 1 2 3',
        )


if __name__ == '__main__':
    unittest.main()
