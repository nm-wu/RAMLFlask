from __future__ import absolute_import
import os
import sys

sys.path.insert(0,os.getcwd())

# Response Element
def test_Response_Element():
    from RAMLFlask.rsp_element import Response_Element
    rsp = Response_Element()
    assert rsp.proceed == True
    assert rsp.create_response() == ('', 200)


# Validation Element
def test_Validation_Element():
    from RAMLFlask.validation_element import Validation_Element
    valid = Validation_Element('get_param',
                               'name',
                               'desc',
                               'string',
                               ['a','b'],
                               '*',
                               1,
                               1,
                               None,
                               None,
                               'a',
                               False,
                               False,
                               'a')
    assert valid.dump() == {
        'source': 'get_param',
        'validation': {
        'enum': ['a', 'b'],
        'repeat': False,
        'minimum': None,
        'desc': 'desc',
        'min_length': 1,
        'name': 'name',
        'default': 'a',
        'pattern': '*',
        'required': False,
        'maximum': None,
        'max_length': 1,
        'type':'string',
        'example': 'a'
    }}


# Generated Class Base
def test_Class_Creation():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request)
    assert gen_class.__class__.__name__ == 'Generated_Class_Base'


def test_Base_Pre_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).pre_req_handler()
    assert gen_class.proceed == True
    assert gen_class.create_response() == ('', 200)

def test_Base_Auth_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).auth_handler()
    assert gen_class.proceed == True
    assert gen_class.create_response() == ('', 200)


def test_Base_Validate_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).validate_params_handler()
    assert gen_class.proceed == True
    assert gen_class.create_response() == ('', 200)


def test_Base_Addvalidate_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).add_validate_params_handler()
    assert gen_class.proceed == True
    assert gen_class.create_response() == ('', 200)


def test_Base_Request_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).request_handler()
    assert gen_class.proceed == True
    assert gen_class.create_response() == ('', 200)


def test_Base_Post_Positive_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).post_req_handler('',200)
    assert gen_class == None


def test_Base_Post_Negative_Handler():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).post_req_handler('', 400)
    assert gen_class == None


def test_check_overridden():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).check_overriden()
    assert gen_class == []

def test_Handle_Request():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).handle_request()
    assert gen_class == ('', 200)


def test_validate_request_parameter():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base

    request = ''
    cls = Generated_Class_Base(request)
    a = [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}]
    b = {'resourceId': u'the_value'}

    corr_valid = cls.validate_request_parameter(a, b)
    assert corr_valid.proceed == True
    assert corr_valid.create_response() == ('', 200)

    b = {'random_thing': u'what'}
    wrong_valid = cls.validate_request_parameter(a, b)
    assert wrong_valid.proceed == False
    assert wrong_valid.create_response() == ('', 400)


def test_validate_query_string():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    from werkzeug.datastructures import ImmutableMultiDict

    request = ''
    cls = Generated_Class_Base(request)
    a = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Your value for some thing.', 'min_length': None, 'name': 'some_query_param', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'my value'}}]
    b = ImmutableMultiDict([('some_query_param', 'my value')])
    corr_valid = cls.validate_query_string(a, b)
    assert corr_valid.proceed == True
    assert corr_valid.create_response() == ('', 200)

    b = ImmutableMultiDict([('some_other_param', 'my value')])
    wrong_valid = cls.validate_query_string(a, b)
    assert wrong_valid.proceed == False
    assert wrong_valid.create_response() == ('', 400)


def test_validate_body_params():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base

    request = ''
    cls = Generated_Class_Base(request)
    input = {u'api_key': u'c4f820f0420a013ea143230c290fbf99'}
    mime_type = 'multipart/form-data'
    reqs = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Your value for some thing.', 'min_length': None, 'name': 'some_query_param', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'my value'}}, {'source': 'body', 'validation': [{'mime-type': 'application/json', 'errors': [], 'params': [], 'example': {u'api_key': u'c4f820f0420a013ea143230c290fbf99'}, 'schema': None}, {'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'example': None, 'schema': None}, {'mime-type': 'multipart/form-data', 'errors': [], 'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'example': None, 'schema': None}]}]
    corr_valid = cls.validate_body_params(reqs, input, mime_type)
    assert corr_valid.proceed == True
    assert corr_valid.create_response() == ('', 200)

    mime_type = None
    wrong_valid = cls.validate_body_params(reqs, input, mime_type)
    assert wrong_valid.proceed == True
    assert wrong_valid.create_response() == ('', 200)

def test_check_response_code():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    request = ''

    instance = Generated_Class_Base(request, resp_t=(True, [{'code':200,'body':None}, {'code':400,'body':None}, {'code':500,'body':None}]))
    assert instance.check_response_code(200) == True
    assert instance.check_response_code(400) == True
    assert instance.check_response_code(500) == True
    assert instance.check_response_code(999) == False


def test_find_corresponding_param():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base
    from werkzeug.datastructures import ImmutableMultiDict

    request = ''
    cls = Generated_Class_Base(request)
    assert cls.find_corresponding_param('mime_type', 'BODY', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'mime'
    assert cls.find_corresponding_param('u_ex', 'URI', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'uri'
    assert cls.find_corresponding_param('g_ex', 'GET', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'get'
    assert cls.find_corresponding_param('b_ex', 'BODY', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'request_body'


def test_perfrom_validation():
    from RAMLFlask.Generated_Class_Base import Generated_Class_Base

    request = ''
    cls = Generated_Class_Base(request)
    name = 'chunk'
    value = 1
    validation = {'repeat': False, 'enum': None, 'minimum': 1, 'desc': 'Which page to display', 'min_length': None, 'name': 'chunk', 'default': None, 'pattern': None, 'required': True, 'maximum': 100, 'max_length': None, 'type': 'integer', 'example': 1}
    assert cls.perform_validation(name, value, validation) == True

    value = 'asdf'
    assert cls.perform_validation(name, value, validation) == False


# Printer functions
def test_info_print():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Printer import info_print

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    info_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[INFO] this is a test 12345!'

    sys.stdout = oldstdout


def test_warn_print():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Printer import warn_print

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    warn_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[WARN] this is a test 12345!'

    sys.stdout = oldstdout


def test_time_print():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Printer import time_print

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    time_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[TIME] this is a test 12345!'

    sys.stdout = oldstdout


# Name builder
def test_build_cls_name():
    from RAMLFlask.Name_Builder import build_cls_name

    assert build_cls_name('/resources', 'new resources') == 'new_resources'
    assert build_cls_name('/resources') == 'resources'
    assert build_cls_name('/{resources}') == 'resources'
    assert build_cls_name('/{resources}', '\\{}-$~=.:resource') == '_______resource'


# Mock Request
def test_mock_request_init():
    from RAMLFlask.Mock_Request import Mock_Request

    mr = Mock_Request('uri', 'get', 'body', 'mime')
    assert mr != None


# Generator Class
def test_gen_instantiation():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen != None


def test_directory_get_set():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    gen.generated_directory = './generated/'
    gen.routes_directory = './routes/'
    gen.delegates_directory = './delegates/'
    assert gen != None


def test_version_getter():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.current_file_name == ''


def test_get_test_res() :
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.test_res == []


def test_get_files():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.new_v_file == {}
    assert gen.new_r_file == {}


def test_generate_and_build():
    from RAMLFlask.Generator import Generator
    import shutil
    import os

    gen = Generator('example.raml')
    gen.generate_code()
    assert os.path.isdir('./generated')
    assert os.path.isdir('./delegates')
    assert os.path.isdir('./routes')
    assert os.path.exists('./generated/generated_routes.py')

    gen.bind_routes()
    assert os.path.exists('./generated/route_mappings.py')

    shutil.rmtree('./generated')
    shutil.rmtree('./delegates')
    shutil.rmtree('./routes')


def test_create_sys_folder():
    import os.path
    import shutil
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    gen.create_sys_folder('test')
    assert os.path.isdir('./test/')
    assert os.path.isfile('./test/__init__.py')
    with file('./test/__init__.py') as f:
        assert f.read() == ''

    os.remove('./test/__init__.py')
    shutil.rmtree('./test')


def test_add_validation_elements():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    input_list = []

    val_type = 'uri_param'
    params = None
    assert gen.add_validation_elements(val_type, params, input_list) == []

    val_type = 'get_param'
    params = None
    assert gen.add_validation_elements(val_type, params, input_list) == []

    class QueryParameter(object):
        def __init__(self, name):
            self.name = name
            self.desc = ''
            self.type = ''
            self.type = ''
            self.enum = ''
            self.pattern = ''
            self.min_length = ''
            self.max_length = ''
            self.minimum = ''
            self.maximum = ''
            self.example = ''
            self.repeat = ''
            self.required = ''
            self.default = ''
    val_type = 'get_param'
    params = [QueryParameter(name='filter')]
    assert gen.add_validation_elements(val_type, params,input_list) == [
        {'source': 'get_param', 'validation': {'repeat': '', 'enum': '', 'minimum': '', 'desc': '', 'min_length': '',
         'name': 'filter', 'default': '', 'pattern': '', 'required': '', 'maximum': '', 'max_length': '', 'type': '',
         'example': ''}}]


def test_generate_handler():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.generate_handler('test', 'get', []) == '    handler = generated_routes.' + 'test' + '.Get_Base(request)\n'
    assert gen.generate_handler('test2', 'get', ['hw_imports_test.test', 'test2.Get']) == '    handler = test2.Get(request)\n'


def test_generate_handwritten_imports():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert 'hw_imports_test.test_class' in gen.generate_handwritten_imports('./hw_imports_test')


def test_generate_handwritten_classes():
    from RAMLFlask.Generator import Generator

    imports = ['hw_imports_test.test_class']
    gen = Generator('example.raml')
    assert gen.generate_handwritten_classes(imports) == ["<class 'hw_imports_test.test_class.Test_Class'>.__class__", "<class 'hw_imports_test.test_class.Test_Class'>.__delattr__", "<class 'hw_imports_test.test_class.Test_Class'>.__dict__", "<class 'hw_imports_test.test_class.Test_Class'>.__doc__", "<class 'hw_imports_test.test_class.Test_Class'>.__format__", "<class 'hw_imports_test.test_class.Test_Class'>.__getattribute__", "<class 'hw_imports_test.test_class.Test_Class'>.__hash__", "<class 'hw_imports_test.test_class.Test_Class'>.__init__", "<class 'hw_imports_test.test_class.Test_Class'>.__module__", "<class 'hw_imports_test.test_class.Test_Class'>.__new__", "<class 'hw_imports_test.test_class.Test_Class'>.__reduce__", "<class 'hw_imports_test.test_class.Test_Class'>.__reduce_ex__", "<class 'hw_imports_test.test_class.Test_Class'>.__repr__", "<class 'hw_imports_test.test_class.Test_Class'>.__setattr__", "<class 'hw_imports_test.test_class.Test_Class'>.__sizeof__", "<class 'hw_imports_test.test_class.Test_Class'>.__str__", "<class 'hw_imports_test.test_class.Test_Class'>.__subclasshook__", "<class 'hw_imports_test.test_class.Test_Class'>.__weakref__", "<class 'hw_imports_test.test_class.Test_Class'>.a_method"]


def test_raml_ver():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.set_raml_version(1) == '/v1'
    assert gen.set_raml_version(None) == ''


def test_create_delegate():
    import os.path
    import shutil
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    if not os.path.exists('./delegates'):
        os.makedirs('./delegates')

    name = 'test'
    del_type = 'Delegate_Test'
    file_name = './delegates/test_delegate.py'

    gen.create_delegate(name, del_type)
    assert os.path.isfile(file_name)
    with file(file_name) as f:
        assert f.read() == 'from RAMLFlask.rsp_element import Response_Element\n\nclass Delegate_Test_Delegate(object):\n    """Delegation class"""\n\n    def handle_delegation(self, request):\n        return Response_Element()'

    os.remove(file_name)
    shutil.rmtree('./delegates')


def test_create_file():
    import os.path
    import shutil
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    if not os.path.exists('./creation_tests'):
        os.makedirs('./creation_tests')

    file_name ='./creation_tests/file_creation.py'
    gen.create_file('./creation_tests/', 'file_creation.py', 'print \'abCD12$%&/()?\'')
    assert os.path.isfile(file_name)
    with file(file_name) as f:
        assert f.read() == 'print \'abCD12$%&/()?\''

    os.remove(file_name)
    shutil.rmtree('./creation_tests')



def test_create_valid():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    c_el = {
        'displayName': 'a',
        'description': 'b',
        'type': 'c',
        'enum': 'd',
        'pattern': 'e',
        'min_length': 'f',
        'max_length': 'g',
        'minimum': 'h',
        'maximum': 'i',
        'example': 'j',
        'repeat': 'k',
        'required': 'l',
        'default': 'm'
    }
    ve = gen.create_valid(c_el)

    assert ve.source == 'body_param'
    assert ve.name == 'a'
    assert ve.desc == 'b'
    assert ve.val_type == 'c'
    assert ve.enum == 'd'
    assert ve.pattern == 'e'
    assert ve.min_length == 'f'
    assert ve.max_length == 'g'
    assert ve.minimum == 'h'
    assert ve.maximum == 'i'
    assert ve.example == 'j'
    assert ve.repeat == 'k'
    assert ve.required == 'l'
    assert ve.default == 'm'

    del c_el['displayName']
    ve = gen.create_valid(c_el, 'x')
    assert ve.source == 'body_param'
    assert ve.name == 'x'
    assert ve.desc == 'b'
    assert ve.val_type == 'c'
    assert ve.enum == 'd'
    assert ve.pattern == 'e'
    assert ve.min_length == 'f'
    assert ve.max_length == 'g'
    assert ve.minimum == 'h'
    assert ve.maximum == 'i'
    assert ve.example == 'j'
    assert ve.repeat == 'k'
    assert ve.required == 'l'
    assert ve.default == 'm'


def test_get_args():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    vb = []
    x = gen.get_args(vb)
    assert gen.get_args(vb) == [{'type': 'BODY', 'name': 'mime_type'}, {'type': 'BODY', 'name': 'content'}]

    vb.append({'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view',
                'min_length': None, 'name': 'uri_val', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}})
    vb.append({'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'get_val',
                'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}})
    vb.append({'source': 'body', 'validation': [{'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create',
                'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}],
                'errors': [], 'mime-type': 'application/x-www-form-urlencoded', 'example': None, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {
                'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None,
                'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}], 'errors': [], 'mime-type': 'multipart/form-data', 'example': None, 'schema': None}]})

    assert gen.get_args(vb) == [{'type': 'BODY', 'name': 'mime_type'}, {'type': 'BODY', 'name': 'content'}, {'type': 'URI', 'name': 'uri_val'}, {'type': 'GET', 'name': 'get_val'}]


def test_add_generated_classes():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    tmpl_vars = {'validation': [], 'return_val': 'return Response_Element()', 'resp_types': (False, set([])), 'class_name': 'Test_Class',
     'args_search': [{'type': 'BODY', 'name': 'mime_type'}, {'type': 'BODY', 'name': 'content'}],
     'documentation': '"""get the first one"""\n', 'method': 'get', 'auth': 'return Response_Element()'}

    output_valid = '    class Test_Class(Generated_Class_Base):\n'
    output_valid += '        \"\"\"get the first one\"\"\"\n\n\n'
    output_valid += '        def __init__(self, request, resp_t=(False, set([]))):\n'
    output_valid += '            self.req = request\n'
    output_valid += '            self.enforced_type = resp_t[0]\n'
    output_valid += '            self.resp_t = resp_t[1]\n\n'
    output_valid += '        def auth_handler(self):\n'
    output_valid += '            return Response_Element()\n\n'
    output_valid += '        def validate_params_handler(self):\n'
    output_valid += '            validations = []\n'
    output_valid += '            uri_in = self.req.view_args\n'
    output_valid += '            get_in = self.req.args\n'
    output_valid += '            body_in = self.req.data\n'
    output_valid += '            mime_type = self.req.mimetype\n\n'
    output_valid += '            # Validate URI paramters\n'
    output_valid += '            check = self.validate_request_parameter(validations, uri_in)\n'
    output_valid += '            if check.proceed == False:\n'
    output_valid += '                return check\n\n'
    output_valid += '            # Validate query string\n'
    output_valid += '            check = self.validate_query_string(validations, get_in)\n'
    output_valid += '            if check.proceed == False:\n'
    output_valid += '                return check\n\n'
    output_valid += '            # Validate query mime type and body\n'
    output_valid += '            check = self.validate_body_params(validations, body_in, mime_type)\n'
    output_valid += '            if check.proceed == False:\n'
    output_valid += '                return check\n\n'
    output_valid += '            cust_request = {}\n'
    output_valid += '            arguments = [{\'type\': \'BODY\', \'name\': \'mime_type\'}, {\'type\': \'BODY\', \'name\': \'content\'}]\n'
    output_valid += '            for arg in arguments:\n'
    output_valid += '                cust_request[arg[\'name\']] = {\'type\': arg[\'type\'], \'value\': self.find_corresponding_param(arg[\'name\'], arg[\'type\'], uri_in, get_in, body_in, mime_type)}\n\n'
    output_valid += '            custom_processing = self.add_validate_params_handler(cust_request)\n\n'
    output_valid += '            return custom_processing\n\n'
    output_valid += '        def add_validate_params_handler(self, cust_request):\n'
    output_valid += '            return Response_Element()\n\n'
    output_valid += '        def check_overriden(self):\n'
    output_valid += '            overriden = []\n\n'
    output_valid += '            for method in (\'auth_handler\', \'validate_params_handler\', \'__init__\', \'handle_request\'):\n'
    output_valid += '                this_method = getattr(self, method)\n'
    output_valid += '                base_method = getattr(.Test_Class, method)\n\n'
    output_valid += '                if this_method.__func__ is not base_method.__func__:\n'
    output_valid += '                    overriden.append(method)\n\n'
    output_valid += '            return overriden\n\n'
    output_valid += '        def check_response_code(self, code):\n'
    output_valid += '            if self.enforced_type:\n'
    output_valid += '                codes = [i[\'code\'] for i  in self.resp_t]\n'
    output_valid += '                if code in codes:\n'
    output_valid += '                    if resp_validator.validate(code, self.resp_t):\n'
    output_valid += '                        return True\n'
    output_valid += '                    else:\n'
    output_valid += '                        return False\n'
    output_valid += '                else:\n'
    output_valid += '                    return False\n'
    output_valid += '            else:\n'
    output_valid += '                return True\n\n'
    output_valid += '        def request_handler(self):\n'
    output_valid += '            return Response_Element()\n\n'

    assert gen.add_generated_classes(tmpl_vars) == output_valid


def test_generate_base_implementation():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    assert gen.generate_base_implementation() != ''


def test_add_imports():
    from RAMLFlask.Generator import Generator

    gen = Generator('example.raml')
    gen_imports = gen.add_imports()
    comp_string = 'import datetime\nfrom collections import OrderedDict\nfrom delegates import basic_auth_delegate\n\nfrom RAMLFlask.rsp_element import Response_Element\n\nfrom RAMLFlask.Generated_Class_Base import Generated_Class_Base\n\nfrom delegates import resp_validator_delegate\n\n'
    assert gen_imports == comp_string


def test_create_delegates_code():
    from RAMLFlask.Generator import Generator
    import shutil
    import os

    os.makedirs('./delegates')
    gen = Generator('example.raml')
    gen.create_delegates_code()
    assert os.path.isfile('./delegates/basic_auth_delegate.py')
    assert os.path.isfile('./delegates/post_req_delegate.py')
    assert os.path.isfile('./delegates/pre_req_delegate.py')
    assert os.path.isfile('./delegates/text_plain_delegate.py')
    shutil.rmtree('./delegates')


def test_export_dicts():
    from RAMLFlask.Generator import Generator
    import shutil
    import os

    os.makedirs('./generated/structures')
    gen = Generator('example.raml')
    gen.export_dicts()
    assert len(os.listdir('./generated/structures/')) == 2
    shutil.rmtree('./generated')


# Comparison class
def test_comp_instantiation():
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()
    assert comp != None


def test_comp_set_and_get():
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    comp.current_version = 'a'
    comp.test_res = ['a']
    comp.new_v_file = 'b'
    comp.new_r_file = 'c'
    comp.old_v_file = 'd'
    comp.old_r_file = 'e'
    assert comp != None


def test_test_analysis():
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()
    comp.generated_directory = './gen_test'

    one_element = {
        'validation': [],
        'name': 'Streaming.Get_Base'
    }
    comp.test_res = []

    comp.test_res.append(one_element)
    comp_list = [('INFO', 'Test of Streaming.Get_Base: SUCCESS')]

    assert comp.test_analysis() == comp_list


def test_open_old_dict():
    import os.path
    import shutil
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()
    comp.generated_directory = './generated/'

    if os.path.exists('./generated/'):
        shutil.rmtree('./generated/')
    os.makedirs('./generated/structures')

    d_type = 'valid'
    current_file = '20170513150945_valid.py'
    old_f = None
    assert comp.open_old_dict(d_type, current_file, old_f) == None

    # --------------------------------------------

    new_file = open('./generated/structures/20170513150948_valid.py', 'w')
    dict_write = {'success_key': 'axcd12'}
    new_file.write(str(dict_write))
    new_file.close()

    dict = comp.open_old_dict(d_type, current_file, old_f)
    assert dict['success_key'] == 'axcd12'

    # --------------------------------------------

    d_type = 'rtype'
    current_file = '20170513150945_rtype.py'
    assert comp.open_old_dict(d_type, current_file, old_f) == None

    # --------------------------------------------

    new_file = open('./generated/structures/20170513150948_rtype.py', 'w')
    dict_write = {'success_key': '45ghzt'}
    new_file.write(str(dict_write))
    new_file.close()

    dict = comp.open_old_dict(d_type, current_file, old_f)
    assert dict['success_key'] == '45ghzt'

    shutil.rmtree('./generated/')


def test_open_new_dict():
    import os
    import shutil
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()
    comp.generated_directory = '/generated'

    if os.path.exists('./generated/'):
        shutil.rmtree('./generated/')
    os.makedirs('./generated/structures')

    d_type = 'valid'
    current_dict = {'current_dict': True}
    new_f = None
    assert comp.open_new_dict(d_type, current_dict, new_f)['current_dict'] == True

    # --------------------------------------------

    d_type = 'valid'
    current_dict = {'current_dict': True}
    new_f = '1'

    new_file = open('./generated/structures/1_valid.py', 'w')
    dict_write = {'current_dict': False}
    new_file.write(str(dict_write))
    new_file.close()

    dict = comp.open_new_dict(d_type, current_dict, new_f)
    assert dict['current_dict'] == False

    # --------------------------------------------

    d_type = 'rtype'
    current_dict = {'current_dict': True}
    new_f = None
    assert comp.open_new_dict(d_type, current_dict, new_f)['current_dict'] == True

    # --------------------------------------------

    d_type = 'rtype'
    current_dict = {'current_dict': True}
    new_f = '1'

    new_file = open('./generated/structures/1_rtype.py', 'w')
    dict_write = {'current_dict': False}
    new_file.write(str(dict_write))
    new_file.close()


    assert comp.open_new_dict(d_type, current_dict, new_f)['current_dict'] == False


    shutil.rmtree('./generated/')


def test_check_validations():
    """
    This also tests static_valid_analysis
    """
    import sys
    from StringIO import StringIO
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    old_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}
    new_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    comp.check_validations(old_dict, new_dict)
    assert comp.dump_output() == ['No changes compared to the previous version']

    #--------------------------------------------

    old_dict = None
    new_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    comp.check_validations(old_dict, new_dict)
    assert comp.dump_output() == ['No previous validations for comparison found']

    # --------------------------------------------

    old_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}
    new_dict = {'POST /alignment/resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    comp.check_validations(old_dict, new_dict)
    assert comp.dump_output() == ['Routed added to the build: POST /alignment/resource/{resourceId}', 'Routed removed from the build: POST /resource/{resourceId}']


def test_populate_params():
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    new_res = [{'source': 'uri_param', 'validation': {'name': 'a'}}, {'source': 'get_param', 'validation': {'name': 'b'}}, {'source': 'body', 'validation':[{'name': 'c'}]}]
    old_res = [{'source': 'uri_param', 'validation': {'name': 'd'}}, {'source': 'get_param', 'validation': {'name': 'e'}}, {'source': 'body', 'validation':[{'name': 'f'}]}]
    res = comp.populate_params(new_res, old_res)

    assert res[0] == [{'name': 'b'}]
    assert res[1] == [[{'name': 'c'}]]
    assert res[2] == [{'name': 'e'}]
    assert res[3] == [[{'name': 'f'}]]


def test_iterate_var_map():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    var_map = {}
    val = 'multipart/form-data'
    changed = comp.iterate_var_map(var_map, val)
    output = out.getvalue().strip()
    assert output == ''
    assert changed == False

    var_map = {'someMultipartFormParamWithMultipleTypes': [
        {'repeat': [False, True], 'enum': [None, None], 'minimum': [None, None], 'desc': [None, None], 'min_length': [None, None], 'default': [None, None], 'pattern': [None, None], 'required': [None, None], 'maximum': [None, None], 'max_length': [None, None], 'type': ['file', 'string'], 'example': [None, None]},
        {'repeat': [None, True], 'enum': [None, None], 'minimum': [None, None], 'desc': [None, None], 'min_length': [None, None], 'default': [None, None], 'pattern': [None, None], 'required': [None, None], 'maximum': [None, None], 'max_length': [None, None], 'type': ['file', 'string'], 'example': [None, None]}
       ],
        None: [
        {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'file', 'example': None},
        {'repeat': True, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'file', 'example': None}
       ]}

    changed = comp.iterate_var_map(var_map, val)

    assert comp.dump_output() == ['The validation type someMultipartFormParamWithMultipleTypes was added to multipart/form-data']
    assert changed == True

    sys.stdout = oldstdout

def test_compare_get():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    n_get = [{'min_length': None, 'repeat': True, 'name': 'someParam', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}, {'min_length': None, 'repeat': False, 'name': 'new_validation', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}]
    o_get = [{'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someParam', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, {'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}]
    assert comp.compare_get(n_get, o_get) == True
    assert comp.dump_output() == ['The query parameter notRepeatable was removed', 'The validation for query parameter someParam was changed: value of repeat was modified', 'The query parameter new_validation was added']

    n_get = [{'min_length': None, 'repeat': False, 'name': 'someParam', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}, {'min_length': None, 'repeat': False, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}]
    o_get = [{'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someParam', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, {'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}]
    comp.compare_get(n_get, o_get)
    assert comp.compare_get(n_get, o_get) == False
    assert comp.dump_output() == []


def test_compare_body():
    import sys
    from StringIO import StringIO
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    out = StringIO()
    sys.stdout = out
    n_body = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]
    o_body = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]

    comp.compare_body(n_body, o_body)
    assert comp.dump_output() == []

    # --------------------------------------------

    n_body1 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None}]]

    comp.compare_body(n_body1, o_body)
    assert comp.dump_output() == ['The body validation with Mime Type application/json was removed']

    # --------------------------------------------

    o_body1 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None}]]

    comp.compare_body(n_body, o_body1)
    assert comp.dump_output() == ['The body validation with Mime Type application/json was added']

    # --------------------------------------------

    n_body2 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': ['test'], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]

    comp.compare_body(n_body2, o_body)
    assert comp.dump_output() == ['The potential errors for the body validation of application/x-www-form-urlencoded have been changed']

    # --------------------------------------------

    n_body3 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': 'A new example for this mime-type', 'schema': None},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]

    comp.compare_body(n_body3, o_body)
    assert comp.dump_output() == ['The example for the body validation of application/x-www-form-urlencoded was changed']

    # --------------------------------------------

    n_body4 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': 'xx-xxxx-xxxx'},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]

    comp.compare_body(n_body4, o_body)
    assert comp.dump_output() == ['The schema for the body validation of application/x-www-form-urlencoded was changed']

    # --------------------------------------------

    n_body5 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': 'added_a_new_name', 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None},
               {'mime-type': 'application/json', 'errors': [], 'params':
                [{'source': 'body_param',
                  'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment', 'desc': 'The name of the resource to create'}},
                  {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None,
                  'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'User-generated content pertinent to the associated blog post',
                  'desc': 'A description of the resource to create'}}], 'example': None, 'schema': None}]]

    comp.compare_body(n_body5, o_body)
    assert comp.dump_output() == ['The validation type added_a_new_name was added to application/x-www-form-urlencoded']


def test_check_returnt():
    """
    This also tests static_rtype_analysis
    """
    import sys
    from StringIO import StringIO
    from RAMLFlask.Comparison import Comparison

    comp = Comparison()

    old_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    new_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    comp.check_returnt(old_dict, new_dict)
    assert comp.dump_output() == ['No return type changes']

    # --------------------------------------------

    comp = Comparison()
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    new_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}, {'body': None, 'code': 500}]}
    comp.check_returnt(old_dict, new_dict)

    assert comp.dump_output() == ['Return type 500 was added']

    # --------------------------------------------

    comp = Comparison()
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    new_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}, {'body': 'text/plain', 'code': 200}]}
    comp.check_returnt(old_dict, new_dict)


    assert comp.dump_output() == ["Return type 200 was modified: from [\'application/json\'] to [\'application/json\', \'text/plain\']"]

    # --------------------------------------------

    comp = Comparison()
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    new_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}],
                'POST /new_resource': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    comp.check_returnt(old_dict, new_dict)

    assert comp.dump_output() == ['Return type POST /new_resource was added']

    # --------------------------------------------

    comp = Comparison()
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}],
                'POST /new_resource': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    new_dict = {'POST /resource/{resourceId}': [{'body': None, 'code': 401}, {'body': 'application/json', 'code': 200}]}
    comp.check_returnt(old_dict, new_dict)

    assert comp.dump_output() == ['Return type POST /new_resource was removed']

    # --------------------------------------------
