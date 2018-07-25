import os

from flask import Flask

application = Flask(__name__)


@application.route("/health", methods=["GET"])
def health():
    return "OK"


if __name__ == '__main__':
    application.run(debug=True)
