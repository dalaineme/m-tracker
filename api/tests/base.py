# ! /api/tests/base.py
# -*- coding: utf-8 -*-
"""Base setup for test
"""

from flask_testing import TestCase

from api.server import APP


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        """Get Testing Config"""
        APP.config.from_object('api.server.config.TestingConfig')
        return APP

    def setUp(self):
        pass

    def tearDown(self):
        pass
