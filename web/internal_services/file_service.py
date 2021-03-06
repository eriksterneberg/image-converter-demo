"""
Simple file service that uses local file cache to speed up requests
"""
import os
import base64

import requests
from requests.exceptions import MissingSchema, SSLError


class FileNotFound(Exception):
    pass


class FileService(object):

    CACHE_DIR = 'image_cache'

    def __init__(self, target_url: str) -> None:
        self.target_url = target_url

    def get_original(self) -> str:
        """
        Returns relative path to local file if it exists,
        otherwise downloads, caches and returns new filepath.
        """
        # Get cached copy if it exists
        cache_key = self.get_cache_key()

        if os.path.exists(cache_key):
            return cache_key

        # Otherwise, download file, save it, and return
        try:
            response = requests.get(self.target_url, stream=True)
        except (MissingSchema, SSLError):
            raise FileNotFound

        FileService.cache(response.content, cache_key)
        return cache_key

    def get_cache_key(self, prefix='') -> str:
        """
        Calculates a base64 version of the image_url and uses that
        as filename base.
        """
        filename = os.path.basename(self.target_url)

        base, extension = os.path.splitext(filename)
        base_encoded = base64.encodebytes(base.encode()).decode()

        filepath = os.path.join(
            FileService.CACHE_DIR,
            '{}{}.{}'.format(prefix, base_encoded, extension)
        )
        return filepath

    @staticmethod
    def cache(byte_array: bytes, filepath: str) -> str:
        """
        Takes a byte array, saves to disk and returns the filename.
        Uses Base64 to convert the base of the filename.
        """
        if not os.path.isdir(FileService.CACHE_DIR):
            os.mkdir(FileService.CACHE_DIR)

        with open(filepath, 'wb') as f:
            f.write(byte_array)
