"""
Simple service that encapsulates fetching and resizing images
"""
import requests
from requests.exceptions import MissingSchema, SSLError
from io import BytesIO
from PIL import Image


class ImageNotFound(Exception):
    pass


class GetImageError(Exception):
    pass


class ImageService(object):

    @staticmethod
    def get_image(url: str) -> str:
        """
        Download image

        TODO: Create a FileService that caches image locally
        """
        try:
            response = requests.get(url, stream=True)
        except (MissingSchema, SSLError):
            raise ImageNotFound
        try:
            img = Image.open(BytesIO(response.content))
            return img
        except Exception as _:
            raise GetImageError

    @staticmethod
    def resize(img, width: int, height: int):
        """
        Receives a Pillow image object as parameter; resizes and returns.

        If width is None it is calculated using the ratio between the old
        and new height in order to maintain the original height/width ratio.
        Same for height, if it is none. If both width and height are
        specified, we will use the number that has the highest ratio.
        """
        width, height = ImageService.calculate_w_h(
            img.width, img.height, width, height)
        new_img = img.resize((int(width), int(height)))
        return new_img

    @staticmethod
    def calculate_w_h(cur_width, cur_height, width, height):
        if width:
            w_ratio = width / cur_width

        if height:
            h_ratio = height / cur_height

        if width and not height:
            height = cur_height * w_ratio

        elif height and not width:
            width = cur_width * h_ratio

        else:
            ratio = max([w_ratio, h_ratio])
            width = cur_width * ratio
            height = cur_height * ratio

        return width, height
