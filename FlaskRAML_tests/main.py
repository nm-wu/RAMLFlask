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
    assert gen_class.__class__.__name__ == 'Generated_Class_Base'


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

def test_check_overridden():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).check_overriden()
    assert gen_class == []

def test_Handle_Request():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''
    gen_class = Generated_Class_Base(request).handle_request()
    assert gen_class == ('', 200)


def test_validate_request_parameter():
    from FlaskRAML.Generated_Class_Base import validate_request_parameter

    a = [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}}]
    b = {'resourceId': u'the_value'}

    corr_valid = validate_request_parameter(a, b)
    assert corr_valid.proceed == True
    assert corr_valid.response == ('', 200)

    b = {'random_thing': u'what'}
    wrong_valid = validate_request_parameter(a, b)
    assert wrong_valid.proceed == False
    assert wrong_valid.response == ('', 400)


def test_validate_query_string():
    from FlaskRAML.Generated_Class_Base import validate_query_string
    from werkzeug.datastructures import ImmutableMultiDict

    a = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Your value for some thing.', 'min_length': None, 'name': 'some_query_param', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'my value'}}]
    b = ImmutableMultiDict([('some_query_param', 'my value')])
    corr_valid = validate_query_string(a, b)
    assert corr_valid.proceed == True
    assert corr_valid.response == ('', 200)

    b = ImmutableMultiDict([('some_other_param', 'my value')])
    wrong_valid = validate_query_string(a, b)
    assert wrong_valid.proceed == False
    assert wrong_valid.response == ('', 400)


def test_validate_body_params():
    from FlaskRAML.Generated_Class_Base import validate_body_params

    input = {u'api_key': u'c4f820f0420a013ea143230c290fbf99'}
    mime_type = 'multipart/form-data'
    reqs = [{'source': 'get_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Your value for some thing.', 'min_length': None, 'name': 'some_query_param', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'my value'}}, {'source': 'body', 'validation': [{'mime-type': 'application/json', 'errors': [], 'params': [], 'example': {u'api_key': u'c4f820f0420a013ea143230c290fbf99'}, 'schema': None}, {'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'example': None, 'schema': None}, {'mime-type': 'multipart/form-data', 'errors': [], 'params': [{'source': 'body_param', 'validation': {'repeat': None, 'enum': None, 'minimum': None, 'desc': 'Your license key for the application. Please contact developer@nzpost.co.nz for a license key', 'min_length': None, 'name': 'API Key', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': 'c4f820f0420a013ea143230c290fbf99'}}], 'example': None, 'schema': None}]}]
    corr_valid = validate_body_params(reqs, input, mime_type)
    assert corr_valid.proceed == True
    assert corr_valid.response == ('', 200)

    mime_type = None
    wrong_valid = validate_body_params(reqs, input, mime_type)
    assert wrong_valid.proceed == True
    assert wrong_valid.response == ('', 200)

def test_check_response_code():
    from FlaskRAML.Generated_Class_Base import Generated_Class_Base
    request = ''

    assert Generated_Class_Base(request).check_response_code(200) == True
    assert Generated_Class_Base(request).check_response_code(400) == True
    assert Generated_Class_Base(request).check_response_code(500) == True
    assert Generated_Class_Base(request).check_response_code(999) == False


def test_find_corresponding_param():
    from FlaskRAML.Generated_Class_Base import find_corresponding_param
    from werkzeug.datastructures import ImmutableMultiDict

    assert find_corresponding_param('BODY_mime_type', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'mime'
    assert find_corresponding_param('URI_u_ex', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'uri'
    assert find_corresponding_param('GET_g_ex', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'get'
    assert find_corresponding_param('BODY_b_ex', {'u_ex': u'uri'}, ImmutableMultiDict([('g_ex', u'get'), ('other_value', u'wrong')]), 'request_body', 'mime') == 'request_body'


def test_perfrom_validation():
    from FlaskRAML.Generated_Class_Base import perform_validation

    name = 'chunk'
    value = 1
    validation = {'repeat': False, 'enum': None, 'minimum': 1, 'desc': 'Which page to display', 'min_length': None, 'name': 'chunk', 'default': None, 'pattern': None, 'required': True, 'maximum': 100, 'max_length': None, 'type': 'integer', 'example': 1}
    assert perform_validation(name, value, validation) == True

    value = 'asdf'
    assert perform_validation(name, value, validation) == False


# RAMLFlask Suite
def test_RAMLFlask_Instantiation():
    from FlaskRAML.RAMLFlask import Server

    server = Server("./example.raml")
    assert server != None


def test_create_sys_folder():
    import os.path
    import shutil
    from FlaskRAML.RAMLFlask import create_sys_folder

    create_sys_folder('test')
    assert os.path.isdir('./test/')
    assert os.path.isfile('./test/__init__.py')
    with file('./test/__init__.py') as f:
        assert f.read() == ''

    os.remove('./test/__init__.py')
    shutil.rmtree('./test')


def test_create_delegate():
    import os.path
    import shutil
    from FlaskRAML.RAMLFlask import create_delegate

    if not os.path.exists('./delegates'):
        os.makedirs('./delegates')

    name = 'test'
    del_type = 'Delegate_Test'
    file_name = './delegates/test_delegate.py'

    create_delegate(name, del_type)
    assert os.path.isfile(file_name)
    with file(file_name) as f:
        assert f.read() == 'from FlaskRAML.rsp_element import Response_Element\n\nclass Delegate_Test_Delegate(object):\n    """Delegation class"""\n\n    def handle_delegation(self, request):\n        return Response_Element()'

    os.remove(file_name)
    shutil.rmtree('./delegates')


def test_add_validation_elements():
    from FlaskRAML.RAMLFlask import add_validation_elements

    input_list = []

    val_type = 'uri_param'
    params = None
    assert add_validation_elements(val_type, params, input_list) == []

    val_type = 'get_param'
    params = None
    assert add_validation_elements(val_type, params, input_list) == []

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
    assert add_validation_elements(val_type, params,input_list) == [
        {'source': 'get_param', 'validation': {'repeat': '', 'enum': '', 'minimum': '', 'desc': '', 'min_length': '',
         'name': 'filter', 'default': '', 'pattern': '', 'required': '', 'maximum': '', 'max_length': '', 'type': '',
         'example': ''}}]


def test_create_file():
    import os.path
    import shutil
    from FlaskRAML.RAMLFlask import create_file

    if not os.path.exists('./creation_tests'):
        os.makedirs('./creation_tests')

    file_name ='./creation_tests/file_creation.py'
    create_file('./creation_tests/', 'file_creation.py', 'print \'abCD12$%&/()?\'')
    assert os.path.isfile(file_name)
    with file(file_name) as f:
        assert f.read() == 'print \'abCD12$%&/()?\''

    os.remove(file_name)
    shutil.rmtree('./creation_tests')


def test_raml_ver():
    from FlaskRAML.RAMLFlask import set_raml_version

    assert set_raml_version(1) == '/v1'
    assert set_raml_version(None) == ''

def test_generate_handler():
    from FlaskRAML.RAMLFlask import generate_handler
    assert generate_handler('test', []) == '    handler = generated_routes.' + 'test' + '_Base(request)\n'
    assert generate_handler('test2', [('hw_imports_test.test', 'test2')]) == '    handler = ' + 'hw_imports_test.test' + '.' + 'test2' + '(request)\n'


def test_generate_handwritten_imports():
    from FlaskRAML.RAMLFlask import generate_handwritten_imports

    assert generate_handwritten_imports('./hw_imports_test') == ['hw_imports_test.test_class']


def test_generate_handwritten_classes():
    from FlaskRAML.RAMLFlask import generate_handwritten_classes

    imports = ['hw_imports_test.test_class']
    assert  generate_handwritten_classes(imports) == [('hw_imports_test.test_class', 'Test_Class')]


def test_add_generated_classes():
    from FlaskRAML.RAMLFlask import add_generated_classes

    tmpl_vars = {'validation': [], 'return_val': 'return Response_Element()', 'resp_types': (False, set([])), 'class_name': 'Test_Class',
     'args_search': 'find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type)',
     'documentation': '"""get the first one"""\n', 'method': 'get', 'auth': 'return Response_Element()', 'args_list': 'self, BODY_mime_type = None, BODY_content = None'}

    output_valid = 'class Test_Class(Generated_Class_Base):\n'
    output_valid += '    \"\"\"get the first one\"\"\"\n\n\n'
    output_valid += '    def __init__(self, request, resp_t=(False, set([]))):\n'
    output_valid += '        self.req = request\n'
    output_valid += '        self.enforced_type = resp_t[0]\n'
    output_valid += '        self.resp_t = resp_t[1]\n\n'
    output_valid += '    def auth_handler(self):\n'
    output_valid += '        return Response_Element()\n\n'
    output_valid += '    def validate_params_handler(self):\n'
    output_valid += '        validations = []\n'
    output_valid += '        uri_in = self.req.view_args\n'
    output_valid += '        get_in = self.req.args\n'
    output_valid += '        body_in = self.req.data\n'
    output_valid += '        mime_type = self.req.mimetype\n\n'
    output_valid += '        # Validate URI paramters\n'
    output_valid += '        check = validate_request_parameter(validations, uri_in)\n'
    output_valid += '        if check.proceed == False:\n'
    output_valid += '            return check\n\n'
    output_valid += '        # Validate query string\n'
    output_valid += '        check = validate_query_string(validations, get_in)\n'
    output_valid += '        if check.proceed == False:\n'
    output_valid += '            return check\n\n'
    output_valid += '        # Validate query mime type and body\n'
    output_valid += '        check = validate_body_params(validations, body_in, mime_type)\n'
    output_valid += '        if check.proceed == False:\n'
    output_valid += '            return check\n\n'
    output_valid += '        custom_processing = self.add_validate_params_handler(find_corresponding_param("BODY_mime_type", uri_in, get_in, body_in, mime_type), find_corresponding_param("BODY_content", uri_in, get_in, body_in, mime_type))\n\n'
    output_valid += '        return custom_processing\n\n'
    output_valid += '    def add_validate_params_handler(self, BODY_mime_type = None, BODY_content = None):\n'
    output_valid += '        return Response_Element()\n\n'
    output_valid += '    def check_overriden(self):\n'
    output_valid += '        overriden = []\n\n'
    output_valid += '        for method in (\'auth_handler\', \'validate_params_handler\', \'__init__\', \'handle_request\'):\n'
    output_valid += '            this_method = getattr(self, method)\n'
    output_valid += '            base_method = getattr(Test_Class, method)\n\n'
    output_valid += '            if this_method.__func__ is not base_method.__func__:\n'
    output_valid += '                overriden.append(method)\n\n'
    output_valid += '        return overriden\n\n'
    output_valid += '    def request_handler(self):\n'
    output_valid += '        return Response_Element()\n\n'

    assert add_generated_classes(tmpl_vars) == output_valid


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


def test_open_old_dict():
    import os.path
    import shutil
    from FlaskRAML.RAMLFlask import open_old_dict

    if os.path.exists('./generated/'):
        shutil.rmtree('./generated/')
    os.makedirs('./generated/structures')

    d_type = 'valid'
    current_file = '20170203102229_valid.py'
    old_f = None
    assert open_old_dict(d_type, current_file, old_f) == None

    # --------------------------------------------

    new_file = open('./generated/structures/20170203102228_valid.py', 'w')
    dict_write = {'success_key': 'axcd12'}
    new_file.write(str(dict_write))
    new_file.close()

    dict = open_old_dict(d_type, current_file, old_f)
    assert dict['success_key'] == 'axcd12'

    # --------------------------------------------

    d_type = 'rtype'
    current_file = '20170203102229_rtype.py'
    assert open_old_dict(d_type, current_file, old_f) == None

    # --------------------------------------------

    new_file = open('./generated/structures/20170203102228_rtype.py', 'w')
    dict_write = {'success_key': '45ghzt'}
    new_file.write(str(dict_write))
    new_file.close()

    dict =  open_old_dict(d_type, current_file, old_f)

    assert dict['success_key'] == '45ghzt'

    shutil.rmtree('./generated/')


def test_open_new_dict():
    import os
    import shutil
    from FlaskRAML.RAMLFlask import open_new_dict

    if os.path.exists('./generated/'):
        shutil.rmtree('./generated/')
    os.makedirs('./generated/structures')

    d_type = 'valid'
    current_dict = {'current_dict': True}
    new_f = None
    assert open_new_dict(d_type, current_dict, new_f)['current_dict'] == True

    # --------------------------------------------

    d_type = 'valid'
    current_dict = {'current_dict': True}
    new_f = '1'

    new_file = open('./generated/structures/1_valid.py', 'w')
    dict_write = {'current_dict': False}
    new_file.write(str(dict_write))
    new_file.close()

    dict = open_new_dict(d_type, current_dict, new_f)
    assert dict['current_dict'] == False

    # --------------------------------------------

    d_type = 'rtype'
    current_dict = {'current_dict': True}
    new_f = None
    assert open_new_dict(d_type, current_dict, new_f)['current_dict'] == True

    # --------------------------------------------

    d_type = 'rtype'
    current_dict = {'current_dict': True}
    new_f = '1'

    new_file = open('./generated/structures/1_rtype.py', 'w')
    dict_write = {'current_dict': False}
    new_file.write(str(dict_write))
    new_file.close()


    assert open_new_dict(d_type, current_dict, new_f)['current_dict'] == False


    shutil.rmtree('./generated/')



def test_check_validations():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import check_validations

    old_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}
    new_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    check_validations(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] No changes compared to the previous version'

    #--------------------------------------------

    old_dict = None
    new_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    check_validations(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] No previous validations for comparison found'

    # --------------------------------------------

    old_dict = {'POST /resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}
    new_dict = {'POST /alignment/resource/{resourceId}': [{'source': 'uri_param', 'validation': {'repeat': False, 'enum': None, 'minimum': None, 'desc': 'Which resoure would you like to view', 'min_length': None, 'name': 'resourceId', 'default': None, 'pattern': None, 'required': True, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, 'class': 'resource_with_resource_id_post'}]}

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    check_validations(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] Routed added to the build: POST /alignment/resource/{resourceId}\n[INFO] Routed removed from the build: POST /resource/{resourceId}'


def test_populate_params():
    from FlaskRAML.RAMLFlask import populate_params

    new_res = [{'source': 'uri_param', 'validation': {'name': 'a'}}, {'source': 'get_param', 'validation': {'name': 'b'}}, {'source': 'body', 'validation':[{'name': 'c'}]}]
    old_res = [{'source': 'uri_param', 'validation': {'name': 'd'}}, {'source': 'get_param', 'validation': {'name': 'e'}}, {'source': 'body', 'validation':[{'name': 'f'}]}]
    res = populate_params(new_res, old_res)

    assert res[0] == [{'name': 'b'}]
    assert res[1] == [[{'name': 'c'}]]
    assert res[2] == [{'name': 'e'}]
    assert res[3] == [[{'name': 'f'}]]


def test_iterate_var_map():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import iterate_var_map

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    var_map = {}
    val = 'multipart/form-data'
    changed = iterate_var_map(var_map, val)
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

    out = StringIO()
    sys.stdout = out
    changed = iterate_var_map(var_map, val)
    output = out.getvalue().strip()

    assert output == '[INFO] The validation type someMultipartFormParamWithMultipleTypes was added to multipart/form-data'
    assert changed == True

    sys.stdout = oldstdout


def test_compare_get():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import compare_get

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    n_get = [{'min_length': None, 'repeat': True, 'name': 'someParam', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}, {'min_length': None, 'repeat': False, 'name': 'new_validation', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}]
    o_get = [{'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someParam', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, {'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}]
    assert compare_get(n_get, o_get) == True
    output = out.getvalue().strip()
    assert output == '[INFO] The query parameter notRepeatable was removed\n[INFO] The validation for query parameter someParam was changed: value of repeat was modified\n[INFO] The query parameter new_validation was added'

    out = StringIO()
    sys.stdout = out

    n_get = [{'min_length': None, 'repeat': False, 'name': 'someParam', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}, {'min_length': None, 'repeat': False, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': False, 'minimum': None, 'max_length': None, 'type': 'string', 'example': None, 'desc': None}]
    o_get = [{'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'someParam', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}, {'repeat': False, 'enum': None, 'minimum': None, 'desc': None, 'min_length': None, 'name': 'notRepeatable', 'default': None, 'pattern': None, 'required': False, 'maximum': None, 'max_length': None, 'type': 'string', 'example': None}]
    compare_get(n_get, o_get)
    assert compare_get(n_get, o_get) == False
    output = out.getvalue().strip()
    assert output == ''

    sys.stdout = oldstdout


def test_compare_body():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import compare_body

    oldstdout = sys.stdout

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

    compare_body(n_body, o_body)
    output = out.getvalue().strip()
    assert output == ''

    # --------------------------------------------

    n_body1 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None}]]

    out = StringIO()
    sys.stdout = out

    compare_body(n_body1, o_body)
    output = out.getvalue().strip()
    assert output == '[INFO] The body validation with Mime Type application/json was removed'
    sys.stdout = oldstdout

    # --------------------------------------------

    o_body1 = [[{'mime-type': 'application/x-www-form-urlencoded', 'errors': [], 'params':
                [{'source': 'body_param', 'validation': {'min_length': None, 'repeat': None, 'name': None, 'default': None, 'pattern': None,
                  'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None, 'type': 'string', 'example': 'Comment',
                  'desc': 'The name of the resource to create'}}, {'source': 'body_param', 'validation': {'min_length': None, 'repeat': None,
                  'name': None, 'default': None, 'pattern': None, 'enum': None, 'maximum': None, 'required': None, 'minimum': None, 'max_length': None,
                  'type': 'string', 'example': 'User-generated content pertinent to the associated blog post', 'desc': 'A description of the resource to create'}}],
                  'example': None, 'schema': None}]]

    out = StringIO()
    sys.stdout = out

    compare_body(n_body, o_body1)
    output = out.getvalue().strip()
    assert output == '[INFO] The body validation with Mime Type application/json was added'
    sys.stdout = oldstdout

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

    out = StringIO()
    sys.stdout = out

    compare_body(n_body2, o_body)
    output = out.getvalue().strip()
    assert output == '[INFO] The potential errors for the body validation of application/x-www-form-urlencoded have been changed'
    sys.stdout = oldstdout

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

    out = StringIO()
    sys.stdout = out
    compare_body(n_body3, o_body)
    output = out.getvalue().strip()
    assert output == '[INFO] The example for the body validation of application/x-www-form-urlencoded was changed'
    sys.stdout = oldstdout

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

    out = StringIO()
    sys.stdout = out
    compare_body(n_body4, o_body)
    output = out.getvalue().strip()
    assert output == '[INFO] The schema for the body validation of application/x-www-form-urlencoded was changed'
    sys.stdout = oldstdout

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

    out = StringIO()
    sys.stdout = out

    compare_body(n_body5, o_body)
    output = out.getvalue().strip()
    assert output == '[INFO] The validation type added_a_new_name was added to application/x-www-form-urlencoded'
    sys.stdout = oldstdout


def test_check_returnt():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import check_returnt

    oldstdout = sys.stdout

    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    new_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    check_returnt(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] No return type changes'

    # --------------------------------------------

    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    new_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201]), 'GET /even/another/resource': set([203, 201])}
    check_returnt(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] Return type GET /even/another/resource was added'

    # --------------------------------------------

    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201]), 'GET /even/another/resource': set([203, 201])}
    new_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    check_returnt(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] Return type GET /even/another/resource was removed'

    # --------------------------------------------

    #'Return type ' + a + ' was added to ' + comp
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': set([201]), 'HEAD /another/resource': set([203, 201])}
    new_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    check_returnt(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] Return type 203 was added to POST /resource/{resourceId}'

    # --------------------------------------------

    #'Return type ' + r + ' was removed from ' + comp
    out = StringIO()
    sys.stdout = out
    old_dict = {'POST /resource/{resourceId}': set([203, 201]), 'HEAD /another/resource': set([203, 201])}
    new_dict = {'POST /resource/{resourceId}': set([201]), 'HEAD /another/resource': set([203, 201])}
    check_returnt(old_dict, new_dict)
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] Return type 203 was removed from POST /resource/{resourceId}'


def test_info_print():
    import sys
    from StringIO import StringIO
    from FlaskRAML.RAMLFlask import info_print

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
    from FlaskRAML.RAMLFlask import warn_print

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
    from FlaskRAML.RAMLFlask import time_print

    out = StringIO()
    oldstdout = sys.stdout
    sys.stdout = out

    time_print('this is a test 12345!')

    output = out.getvalue().strip()
    assert output == '[TIME] this is a test 12345!'

    sys.stdout = oldstdout


def test_mock_request_init():
    from FlaskRAML.RAMLFlask import Mock_Request

    mr = Mock_Request('uri', 'get', 'body', 'mime')
    assert mr != None


# RAMLFlask Integration tests
def integration_tests():
    import os
    import sys
    from StringIO import StringIO
    import shutil
    from FlaskRAML.RAMLFlask import Server

    oldstdout = sys.stdout

    # Server instantiation
    server = Server('example.raml')
    assert isinstance(server, Server)

    # --------------------------------------------

    # Code generation


    out = StringIO()
    sys.stdout = out
    server.generate_code()
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    delegates = ['__init__.py', 'application_json_delegate.py', 'application_x_www_form_urlencoded_delegate.py', 'basic_auth_delegate.py',
                 'multipart_form_data_delegate.py', 'post_req_delegate.py','pre_req_delegate.py', 'text_plain_delegate.py']
    generated = ['__init__.py', 'generated_routes.py', 'structures']
    assert os.listdir('./delegates').sort() == delegates.sort()
    assert os.listdir('./generated').sort() == generated.sort()
    assert output == '[INFO] Starting route generation: 17 hw_imports_test'

    # --------------------------------------------

    # Route binding
    server.bind_routes()
    gen_dir = os.listdir('./generated')
    assert 'route_mappings.py' in gen_dir

    # --------------------------------------------

    # Static analysis
    out = StringIO()
    sys.stdout = out
    server.static_analysis()
    output = out.getvalue().strip()
    sys.stdout = oldstdout
    assert output == '[INFO] No previous validations for comparison found\n[INFO] No return type changes'

    # --------------------------------------------

    # Test analysis
    out = StringIO()
    sys.stdout = out
    server.test_analysis()
    output = out.getvalue().strip()
    sys.stdout = oldstdout

    comp = ['[INFO] Test of First_One_get_Base: SUCCESS', '[INFO] Test of First_One_put_Base: SUCCESS',
           '[INFO] Test of First_One_delete_Base: SUCCESS', '[INFO] Test of First_One_patch_Base: SUCCESS',
           '[INFO] Test of First_One_options_Base: SUCCESS', '[INFO] Test of First_One_trace_Base: SUCCESS',
           '[INFO] Test of First_One_connect_Base: SUCCESS', '[INFO] GET Parameter filter of resource resource_with_resource_id_get_Base does not have an example defined for testing',
           '[INFO] URI Parameter resourceId of resource resource_with_resource_id_get_Base does not have an example defined for testing[WARN] Test of resource_with_resource_id_get_Base: FAIL',
           '[INFO] URI Parameter resourceId of resource resource_with_resource_id_post_Base does not have an example defined for testing',
           '[INFO] BODY with schema application/x-www-form-urlencoded of resource resource_with_resource_id_post_Base does not have an example defined for testing',
           '[INFO] BODY with schema multipart/form-data of resource resource_with_resource_id_post_Base does not have an example defined for testing',
           '[WARN] Test of resource_with_resource_id_post_Base: FAIL', '[INFO] GET Parameter query of resource Cats_get_Base does not have an example defined for testing',
           '[INFO] Test of Cats_get_Base: SUCCESS', '[INFO] Test of Cats_head_Base: SUCCESS', '[INFO] Test of Cats_connect_Base: SUCCESS',
           '[INFO] Test of Resource_With_headers_get_Base: SUCCESS', '[INFO] Test of SO_SECURE_get_Base: SUCCESS',
           '[INFO] Test of First_One_with_method_level_traits_get_Base: SUCCESS', '',
           '[INFO] BODY with schema application/x-www-form-urlencoded of resource resource_with_form_and_multipart_form_parameters_get_Base does not have an example defined for testing',
           '[INFO] BODY with schema multipart/form-data of resource resource_with_form_and_multipart_form_parameters_get_Base does not have an example defined for testing',
           '[INFO] Test of resource_with_form_and_multipart_form_parameters_get_Base: SUCCESS',
           '[INFO] GET Parameter someParam of resource resource_with_repeatable_params_post_Base does not have an example defined for testing',
           '[INFO] GET Parameter notRepeatable of resource resource_with_repeatable_params_post_Base does not have an example defined for testing',
           '[INFO] BODY with schema application/x-www-form-urlencoded of resource resource_with_repeatable_params_post_Base does not have an example defined for testing',
           '[INFO] BODY with schema multipart/form-data of resource resource_with_repeatable_params_post_Base does not have an example defined for testing',
           '[INFO] Test of resource_with_repeatable_params_post_Base: SUCCESS']
    output = output.split('\n')

    assert output.sort() == comp.sort()

    # --------------------------------------------

    shutil.rmtree('./delegates')
    shutil.rmtree('./generated')