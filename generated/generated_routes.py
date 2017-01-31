import datetime
from collections import OrderedDict
from delegates import basic_auth_delegate

import re
from flask import request
from delegates import pre_req_delegate, post_req_delegate
from FlaskRAML.rsp_element import Response_Element
from importlib import import_module

class Generated_Class_Base(object):
    """Base Class for generated classes"""

    def __init__(self, request, resp_t=(False, [200, 400, 500])):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def pre_req_handler(self):
        pre_r_delegate = pre_req_delegate.Pre_Req_Delegate()
        return pre_r_delegate.handle_delegation(request)

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        custom_processing = self.add_validate_params_handler()
        return Response_Element()

    def add_validate_params_handler(self, **kwargs):
        return Response_Element()

    def request_handler(self):
        return Response_Element()

    def post_req_handler(self, response):
        post_r_delegate = post_req_delegate.Post_Req_Delegate()
        new_result = post_r_delegate.handle_delegation(request)

        if new_result is None or response[1] == 400:
            new_result = response
        else:
            new_result = new_result.response

        return Response_Element(False, new_result)

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(Generated_Class_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def check_response_code(self, code):
        if self.enforced_type:
            if code in  self.resp_t:
                return False
            else:
                return True
        else:
            return True

    def handle_request(self):
        overridden = self.check_overriden()

        if overridden:
            exception = 'This class should not be overridden: ' + str(overridden).strip('[]')
            raise Exception(exception)
            return 'Internal Server Error', 500

        res_pre_req = self.pre_req_handler()
        if res_pre_req.proceed is False:
            if self.check_response_code(res_pre_req.response[1]):
                return res_pre_req.response
            else:
                exception = 'This return code should not be used: ' + str(res_pre_req.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_auth = self.auth_handler()
        if res_auth.proceed is False:
            if self.check_response_code(res_auth.response[1]):
                return res_auth.response
            else:
                exception = 'This return code should not be used: ' + str(res_auth.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_validate = self.validate_params_handler()
        if res_validate.proceed is False:
            if self.check_response_code(res_validate.response[1]):
                return res_validate.response
            else:
                exception = 'This return code should not be used: ' + str(res_validate.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_request = self.request_handler()
        if res_request.proceed is False:
            if self.check_response_code(res_request.response[1]):
                return res_request.response
            else:
                exception = 'This return code should not be used: ' + str(res_request.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_post_req = self.post_req_handler(res_request.response)

        if self.check_response_code(res_request.response[1]):
            return res_request.response
        else:
            exception = 'This return code should not be used: ' + str(res_request.response.resp)
            raise Exception(exception)
            return 'Internal Server Error', 500

        return res_post_req.resp


def validate_request_parameter(reqs, input):
    status = True

    for r in reqs:
        if r['source'] == 'uri_param':
            selected_input = None
            for q in input:
                if r['validation']['name'] == q:
                    selected_input = q

            if selected_input == None:
                if type(r) is not list:
                    if type(r['validation']) is not list:
                        if r['validation']['required'] == True:
                            return Response_Element(False, ('', 400))
                    else:
                        for mime in r['validation']:
                            for valid in mime['params']:
                                if type(valid) is not list:
                                    if valid['validation']['required'] == True:
                                        return Response_Element(False, ('', 400))
                                else:
                                    for v in valid:
                                        if v['validation']['required'] == True:
                                            return Response_Element(False, ('', 400))
            else:
                if perform_validation(selected_input, input[selected_input], r['validation']) == False:
                    status = False

    if status == True:
        return Response_Element()
    else:
        return Response_Element(False, ('', 400))

def validate_query_string(reqs, input):
    status = True
    for r in reqs:
        if r['source'] == 'get_param':
            selected_input = None
            for q in input:
                if r['validation']['name'] == q:
                    selected_input = q

            if selected_input == None:
                if type(r) is not list:
                    if r is not list:
                        if r['validation'] is not list:
                            if r['validation']['required'] == True:
                                return Response_Element(False, ('', 400))
            else:
                if perform_validation(selected_input, input[selected_input], r['validation']) == False:
                    status = False

    if status == True:
        return Response_Element()
    else:
        return Response_Element(False, ('', 400))


def validate_body_params(reqs, input, mime_type):
    if mime_type == None or mime_type == '':
        return Response_Element()

    mt = mime_type.replace('/', '_').replace('-', '_')
    delegates = 'delegates.' + mt + '_delegate'

    module = import_module(delegates, mt)
    instance = module.validation_Delegate()

    if instance.handle_delegation([reqs, input]) != False:
        return Response_Element()
    else:
        return Response_Element(False, ('', 400))

def find_corresponding_param(param, uri_inputs=None, get_inputs=None, body_inputs=None, mime_type=None):
    if param == 'BODY_mime_type':
        return mime_type

    keyword = param.split('_')

    if keyword[0] == 'URI':
        return uri_inputs.get(keyword[1], None)

    if keyword[0] == 'GET':
        return get_inputs.get(keyword[1], None)

    if keyword[0] == 'BODY':
        return body_inputs


def perform_validation(name, value, validation):
    v_type = type(value)
    if v_type == unicode or v_type == str:
        v_type = 'string'

    if validation['enum'] != None:
        match = False
        for e in validation['enum']:
            if e == value:
                match = True

        if match == False:
            return False

    if validation['type'] == v_type:
        if validation['type'] == 'string':
            if len(value) > validation['max_length'] or len(value) < validation['min_length']:
                return False

        if validation['type'] == 'int':
            if value > validation['maximum'] or value < validation['minimum']:
                return False
    else:
        return False

    if validation['pattern'] != None:
        result = re.match(validation['pattern'], value)
        if not result:
            return False

    return True
class First_One_get_Base(Generated_Class_Base):
    """get the first one"""


    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_put_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([203, 201]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_put_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_delete_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([203, 201]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_delete_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_patch_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_patch_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_options_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_options_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_trace_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_trace_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_connect_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_connect_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class resource_with_resource_id_get_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'What to filter', 'min_length': None, 'name': 'filter', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}, {'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}]
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_filter", uri_in, get_in, body_in, mime_type), find_corresponding_param("URI_resourceId", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, GET_filter = None, URI_resourceId = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(resource_with_resource_id_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class resource_with_resource_id_post_Base(Generated_Class_Base):
    """This is a resource description *with* some _markdown_ embedded in it"""


    def __init__(self, request, resp_t=(False, set([203, 201]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}, {'source': 'body', 'validation': [{'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}, {'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'A description of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post'}}], 'errors': [], 'mime-type': 'application/x-www-form-urlencoded', 'example': None, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}, {'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'A description of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post'}}], 'errors': [], 'mime-type': 'multipart/form-data', 'example': None, 'schema': None}]}]
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("URI_resourceId", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, URI_resourceId = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(resource_with_resource_id_post_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class Cats_get_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': 1, 'desc': 'Which page to display', 'min_length': None, 'name': 'chunk', 'default': None, 'pattern': None, 'required': True, 'maximum': 100, 'max_length': None, 'type': 'integer', 'example': 1}}, {'source': 'get_param', 'validation': {'repeat': False, 'enum': ['oldest', 'newest'], 'minimum': None, 'desc': 'The sort order of resources', 'min_length': 5, 'name': 'order', 'default': 'newest', 'pattern': None, 'required': False, 'maximum': None, 'max_length': 7, 'type': 'string', 'example': 'oldest'}}, {'source': 'get_param', 'validation': {'repeat': True, 'enum': None, 'minimum': None, 'desc': 'A query parameter', 'min_length': None, 'name': 'query', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}]
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_order", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_chunk", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_query", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, GET_order = None, GET_chunk = None, GET_query = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(Cats_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class Cats_head_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([203, 201]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(Cats_head_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class Cats_connect_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(Cats_connect_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class Resource_With_headers_get_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(Resource_With_headers_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class SO_SECURE_get_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        a_delegate = basic_auth_delegate.Basic_Auth_Delegate() 
        a_delegate.handle_delegation(request)  
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(SO_SECURE_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class First_One_with_method_level_traits_get_Base(Generated_Class_Base):
    """get the first one"""


    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = []
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(First_One_with_method_level_traits_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class resource_with_form_and_multipart_form_parameters_get_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Your value for some thing.', 'min_length': None, 'name': 'some_query_param', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'my value'}}, {'source': 'body', 'validation': [{'params': [], 'errors': [], 'mime-type': 'application/json', 'example': {u'api_key': u'c4f820f0420a013ea143230c290fbf99'}, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'errors': [], 'mime-type': 'application/x-www-form-urlencoded', 'example': None, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'errors': [], 'mime-type': 'multipart/form-data', 'example': None, 'schema': None}]}]
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_some_query_param", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, GET_some_query_param = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(resource_with_form_and_multipart_form_parameters_get_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

class resource_with_repeatable_params_post_Base(Generated_Class_Base):
    

    def __init__(self, request, resp_t=(False, set([]))):
        self.req = request
        self.enforced_type = True
        self.resp_t = resp_t

    def auth_handler(self):
        return Response_Element()

    def validate_params_handler(self):
        validations = [{'source': 'get_param', 'validation': {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someParam', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}, {'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}, {'source': 'body', 'validation': [{'params': [{'source': 'body_param', 'validation': {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': None, 'example': None}}], 'errors': [], 'mime-type': 'application/x-www-form-urlencoded', 'example': None, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'file', 'example': None}}, [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someMultipartFormParamWithMultipleTypes', 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'file', 'example': None}}, {'source': 'body_param', 'validation': {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someMultipartFormParamWithMultipleTypes', 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}]], 'errors': [], 'mime-type': 'multipart/form-data', 'example': None, 'schema': None}]}]
        uri_in = self.req.view_args
        get_in = self.req.args
        body_in = self.req.data
        mime_type = self.req.mimetype

        # Validate URI paramters
        check = validate_request_parameter(validations, uri_in)
        if check.proceed == False:
            return check

        # Validate query string
        check = validate_query_string(validations, get_in)
        if check.proceed == False:
            return check

        # Validate query mime type and body
        check = validate_body_params(validations, body_in, mime_type)
        if check.proceed == False:
            return check

        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_notRepeatable", uri_in, get_in, body_in, mime_type), find_corresponding_param("GET_someParam", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))

        return custom_processing

    def add_validate_params_handler(self, BODY_mime_type = None, GET_notRepeatable = None, GET_someParam = None, BODY_content = None):
        return Response_Element()

    def check_overriden(self):
        overriden = []

        for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
            this_method = getattr(self, method)
            base_method = getattr(resource_with_repeatable_params_post_Base, method)

            if this_method.__func__ is not base_method.__func__:
                overriden.append(method)

        return overriden

    def request_handler(self):
        return Response_Element()

