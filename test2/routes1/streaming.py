import datetime
import json
import time
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test2.generated.generated_routes import Streaming

class Streaming():
    class Get(Streaming.Get_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):

            n = self.req.view_args['n']

            def generate():
                for row in xrange(n):
                    time.sleep(1)
                    yield str(row) + "\n"

            output = ''
            for i in generate():
                output += i

            return Response_Element(True, (json.dumps(output), 200), {"Transfer-Encoding": "chunked", "Content-Type": "application/json"})