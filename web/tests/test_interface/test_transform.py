import unittest

import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.application.testing = True
        self.app = app.application.test_client()

    def tearDown(self):
        pass

    def test_health_endpoint(self):
        response = self.app.get("/health")
        assert b'OK' in response.data
