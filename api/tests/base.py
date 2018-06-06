# api/tests/base.py
"""This is the base test module"""


from flask_testing import TestCase

from api.server import APP


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        APP.config.from_object('api.server.config.TestingConfig')
        return APP

    def setUp(self):
        pass

    def tearDown(self):
        pass
