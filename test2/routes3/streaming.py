import datetime
import json
import time
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test2.generated.generated_routes import Streaming
from flask import request

class Streaming():
    class Get(Streaming.Get_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            response = get_dict(self.req, 'url', 'args', 'headers', 'origin')

            n = self.req.view_args['n']

            def generate_stream():
                for i in xrange(n):
                    response["id"] = i
                    yield json.dumps(response) + "\n"
                    time.sleep(1)

            output = ''
            for i in generate_stream():
                output += i

            return Response_Element(True, (json.dumps(output), 200), {"Transfer-Encoding": "chunked", "Content-Type": "application/json"})


def get_dict(req, *keys, **extras):
    """Returns request dict of given keys."""

    _keys = ('url', 'args', 'form', 'data', 'origin', 'headers', 'files')

    assert all(map(_keys.__contains__, keys))

    data = req.data
    form = req.form

    if (len(form) == 1) and (not data):
        if not form.values().pop():
            data = form.keys().pop()
            form = None

    d = dict(
        url=req.url,
        args=request.args,
        form=form,
        data=data,
        origin=req.remote_addr,
        headers=get_headers(),
        files=get_files(req)
    )

    out_d = dict()

    for key in keys:
        out_d[key] = d.get(key)

    out_d.update(extras)

    return out_d


def get_headers(hide_env=True):
    """Returns headers dict from request context."""

    headers = dict(request.headers.items())

    ENV_HEADERS = (
        'X-Varnish',
        'X-Request-Start',
        'X-Heroku-Queue-Depth',
        'X-Real-Ip',
        'X-Forwarded-Proto',
        'X-Heroku-Queue-Wait-Time',
        'X-Forwarded-For',
        'X-Heroku-Dynos-In-Use',
        'X-Forwarded-For',
        'X-Forwarded-Protocol'
    )

    if hide_env and ('show_env' not in request.args):
        for key in ENV_HEADERS:
            try:
                del headers[key]
            except KeyError:
                pass

    return CaseInsensitiveDict(headers.items())


def get_files(req):
    """Returns files dict from request context."""

    files = dict()

    for k, v in req.files.items():
        files[k] = v.read()

    return files


class CaseInsensitiveDict(dict):
    """Case-insensitive Dictionary for headers.
    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header.
    """

    def _lower_keys(self):
        return map(str.lower, self.keys())

    def __contains__(self, key):
        return key.lower() in self._lower_keys()

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None
        if key in self:
            return self.items()[self._lower_keys().index(key.lower())][1]