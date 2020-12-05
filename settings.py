import os
import json
from flask import Response
from functools import wraps

UPLOAD_DIR = os.path.abspath("./data")


def as_json(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        res = f(*args, **kwargs)

        res = json.dumps(res, ensure_ascii=False).encode('utf8')

        return Response(res, content_type='application/json; charset=utf-8')

    return decorated_function
