from flask import Blueprint, request
import generated_routes

route_imports = Blueprint('route_imports', __name__)

@route_imports.route('/v1/resource', methods=['get'])
def handle_First_One_get_INLCEXZJNMFZYCMSXZZP():
    handler = generated_routes.First_One_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['put'])
def handle_First_One_put_KLHFLGUNKGXKPSYJGQLO():
    handler = generated_routes.First_One_put_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['delete'])
def handle_First_One_delete_BYIPBQKTELWKDNFPKLOM():
    handler = generated_routes.First_One_delete_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['patch'])
def handle_First_One_patch_DCEQVRNBKUDVGRHDEGTP():
    handler = generated_routes.First_One_patch_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['options'])
def handle_First_One_options_NSCROURNMJZBSYLAVXCO():
    handler = generated_routes.First_One_options_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['trace'])
def handle_First_One_trace_DIPTDJHZZXJTNLKQHJGM():
    handler = generated_routes.First_One_trace_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource', methods=['connect'])
def handle_First_One_connect_YGKLCCUDZBOYXGLRMHLI():
    handler = generated_routes.First_One_connect_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource/<resourceId>', methods=['get'])
def handle_resource_with_resource_id_get_LPIULQBGNZMIBZOPYSMA(resourceId):
    handler = generated_routes.resource_with_resource_id_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource/<resourceId>', methods=['post'])
def handle_resource_with_resource_id_post_QPZFSGPRJOWSZFALQOVH(resourceId):
    handler = generated_routes.resource_with_resource_id_post_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/another/resource', methods=['get'])
def handle_Cats_get_AGCMVTSJYYZSGZVRDQBY():
    handler = generated_routes.Cats_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/another/resource', methods=['head'])
def handle_Cats_head_WJRBORFEAKUFAQUIITPJ():
    handler = generated_routes.Cats_head_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/another/resource', methods=['connect'])
def handle_Cats_connect_KACXTETBLICLEPHHZWMZ():
    handler = generated_routes.Cats_connect_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource-with-headers', methods=['get'])
def handle_Resource_With_headers_get_UNKFCONWELVXARCDDEYH():
    handler = generated_routes.Resource_With_headers_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/secured-resource', methods=['get'])
def handle_SO_SECURE_get_YSKQQUBKDLPMYPEENFWP():
    handler = generated_routes.SO_SECURE_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource-with-method-level-traits', methods=['get'])
def handle_First_One_with_method_level_traits_get_XCJQXKULICHKSRDYTUKQ():
    handler = generated_routes.First_One_with_method_level_traits_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource-with-form-and-multipart-form-parameters', methods=['get'])
def handle_resource_with_form_and_multipart_form_parameters_get_BVDGQSTKROTGFWZENEZP():
    handler = generated_routes.resource_with_form_and_multipart_form_parameters_get_Base(request)
    return handler.handle_request()



@route_imports.route('/v1/resource-with-repeatable-params', methods=['post'])
def handle_resource_with_repeatable_params_post_GKDLGXVEFXZAEBEYOYAY():
    handler = generated_routes.resource_with_repeatable_params_post_Base(request)
    return handler.handle_request()



