from json import JSONDecodeError

from rest_framework.exceptions import ValidationError
from rest_framework.utils import json


def validate_json(j: str):
    try:
        return json.loads(j) is not None
    except JSONDecodeError as e:
        raise ValidationError(e)


def load_valid_json(j: str):
    try:
        return json.loads(j)
    except JSONDecodeError as e:
        raise ValidationError(e)