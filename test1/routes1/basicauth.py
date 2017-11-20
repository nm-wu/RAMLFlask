from test1.generated.generated_routes import Basic_Auth
from RAMLFlask.rsp_element import Response_Element
from flask import request

class Basic_Auth():
    class Delete(Basic_Auth.Delete_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):

            if not check_basic_authorization(self.req):
                return Response_Element(False, ('Error', 401))
            return make_response('auth ok')



def check_basic_authorization(req):
    """Checks user authentication using HTTP Basic Auth."""

    auth = req.authorization
    return auth and auth.username == "httpbin" and auth.password == "secret"


def make_response(text):
    return Response_Element(True, (text, 200))