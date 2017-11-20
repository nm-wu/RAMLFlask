import datetime
import json
import time
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test2.generated.generated_routes import Streaming
from flask import request
from six.moves.urllib.parse import urlparse, urlunparse
import six
import base64


class Streaming():
    class Get(Streaming.Get_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            response = get_dict(self.req, 'url', 'args', 'headers', 'origin')

            n = self.req.view_args['n']

            def generate_stream():
                for i in xrange(n):
                    response['id'] = i
                    yield json.dumps(response) + '\n'

            output = ''
            for i in generate_stream():
                output += i

            return Response_Element(True, (json.dumps(output), 200), {"Content-Type": "application/json"})



def get_dict(req, *keys, **extras):
    """Returns request dict of given keys."""

    _keys = ('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json')

    assert all(map(_keys.__contains__, keys))
    data = req.data
    form = req.form
    form = semiflatten(req.form)

    try:
        _json = json.loads(data.decode('utf-8'))
    except (ValueError, TypeError):
        _json = None

    d = dict(
        url=get_url(req),
        args=semiflatten(req.args),
        form=form,
        data=json_safe(data),
        origin=req.headers.get('X-Forwarded-For', req.remote_addr),
        headers=get_headers(),
        files=get_files(req),
        json=_json
    )

    out_d = dict()

    for key in keys:
        out_d[key] = d.get(key)

    out_d.update(extras)

    return out_d


def semiflatten(multi):
    """Convert a MutiDict into a regular dict. If there are more than one value
    for a key, the result will have a list of values for the key. Otherwise it
    will have the plain value."""
    if multi:
        result = multi.to_dict(flat=False)
        for k, v in result.items():
            if len(v) == 1:
                result[k] = v[0]
        return result
    else:
        return multi


def get_url(request):
    """
    Since we might be hosted behind a proxy, we need to check the
    X-Forwarded-Proto, X-Forwarded-Protocol, or X-Forwarded-SSL headers
    to find out what protocol was used to access us.
    """
    protocol = request.headers.get('X-Forwarded-Proto') or request.headers.get('X-Forwarded-Protocol')
    if protocol is None and request.headers.get('X-Forwarded-Ssl') == 'on':
        protocol = 'https'
    if protocol is None:
        return request.url
    url = list(urlparse(request.url))
    url[0] = protocol
    return urlunparse(url)


def json_safe(string, content_type='application/octet-stream'):
    """Returns JSON-safe version of `string`.
    If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
    as it can safely be encoded to JSON string.
    If `string` contains raw/binary data, it is Base64-encoded, formatted and
    returned according to "data" URL scheme (RFC2397). Since JSON is not
    suitable for binary data, some additional encoding was necessary; "data"
    URL scheme was chosen for its simplicity.
    """
    try:
        string = string.decode('utf-8')
        _encoded = json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b''.join([
            b'data:',
            content_type.encode('utf-8'),
            b';base64,',
            base64.b64encode(string)
        ]).decode('utf-8')


def get_headers(hide_env=True):
    """Returns headers dict from request context."""

    headers = dict(request.headers.items())

    ENV_HEADERS = (
        'X-Varnish',
        'X-Request-Start',
        'X-Heroku-Queue-Depth',
        'X-Real-Ip',
        'X-Forwarded-Proto',
        'X-Forwarded-Protocol',
        'X-Forwarded-Ssl',
        'X-Heroku-Queue-Wait-Time',
        'X-Forwarded-For',
        'X-Heroku-Dynos-In-Use',
        'X-Forwarded-For',
        'X-Forwarded-Protocol',
        'X-Forwarded-Port',
        'Runscope-Service'
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
        content_type = request.files[k].content_type or 'application/octet-stream'
        val = json_safe(v.read(), content_type)
        if files.get(k):
            if not isinstance(files[k], list):
                files[k] = [files[k]]
            files[k].append(val)
        else:
            files[k] = val

    return files


class CaseInsensitiveDict(dict):
    """Case-insensitive Dictionary for headers.
    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header.
    """

    def _lower_keys(self):
        return [str.lower(k) for k in  self.keys()]

    def __contains__(self, key):
        return key.lower() in self._lower_keys()

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None
        if key in self:
            return list(self.items())[self._lower_keys().index(key.lower())][1]