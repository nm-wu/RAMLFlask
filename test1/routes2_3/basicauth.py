from test1.generated.generated_routes import Basic_Auth
from RAMLFlask.rsp_element import Response_Element

class Basic_Auth():
    class Delete(Basic_Auth.Delete_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):

            if not check_basic_authorization(self.req):
                return Response_Element(False, ('Error', 401))
            return Response_Element(False, (dict(authenticated=True), 200))



def check_basic_authorization(req):
    """Checks user authentication using HTTP Basic Auth."""

    auth = req.authorization
    return auth and auth.username == "httpbin" and auth.password == "secret"