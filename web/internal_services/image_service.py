"""
Simple service that encapsulates fetching and resizing images
"""
import requests

from PIL import Image


class ImageError(Exception):
    pass


class ImageService(object):

    @staticmethod
    def resize(filepath: str, resized_filepath: str,
               width: int, height: int) -> str:
        """
        Receives a string object; reads with Pillow, resizes and returns.

        If width is None it is calculated using the ratio between the old
        and new height in order to maintain the original height/width ratio.
        Same for height, if it is none. If both width and height are
        specified, we will use the number that has the highest ratio.
        """
        try:
            img = Image.open(filepath)
        except Exception as _:
            raise ImageError

        width, height = ImageService.calculate_w_h(
            img.width, img.height, width, height)

        mime_type = img.get_format_mimetype()

        with img.resize((int(width), int(height))) as new_img:
            ImageService.save(resized_filepath, new_img, mime_type)

        return mime_type

    @staticmethod
    def calculate_w_h(cur_width, cur_height, width, height) -> (int, int):
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

    @staticmethod
    def save(filepath: str, img, mime_type: str) -> None:
        img.save(filepath, mime_type.split('/')[1])
