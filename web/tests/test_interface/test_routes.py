"""
Functional tests for all routes
"""

import os
import shutil
import unittest
from unittest.mock import patch, MagicMock

from requests.exceptions import MissingSchema, SSLError

import app
from internal_services.file_service import FileService

TEST_DATA_FOLDER = 'tests/data/'


class TestTransformRoute(unittest.TestCase):

    def setUp(self):
        app.application.testing = True
        self.app = app.application.test_client()

    def tearDown(self):
        try:
            shutil.rmtree(FileService.CACHE_DIR)
        except FileNotFoundError:
            pass

    def test_health_endpoint(self):
        response = self.app.get("/health")
        self.assertTrue(b'OK' in response.data)

    def test_transform_illegal_width_and_height(self):
        response = self.app.get("/foo")
        self.assertTrue(
            b'{"error": ["Must supply either width or height."]}'
            in response.data)
        self.assertEqual(response.status_code, 400)

    @patch('internal_services.image_service.requests.get')
    def test_transform_url_malformed(self, get_mock):
        get_mock.side_effect = MissingSchema

        response = self.app.get("/w_100?url=foo")
        self.assertTrue(b'{"error": ["URL does not exist"]}' in response.data)
        self.assertEqual(response.status_code, 404)

    @patch('internal_services.image_service.requests.get')
    def test_transform_url_ssl_error(self, get_mock):
        get_mock.side_effect = SSLError
        response = self.app.get("/h_100?url=https://www.foo.com/bar.gif")
        self.assertTrue(b'{"error": ["URL does not exist"]}' in response.data)
        self.assertEqual(response.status_code, 404)

    @patch('internal_services.file_service.requests.get')
    def test_transform__response_is_text(self, get_mock):
        get_mock.return_value = MagicMock(content=b"This is a text response")

        response = self.app.get("/h_100?url=https://www.foo.com/bar.gif")
        self.assertTrue(
            b'{"error": ["The url does not point to a valid image"]}'
            in response.data
        )
        self.assertEqual(response.status_code, 400)

    @patch('internal_services.image_service.requests.get')
    def test_transform_happy_path(self, get_mock):
        test_file_path = os.path.join(TEST_DATA_FOLDER, 'test.jpeg')

        with open(test_file_path, 'rb') as test_file:
            image_bytes = test_file.read()
            get_mock.return_value = MagicMock(content=image_bytes)
            response = self.app.get(
                "/w_50,h_50?url=https://www.foo.com/bar.jpeg")
            self.assertEqual(response.mimetype, 'image/jpeg')
            self.assertEqual(response.status_code, 200)
