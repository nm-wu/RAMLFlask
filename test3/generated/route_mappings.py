from flask import Blueprint, request
import generated_routes
import test3.routes1.threadsearch

route_imports = Blueprint('route_imports', __name__)

@route_imports.route('/v1/threads/search', methods=['get'])
def handle_Thread_Search_PNYKAIZKIMCKSNOGPMDN():
    handler = test3.routes1.threadsearch.Thread_Search.Get(request)
    return handler.handle_request()



