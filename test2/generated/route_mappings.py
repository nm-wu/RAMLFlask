from flask import Blueprint, request
import generated_routes
import test2.routes6.streaming

route_imports = Blueprint('route_imports', __name__)

@route_imports.route('/v1/stream/<int:n>', methods=['get'])
def handle_Streaming_VRKPFJGFLCSCUTHBZMCA(n):
    handler = test2.routes6.streaming.Streaming.Get(request)
    return handler.handle_request()



