from test1.generated.generated_routes import Basic_Auth
from RAMLFlask.rsp_element import Response_Element

class Basic_Auth():
    class Delete(Basic_Auth.Delete_Base):
        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            args = self.req.view_args
            if not check_basic_auth(self.req, args['user'], args['passwd']):
                return Response_Element(False, ('Error', 401))
            return Response_Element(False, (dict(authenticated=True, user=args['user']), 200))


def check_basic_auth(req, user, passwd):
    """Checks user authentication using HTTP Basic Auth."""

    auth = req.authorization
    return auth and auth.username == user and auth.password == passwd




