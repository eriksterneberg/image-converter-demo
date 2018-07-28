""""
Simple Flask app that downloads and resizes images
"""

import os
import re
import tempfile

from flask import Flask, request, make_response, send_file

from internal_services.file_service import FileService, FileNotFound
from internal_services.image_service import ImageService, ImageError

application = Flask(__name__)


# Using two different regex is slower than one, but more readable.
# Of course the better design is to use GET parameters instead of a string,
# which might make it faster if there are many parameters.
WIDTH_REGEX = r'^w_(?P<width>[1-9][0-9]*)$'
HEIGHT_REGEX = r'^h_(?P<height>[1-9][0-9]*)$'


@application.route("/health", methods=["GET"])
def health():
    return "OK"


@application.route("/<parameters>", methods=["GET"])
def transform(parameters):
    target_url = request.args.get("url")
    width = None
    height = None

    for param in parameters.split(','):
        try:
            width = int(re.match(WIDTH_REGEX, param).group('width'))
            continue
        except AttributeError:
            pass

        try:
            height = int(re.match(HEIGHT_REGEX, param).group('height'))
        except AttributeError:
            pass

    if not width and not height:
        return make_response(
            '{"error": ["Must supply either width or height."]}', 400)

    file_service = FileService(target_url)
    prefix = '{}-{}-'.format(height, width)
    resized_filepath = file_service.get_cache_key(prefix)

    # 1. If resized image exists, return that
    if os.path.exists(resized_filepath):
        img_format = resized_filepath.split('.')[-1]
        return send_file(
            resized_filepath, mimetype='image/{}'.format(img_format))

    # 2. Otherwise download original and cache that
    try:
        filepath = file_service.get_original()
    except FileNotFound:
        return make_response(
            '{"error": ["URL does not exist"]}', 404)

    # 3. Resize image
    try:
        mime_type = ImageService.resize(
            filepath, resized_filepath, width, height)
    except ImageError:
        return make_response(
            '{"error": ["The url does not point to a valid image"]}', 400)

    return send_file(resized_filepath, mimetype=mime_type)


if __name__ == '__main__':
    application.run(debug=True)
