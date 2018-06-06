# api/tests/test_config.py
"""This is the test config module

This module tests the various app configurations
"""

import unittest

from flask import current_app
from flask_testing import TestCase

from api.server import APP


class TestDevelopmentConfig(TestCase):
    """Test various app configs"""

    def create_app(self):
        """Create app method"""
        APP.config.from_object('api.server.config.DevelopmentConfig')
        return APP

    def test_app_is_development(self):
        """Test the app development config"""
        self.assertFalse(APP.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(APP.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    """Test Testing Config"""

    def create_app(self):
        """Create app"""
        APP.config.from_object('api.server.config.TestingConfig')
        return APP

    def test_app_is_testing(self):
        """Test if app is in testing config"""
        self.assertFalse(APP.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(APP.config['DEBUG'])


class TestProductionConfig(TestCase):
    """Test Production Config"""

    def create_app(self):
        """Create the app"""
        APP.config.from_object('api.server.config.ProductionConfig')
        return APP

    def test_app_is_production(self):
        """Test if the app is in prod config"""
        self.assertTrue(APP.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
