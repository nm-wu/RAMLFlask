import json
from flask import Response

class Response_Element(object):
    """Response object for usage in various generated and handwritten classes"""

    def __init__(self, proceed=True, resp=('', 200), headers=None):
        self.proceed = proceed
        self.value = resp[0]
        self.code = resp[1]
        self.headers = headers

    def create_response(self):
        if type(self.value) == dict:
            self.value = json.dumps(self.value)

        if self.headers == None:
            return (self.value, self.code)
        else:
            resp = Response(self.value, self.code)
            resp.headers = self.headers
            return resp