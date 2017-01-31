from __future__ import absolute_import

# Response Element
def test_Response_Element():
    from FlaskRAML.rsp_element import Response_Element
    rsp = Response_Element()
    assert rsp.proceed == True
    assert rsp.response == ('', 200)


# Validation Element
def test_Validation_Element():
    from FlaskRAML.validation_element import Validation_Element
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
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request)
    assert True
    #TODO: finish


def test_Base_Pre_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).pre_req_handler()
    assert gen_class.proceed == True
    assert gen_class.response == ('', 200)

def test_Base_Auth_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).auth_handler()
    assert gen_class.proceed == True
    assert gen_class.response == ('', 200)


def test_Base_Validate_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).validate_params_handler()
    assert gen_class.proceed == True
    assert gen_class.response == ('', 200)


def test_Base_Addvalidate_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).add_validate_params_handler()
    assert gen_class.proceed == True
    assert gen_class.response == ('', 200)


def test_Base_Request_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).request_handler()
    assert gen_class.proceed == True
    assert gen_class.response == ('', 200)


def test_Base_Post_Positive_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).post_req_handler(('', 200))
    assert gen_class.proceed == False
    assert gen_class.response == ('', 200)

def test_Base_Post_Negative_Handler():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).post_req_handler(('', 400))
    assert gen_class.proceed == False
    assert gen_class.response == ('', 400)

def test_Overridden_Check():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).check_overriden()
    assert gen_class == []


def test_Handle_Request():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    import flask

# TODO: test validate_request_parameter
# TODO: test validate_query_string
# TODO: test validate_body_params


# RAMLFlask Suite
def test_RAMLFlask_Instantiation():
    from FlaskRAML.RAMLFlask import Server

    server = Server("./example.raml")
    assert server != None

#TODO: test server/generate code
#TODO: test server/bind routes
#TODO: test server/static analysis
#TODO: test server/analysis via test
#TODO: test server/server start

#TODO: test create_sys_folder
#TODO: test create_delegate

#TODO: test add_validation_elements

#TODO: test create_file

def test_raml_ver():
    from FlaskRAML.RAMLFlask import set_raml_version

    assert set_raml_version(1) == '/v1'
    assert set_raml_version(None) == ''

def test_generate_handler():
    from FlaskRAML.RAMLFlask import generate_handler
    assert generate_handler('test', []) == '    handler = generated_routes.' + 'test' + '_Base(request)\n'
    assert generate_handler('test2', [('routes.test', 'test2')]) == '    handler = ' + 'routes.test' + '.' + 'test2' + '(request)\n'

#TODO: test generate_handwritten imports

#TODO: test generate_handwritten_classes

#TODO: test add_generated_classes

def test_get_args():
    from FlaskRAML.RAMLFlask import get_args

    vb = []
    assert get_args(vb) == ['BODY_mime_type', 'BODY_content']

    vb.append({'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view',
                'min_length': None, 'name': 'uri_val', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}})
    vb.append({'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'get_val',
                'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}})
    vb.append({'source': 'body', 'validation': [{'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create',
                'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}],
                'errors': [], 'mime-type': 'application/x-www-form-urlencoded', 'example': None, 'schema': None}, {'params': [{'source': 'body_param', 'validation': {
                'repeat': None, 'enum': None, 'minimum': None, 'desc': 'The name of the resource to create', 'min_length': None, 'name': None, 'default': None, 'pattern': None, 'required': None,
                'maximum': None, 'max_length': None, 'type': 'string', 'example': 'Comment'}}], 'errors': [], 'mime-type': 'multipart/form-data', 'example': None, 'schema': None}]})

    assert get_args(vb) == ['BODY_mime_type', 'GET_get_val', 'URI_uri_val', 'BODY_content']


def test_create_valid():
    from FlaskRAML.RAMLFlask import create_valid

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
    ve = create_valid(c_el)

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
    ve = create_valid(c_el, 'x')
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


def test_build_cls_name():
    from FlaskRAML.RAMLFlask import build_cls_name

    assert build_cls_name('/resources', 'get', 'new resources') == 'new_resources_get'
    assert build_cls_name('/resources', 'get') == 'resources_get'
    assert build_cls_name('/{resources}', 'get') == 'resources_get'
    assert build_cls_name('/{resources}', 'get', '\\{}-$~=.:resource') == '_________resource_get'

#TODO: test open_old_dict

#TODO: test open_new_dict

#TODO: test check_validations

#TODO: test populate_params

#TODO: test iterate_var_map

#TODO: test compare_get

#TODO: test compare_body

#TODO: test check_returnt

def test_info_print():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import info_print

    out = StringIO()
    sys.stdout = out

    info_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[INFO] this is a test 12345!'

def test_warn_print():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import warn_print

    out = StringIO()
    sys.stdout = out

    warn_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[WARN] this is a test 12345!'

def test_time_print():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import time_print

    out = StringIO()
    sys.stdout = out

    time_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[TIME] this is a test 12345!'

def test_mock_request_init():
    from FlaskRAML.RAMLFlask import Mock_Request

    mr = Mock_Request('uri', 'get', 'body', 'mime')
    assert mr != None