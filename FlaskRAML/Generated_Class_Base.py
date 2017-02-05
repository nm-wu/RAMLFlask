import re
from flask import request
from delegates import pre_req_delegate, post_req_delegate
from FlaskRAML.rsp_element import Response_Element
from importlib import import_module

class Generated_Class_Base(object):
    """Base Class for generated classes"""

    def __init__(self, request, resp_t=(True, [200, 400, 500])):
        self.req = request
        self.enforced_type = resp_t[0]
        self.resp_t = resp_t[1]

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
            if code in self.resp_t:
                return True
            else:
                return False
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
    find_param = "_".join(keyword[1:])

    if keyword[0] == 'URI':
        return uri_inputs.get(find_param, None)

    if keyword[0] == 'GET':
        return get_inputs.get(find_param, None)

    if keyword[0] == 'BODY':
        return body_inputs


def perform_validation(name, value, validation):
    v_type = type(value)
    if v_type == unicode or v_type == str:
        v_type = 'string'

    if v_type == int:
        v_type = 'integer'

    if validation['enum'] != None:
        match = False
        for e in validation['enum']:
            if e == value:
                match = True

        if match == False:
            return False

    if validation['type'] == v_type:
        if validation['type'] == 'string':
            if len(value) > validation['max_length'] and validation['max_length'] != None:
                return False

            if len(value) < validation['min_length'] and validation['min_length'] != None:
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