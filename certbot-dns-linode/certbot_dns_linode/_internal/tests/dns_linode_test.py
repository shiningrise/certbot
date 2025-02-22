"""Tests for certbot_dns_linode._internal.dns_linode."""

import sys
import unittest
from unittest import mock

import pytest

from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util
from certbot_dns_linode._internal.dns_linode import Authenticator

TOKEN = 'a-token'
TOKEN_V4 = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconDNSAuthenticatorTest):

    DOMAIN_NOT_FOUND = Exception('Domain not found')

    def setUp(self):
        super().setUp()

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({"linode_key": TOKEN}, path)

        self.config = mock.MagicMock(linode_credentials=path,
                                     linode_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "linode")

    # pylint: disable=protected-access
    def test_api_version_4_detection(self):
        path = os.path.join(self.tempdir, 'file_4_auto.ini')
        dns_test_common.write({"linode_key": TOKEN_V4}, path)

        config = mock.MagicMock(linode_credentials=path,
                                linode_propagation_seconds=0)
        auth = Authenticator(config, "linode")

        assert auth._provider_name == "linode4"


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))  # pragma: no cover
