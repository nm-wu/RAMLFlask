import re
from flask import request
from delegates import pre_req_delegate, post_req_delegate
from RAMLFlask.rsp_element import Response_Element
from importlib import import_module

class Generated_Class_Base(object):
    """Base Class for generated classes"""

    def __init__(self, request, resp_t=(False, [{'code':200,'body':None}, {'code':400,'body':None}, {'code':500,'body':None}])):
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

    def post_req_handler(self, resp_value, resp_code, resp_headers=None):
        post_r_delegate = post_req_delegate.Post_Req_Delegate()


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
            codes = [i['code'] for i  in self.resp_t]
            if code in codes:
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
            if self.check_response_code(res_pre_req.code):
                return res_pre_req.create_response()
            else:
                exception = 'This return code should not be used: ' + str(res_pre_req.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_auth = self.auth_handler()
        if res_auth.proceed is False:
            if self.check_response_code(res_auth.code):
                return res_auth.create_response()
            else:
                exception = 'This return code should not be used: ' + str(res_auth.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_validate = self.validate_params_handler()
        if res_validate.proceed is False:
            if self.check_response_code(res_validate.code):
                return res_validate.create_response()
            else:
                exception = 'This return code should not be used: ' + str(res_validate.response.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        res_request = self.request_handler()
        if res_request.proceed is False:
            if self.check_response_code(res_request.code):
                return res_request.create_response()
            else:
                exception = 'This return code should not be used: ' + str(res_request.resp)
                raise Exception(exception)
                return 'Internal Server Error', 500

        self.post_req_handler(res_request.value, res_request.code, res_request.headers)

        if self.check_response_code(res_request.code):
            return res_request.create_response()
        else:
            exception = 'This return code should not be used: ' + str(res_request.resp)
            raise Exception(exception)
            return 'Internal Server Error', 500

        return res_post_req.resp


    def validate_request_parameter(self, reqs, input):
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
                    if self.perform_validation(selected_input, input[selected_input], r['validation']) == False:
                        status = False

        if status == True:
            return Response_Element()
        else:
            return Response_Element(False, ('', 400))

    def validate_query_string(self, reqs, input):
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
                    if self.perform_validation(selected_input, input[selected_input], r['validation']) == False:
                        status = False

        if status == True:
            return Response_Element()
        else:
            return Response_Element(False, ('', 400))


    def validate_body_params(self, reqs, input, mime_type):
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

    def find_corresponding_param(self, param, type, uri_inputs=None, get_inputs=None, body_inputs=None, mime_type=None):
        if param == 'mime_type':
            return mime_type

        if type == 'URI':
            return uri_inputs.get(param, None)

        if type == 'GET':
            return get_inputs.get(param, None)

        if type == 'BODY':
            return body_inputs


    def perform_validation(self, name, value, validation):
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