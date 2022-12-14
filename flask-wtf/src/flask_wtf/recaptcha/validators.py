import json
from urllib import request as http

from flask import current_app
from flask import request
from werkzeug.urls import url_encode
from wtforms import ValidationError

from .._compat import to_bytes
from .._compat import to_unicode

RECAPTCHA_VERIFY_SERVER = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_ERROR_CODES = {
    "missing-input-secret": "The secret parameter is missing.",
    "invalid-input-secret": "The secret parameter is invalid or malformed.",
    "missing-input-response": "The response parameter is missing.",
    "invalid-input-response": "The response parameter is invalid or malformed.",
}


__all__ = ["Recaptcha"]


class Recaptcha:
    """Validates a ReCaptcha."""

    def __init__(self, message=None):
        if message is None:
            message = RECAPTCHA_ERROR_CODES["missing-input-response"]
        self.message = message

    def __call__(self, form, field):
        if current_app.testing:
            return True

        if request.json:
            response = request.json.get("g-recaptcha-response", "")
        else:
            response = request.form.get("g-recaptcha-response", "")
        remote_ip = request.remote_addr

        if not response:
            raise ValidationError(field.gettext(self.message))

        if not self._validate_recaptcha(response, remote_ip):
            field.recaptcha_error = "incorrect-captcha-sol"
            raise ValidationError(field.gettext(self.message))

    def _validate_recaptcha(self, response, remote_addr):
        """Performs the actual validation."""
        try:
            private_key = current_app.config["RECAPTCHA_PRIVATE_KEY"]
        except KeyError:
            raise RuntimeError("No RECAPTCHA_PRIVATE_KEY config set")

        data = url_encode(
            {"secret": private_key, "remoteip": remote_addr, "response": response}
        )

        http_response = http.urlopen(RECAPTCHA_VERIFY_SERVER, to_bytes(data))

        if http_response.code != 200:
            return False

        json_resp = json.loads(to_unicode(http_response.read()))

        if json_resp["success"]:
            return True

        for error in json_resp.get("error-codes", []):
            if error in RECAPTCHA_ERROR_CODES:
                raise ValidationError(RECAPTCHA_ERROR_CODES[error])

        return False
