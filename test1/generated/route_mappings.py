from flask import Blueprint, request
import generated_routes
import test1.routes1.basicauth

route_imports = Blueprint('route_imports', __name__)

@route_imports.route('/v1/basic-auth', methods=['delete'])
def handle_Basic_Auth_PWJNMFMEQTUWMDNUPVIT():
    handler = test1.routes1.basicauth.Basic_Auth.Delete(request)
    return handler.handle_request()



