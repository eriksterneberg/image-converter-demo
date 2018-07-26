"""
Unit tests for functionality in ImageService that have no side effects
"""
import unittest

from internal_services.image_service import ImageService


class TestImageService(unittest.TestCase):

    def test_calculate_w_h(self):
        current_width, current_height = 100, 10

        new_width, new_height = 50, None
        self.assertEqual(
            ImageService.calculate_w_h(
                current_width, current_height, new_width, new_height),
            (50, 5)
        )

        new_width, new_height = None, 50
        self.assertEqual(
            ImageService.calculate_w_h(
                current_width, current_height, new_width, new_height),
            (500, 50)
        )

        new_width, new_height = 100, 50
        self.assertEqual(
            ImageService.calculate_w_h(
                current_width, current_height, new_width, new_height),
            (500, 50)
        )

        new_width, new_height = 300, 20
        self.assertEqual(
            ImageService.calculate_w_h(
                current_width, current_height, new_width, new_height),
            (300, 30)
        )
