import datetime
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element

from RAMLFlask.Generated_Class_Base import Generated_Class_Base

from delegates import resp_validator_delegate

class Thread_Search():
    class Get_Base(Generated_Class_Base):
        

        def __init__(self, request, resp_t=(False, [{'body': 'text/plain', 'code': 501}, {'body': 'application/json', 'code': 200}, {'body': None, 'code': 400}, {'body': None, 'code': 500}])):
            self.req = request
            self.enforced_type = resp_t[0]
            self.resp_t = resp_t[1]

        def auth_handler(self):
            return Response_Element()

        def validate_params_handler(self):
            validations = []
            uri_in = self.req.view_args
            get_in = self.req.args
            body_in = self.req.data
            mime_type = self.req.mimetype

            # Validate URI paramters
            check = self.validate_request_parameter(validations, uri_in)
            if check.proceed == False:
                return check

            # Validate query string
            check = self.validate_query_string(validations, get_in)
            if check.proceed == False:
                return check

            # Validate query mime type and body
            check = self.validate_body_params(validations, body_in, mime_type)
            if check.proceed == False:
                return check

            cust_request = {}
            arguments = [{'type': 'BODY', 'name': 'mime_type'}, {'type': 'BODY', 'name': 'content'}]
            for arg in arguments:
                cust_request[arg['name']] = {'type': arg['type'], 'value': self.find_corresponding_param(arg['name'], arg['type'], uri_in, get_in, body_in, mime_type)}

            custom_processing = self.add_validate_params_handler(cust_request)

            return custom_processing

        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def check_overriden(self):
            overriden = []

            for method in ('auth_handler', 'validate_params_handler', '__init__', 'handle_request'):
                this_method = getattr(self, method)
                base_method = getattr(Thread_Search.Get_Base, method)

                if this_method.__func__ is not base_method.__func__:
                    overriden.append(method)

            return overriden

        def check_response_code(self, code):
            if self.enforced_type:
                codes = [i['code'] for i  in self.resp_t]
                if code in codes:
                    if resp_validator.validate(code, self.resp_t):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return True

        def request_handler(self):
            return Response_Element()

