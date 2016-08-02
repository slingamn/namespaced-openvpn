from __future__ import print_function
from __future__ import unicode_literals

import base64
import unittest

from collections import defaultdict

try:
    from cStringIO import StringIO
except ImportError:
    # py3
    from io import StringIO

from .namespaced_openvpn import parse_dhcp_opts
from .namespaced_openvpn import parse_validate_args
from .namespaced_openvpn import write_resolvconf


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


class TestWriteResolvConf(unittest.TestCase):

    def test_dns_only(self):
        opts = defaultdict(list)
        opts['DNS'] = ['10.0.0.1', '10.0.0.2']
        outfile = StringIO()
        write_resolvconf(outfile, opts)
        self.assertEqual(
            outfile.getvalue(),
            'nameserver 10.0.0.1\nnameserver 10.0.0.2\n'
        )

    def test_domain(self):
        opts = defaultdict(list)
        opts['DNS'] = ['8.8.8.8']
        opts['DOMAIN'] = ['example.com']
        outfile = StringIO()
        write_resolvconf(outfile, opts)
        self.assertEqual(
            outfile.getvalue(),
            'domain example.com\nnameserver 8.8.8.8\n'
        )

    def test_domains(self):
        opts = defaultdict(list)
        opts['DNS'] = ['8.8.4.4']
        opts['DOMAIN'] = ['example.com', 'example2.com']
        outfile = StringIO()
        write_resolvconf(outfile, opts)
        self.assertEqual(
            outfile.getvalue(),
            'search example.com example2.com\nnameserver 8.8.4.4\n'
        )

    def test_all(self):
        opts = defaultdict(list)
        opts['DNS'] = ['8.8.4.4']
        opts['DOMAIN'] = ['example.com']
        opts['DOMAIN-SEARCH'] = ['test.example.com', 'check.example.com']
        outfile = StringIO()
        write_resolvconf(outfile, opts)
        self.assertEqual(
            outfile.getvalue(),
            'domain example.com\nsearch test.example.com check.example.com\nnameserver 8.8.4.4\n'
        )

    def test_truncate(self):
        opts = defaultdict(list)
        opts['DNS'] = ['10.10.10.%d' % (i,) for i in range(100)]
        opts['DOMAIN'] = ['example%d.com' % (i,) for i in range(100)]
        expected_nameservers = ''.join('nameserver 10.10.10.%d\n' % (i,) for i in range(3))
        expected_search = ' '.join(opts['DOMAIN'][:6])
        outfile = StringIO()
        write_resolvconf(outfile, opts)
        self.assertEqual(
            outfile.getvalue(),
            'search %s\n%s' % (expected_search, expected_nameservers),
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
