# ! /api/tests/base.py
# -*- coding: utf-8 -*-
"""Base setup for test
"""

from flask_testing import TestCase
import pytest

from api.server import APP
from api.server.models import USERS_LIST


class BaseTestCase(TestCase):
    """ Base Tests """

    @pytest.fixture
    def create_app(self):
        """Get Testing Config"""
        APP.config.from_object('api.server.config.TestingConfig')
        return APP

    def setUp(self):
        pass

    def tearDown(self):
        """Delete everything from user list after each test"""
        USERS_LIST.clear()
