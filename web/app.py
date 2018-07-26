""""
Simple Flask app that downloads and resizes images
"""

import re
import tempfile

from flask import Flask, request, make_response, send_file

from internal_services.image_service import (
    ImageService,
    ImageNotFound,
    GetImageError
)

application = Flask(__name__)


@application.route("/health", methods=["GET"])
def health():
    return "OK"


@application.route("/<parameters>", methods=["GET"])
def transform(parameters):
    image_url = request.args.get("url")
    width = None
    height = None

    matches = re.match('.*w_([0-9]+).*', parameters)

    if matches:
        width = int(matches[1])

    matches = re.match('.*h_([0-9]+).*', parameters)

    if matches:
        height = int(matches[1])

    if not width and not height:
        return make_response(
            '{"error": ["Must supply either width or height."]}', 400)

    try:
        img = ImageService.get_image(image_url)
    except ImageNotFound:
        return make_response(
            '{"error": ["URL does not exist"]}', 404)
    except GetImageError:
        return make_response(
            '{"error": ["The url does not point to a valid image"]}', 400)

    img_format = img.get_format_mimetype().split('/')[1]
    img = ImageService.resize(img, width, height)

    with tempfile.TemporaryFile() as tmp_file:
        img.save(tmp_file, img_format)
        tmp_file.seek(0)

        return send_file(tmp_file, mimetype=img_format)


if __name__ == '__main__':
    application.run(debug=True)
