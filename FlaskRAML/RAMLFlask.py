import os
import jinja2
import ramlfications
import pyclbr
import re
import copy
from flask import Flask
from FlaskRAML.validation_element import Validation_Element
from pathlib2 import Path
from importlib import import_module
from werkzeug.datastructures import ImmutableMultiDict
import time
import datetime
from collections import OrderedDict

class Server:
    generated_dir = './generated/'
    routes_dir = './routes/'
    delegates_dir = './delegates/'

    def __init__(self, raml_file, return_success=True, enforce_resp=False):
        self.RAML_FILE = raml_file
        CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print dir_path
        self.raml = ramlfications.parse(self.RAML_FILE, CONFIG_FILE)

        # Allows to determine whether base class responses will return success or error messages
        self.rs = return_success

        # Allows to set if return parameters are enforced
        self.enforce_resp = enforce_resp

        # Resources to test
        self.test_res = []

        # Creates the basic Flask app
        self.app = Flask(__name__)

        # Initializes the list of mime types
        self.mime_types = []

        # Initializes the placeholder for comparisons
        self.file_name = ''
        self.file_name2 = ''
        self.new_dict = {}
        self.new_dict2 = {}

    def generate_code(self):

        # Create directories for the generated, and handwritten routes, as well as for the delegates
        create_sys_folder(self.generated_dir)
        create_sys_folder(self.routes_dir)
        create_sys_folder(self.delegates_dir)

        # Add content to the generated classes
        generated_classes = ''

        generated_classes += 'import datetime\n'
        generated_classes += 'from collections import OrderedDict\n'

        if self.raml.security_schemes != None:
            for sec_scheme in self.raml.security_schemes:
                generated_classes += 'from delegates import ' + sec_scheme.name + '_auth_delegate' + '\n\n'

        for mt in self.mime_types:
            generated_classes += 'from delegates import ' + mt + '_delegate' + '\n\n'

        # Read base class and add it to generated file
        fn = os.path.join(os.path.dirname(__file__), 'Generated_Class_Base.py')
        generated_classes += Path(fn).read_text() + '\n'

        # Print resource count
        info_print('Starting route generation: ' + str(len(self.raml.resources)) + ' routes')

        # Iterate over all resources to generate automatic base implementations
        for res in self.raml.resources:
            # Add security delegates
            if res.security_schemes is None:
                security = 'return Response_Element()'
            else:
                for sec_scheme in res.security_schemes:
                    security = 'a_delegate = ' + sec_scheme.name + '_auth_delegate.' + sec_scheme.name.capitalize() + '_Auth_Delegate() \n'
                    security += '        a_delegate.handle_delegation(request)  \n'
                    security += '        return Response_Element()'

            # Query parameter e.g. ?x=1
            validation_builder = add_validation_elements('get_param', res.query_params, [])

            # URI parameter in the base URI
            validation_builder = add_validation_elements('uri_param', res.uri_params, validation_builder)

            # Form parameter with properties defined by the RAML specifications named paramter section. Example:
            # curl -X POST https://api.com/foo/bar -d baz=123 where baz is the Form Parameter name.
            #validation_builder = add_validation_elements('body_param', res.form_params, validation_builder)

            # Body of the request
            if res.body is not None:
                bodies = {'source': 'body', 'validation': []}
                c = 0
                for i in res.body:
                    self.mime_types.append(i.__dict__['mime_type'])
                    bodies['validation'].append({
                        'mime-type': i.__dict__['mime_type'],
                        'schema': i.__dict__['schema'],
                        'errors': i.__dict__['errors'],
                        'example': i.__dict__['example'],
                        'params': []
                    })

                    if i.__dict__['form_params'] != None:
                        for x in i.__dict__['form_params']:
                            current_el = i.__dict__['form_params'][x]
                            if type(current_el) is list:
                                intermediate = []
                                for a in range(0,len(current_el)):
                                    valid = create_valid(current_el[a], x)
                                    intermediate.append(valid.dump())
                                bodies['validation'][c]['params'].append(intermediate)

                            else:
                                valid = create_valid(current_el)
                                bodies['validation'][c]['params'].append(valid.dump())
                    c += 1

                validation_builder.append(bodies)

            cls_name = build_cls_name(res.path, res.method, res.display_name) + '_Base'

            if res.method != None:
                self.test_res.append({'name': cls_name, 'validation': validation_builder})

            vb = copy.deepcopy(validation_builder)
            for i in vb:
                i['class'] = build_cls_name(res.path, res.method, res.display_name)

            if res.method != None:
                self.new_dict[res.method.upper() + ' ' + res.path] = vb

            args_list = get_args(validation_builder)
            args_search = copy.deepcopy(args_list)

            for idx in range(len(args_list)):
                args_list[idx] += ' = None'
            args_list.insert(0, 'self')

            args_list = ", ".join(args_list)

            for idx in range(len(args_search)):
                args_search[idx] = 'find_corresponding_param(\"' + args_search[idx] + '\", uri_in, get_in, body_in, mime_type)'
            args_search = ", ".join(args_search)

            # Calculate the supported request types
            supported_types = [200, 400, 500]
            if res.responses != None:
                for resp_c in res.responses:
                    if resp_c.method == res.method:
                        supported_types.append(resp_c.code)

            supported_types = set(supported_types)

            supported_types.remove(200)
            supported_types.remove(400)
            supported_types.remove(500)

            if res.method != None:
                self.new_dict2[res.method.upper() + ' ' + res.path] = supported_types

            # Generate classes for request handling automatically
            if res.method != None:
                generated_classes += add_generated_classes({
                    'class_name': cls_name,
                    'method': res.method,
                    'return_val': 'return Response_Element()' if self.rs else 'Response_Element(True, (abort(400)))',
                    'auth': security,
                    'documentation': '\"\"\"' + res.description.data + '\"\"\"\n' if type(res.description.data) == str else '',
                    'validation': validation_builder,
                    'args_list': args_list,
                    'args_search': args_search,
                    'resp_types': (self.enforce_resp, supported_types)
                })

        create_file(self.generated_dir, 'generated_routes.py', generated_classes)

        # Creates the delegates files, if they do not exist
        if self.raml.security_schemes != None:
            for sec_scheme in self.raml.security_schemes:
                create_delegate(sec_scheme.name + '_auth', sec_scheme.name.capitalize() + '_Auth')

        create_delegate('pre_req', 'Pre_Req')
        create_delegate('post_req', 'Post_Req')

        # Create the structures folder
        create_sys_folder('./generated/structures/')

        # Export the dictionary with validation information
        self.file_name = time.strftime("%Y%m%d%H%M%S") + '_valid.py'

        fn_route = os.path.join(os.path.dirname(__file__), 'dict_ex.template')
        template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
        file_content = template_route.render(tmpl={'dictionary': self.new_dict})
        create_file('./generated/structures/', self.file_name, file_content)

        # Export the dictionary with return type information
        self.file_name2 = time.strftime("%Y%m%d%H%M%S") + '_rtype.py'

        fn_route = os.path.join(os.path.dirname(__file__), 'dict_ex.template')
        template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
        file_content = template_route.render(tmpl={'dictionary': self.new_dict2})
        create_file('./generated/structures/', self.file_name2, file_content)

        # Create delegates for all mime type body validations
        mt_set = copy.deepcopy(self.mime_types)
        mt_set.append('text/plain')
        for m_type in set(mt_set):
            new_del = m_type.replace('/', '_').replace('-', '_')
            create_delegate(new_del, 'validation')


    def bind_routes(self):
        if not os.path.exists(self.generated_dir):
            raise Exception("No generated routes exist!")

        # Add basic imports
        bindings = 'from flask import Blueprint, request' + '\n'
        bindings += 'import generated_routes' + '\n'

        # Add imports for handwritten files
        handwritten_imports = generate_handwritten_imports('routes')
        for imp in handwritten_imports:
            bindings += 'import ' + imp + '\n'

        # Add definition to allow for importing the route definitions
        bindings += '\nroute_imports = Blueprint(\'route_imports\', __name__)' + '\n\n'

        # Creates the string for the RAML version in the URI
        raml_version = set_raml_version(self.raml.version)

        handwritten_classes = generate_handwritten_classes(handwritten_imports)

        # Create route binding and reference to handler method
        for res in self.raml.resources:
            if res.method != None:
                base_name = build_cls_name(res.path, res.method, res.display_name)
                flask_path = res.path.replace('{', '<').replace('}', '>')

                uri_vals = re.findall('{[A-Za-z0-9_]+}', res.path)
                for idx,val in enumerate(uri_vals):
                    uri_vals[idx] = val.replace('{','').replace('}','')

                uri_vals = ",".join(uri_vals)

                bindings += '@route_imports.route(\'' + raml_version + flask_path + '\', methods=[\'' + res.method + '\'])' + '\n'
                bindings += 'def handle_' + base_name + '(' + uri_vals + '):' + '\n'
                bindings += generate_handler(base_name, handwritten_classes)
                bindings += '    return handler.handle_request()\n\n\n\n'

        # Create route mapping file
        create_file(self.generated_dir, 'route_mappings.py', bindings)


    def static_analysis(self, old_f=None, new_f=None):

        # Analyze the validations
        new_dict = open_new_dict('valid', self.new_dict, new_f)
        old_dict = open_old_dict('valid', self.file_name, old_f)
        check_validations(old_dict, new_dict)

        # Analyze the return types
        new_dict = open_new_dict('rtype', self.new_dict, new_f)
        old_dict = open_old_dict('rtype', self.file_name, old_f)
        check_returnt(old_dict, new_dict)

    def test_analysis(self):
        md_gen = import_module('generated.generated_routes')

        for res in self.test_res:
            v_uri = {}
            v_args = ImmutableMultiDict([])
            v_data = ''
            v_mimetype = 'text/plain'

            if res['validation'] != []:
                for x in res['validation']:
                    if x['source'] == 'get_param':
                        if x['validation']['example'] == None:
                            info_print('GET Parameter ' + x['validation']['name'] + ' of resource ' + res['name'] + ' does not have an example defined for testing')
                        else:
                            d_items = []
                            for y in v_args:
                                d_items.append((y, v_args[y]))

                            d_items.append((x['validation']['name'], x['validation']['example']))
                            v_args = ImmutableMultiDict(d_items)

                    elif x['source'] == 'uri_param':
                        if x['validation']['example'] == None:
                            info_print('URI Parameter ' + x['validation']['name'] + ' of resource ' + res['name'] + ' does not have an example defined for testing')
                        else:
                            v_uri[x['validation']['name']] = x['validation']['example']
                    elif x['source'] == 'body':
                        for y in x['validation']:
                            v_mimetype = y['mime-type']
                            if y['example'] == None:
                                info_print('BODY with schema ' + y['mime-type'] + ' of resource ' + res['name'] + ' does not have an example defined for testing')
                            else:
                                v_data = y['example']

            mr = Mock_Request(v_uri, v_args, v_data, v_mimetype)

            tested_class = eval('md_gen.' + res['name'] + '(mr)')
            result = tested_class.validate_params_handler()
            if result.response == ('', 200) and result.proceed == True:
                info_print('Test of ' + res['name'] + ': SUCCESS')
            else:
                warn_print('Test of ' + res['name'] + ': FAIL')


    def start_server(self):
        module = import_module('generated.route_mappings', 'route_imports')
        self.app.register_blueprint(module.route_imports, url_prefix='')
        self.app.run()


    def generate_all(self):
        self.generate_code()
        self.bind_routes()

    def validate_all(self):
        self.static_analysis()
        self.test_analysis()

    def exec_all(self):
        self.generate_code()
        self.bind_routes()
        self.static_analysis()
        self.test_analysis()
        self.start_server()

    def exec_all_timing(self):
        s_time = time.time()
        self.generate_code()
        time_print('Code generation finished after ' + str(round(time.time() - s_time, 2)) + ' seconds')
        self.bind_routes()
        time_print('Route binding finished after ' + str(round(time.time() - s_time, 2)) + ' seconds')
        self.static_analysis()
        time_print('Static analysis finished after ' + str(round(time.time() - s_time, 2)) + ' seconds')
        self.test_analysis()
        time_print('Test analysis finished after ' + str(round(time.time() - s_time, 2)) + ' seconds')
        self.start_server()

def create_sys_folder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        text_file = open(dir + '__init__.py', 'w')
        text_file.write('')
        text_file.close()


def create_delegate(name, del_type):
    fn_delegate = os.path.join(os.path.dirname(__file__), 'delegate.template')
    template_delegate = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_delegate)

    new_delegate = template_delegate.render(type=del_type)
    text_file = open('./delegates/' + name + '_delegate.py', 'w')
    text_file.write(new_delegate)
    text_file.close()


def add_validation_elements(val_type, params, list=[]):
    if params is not None:
        for i in params:
            valid = Validation_Element(val_type, i.name, i.desc, i.type, i.enum, i.pattern, i.min_length, i.max_length,
                                       i.minimum, i.maximum, i.example, i.repeat, i.required, i.default)
            list.append(valid.dump())

    return list


def create_file(dir, file_name, content):
    text_file = open(dir + file_name, 'w')
    text_file.write(content.encode('utf-8'))
    text_file.close()


def set_raml_version(version):
    if version == None:
        return ''
    else:
        return '/v' + str(version)


def generate_handler(base_name, handwritten_classes):
    handwritten_option = [item for item in handwritten_classes if item[1] == base_name]
    if handwritten_option != []:
        return '    handler = ' + handwritten_option[0][0] + '.' + base_name + '(request)\n'
    else:
        return '    handler = generated_routes.' + base_name + '_Base(request)\n'

def generate_handwritten_imports(folder):
    handwritten_imports = []
    for x in os.walk(folder):
        folder = x[0].replace('/', '.').replace('\\', '.') + '.'

        for y in x[2]:
            f_split = y.split('.', 1)

            if f_split[0] != '__init__' and f_split[1] != 'pyc':
                handwritten_imports.append(folder + f_split[0])

    return handwritten_imports

def generate_handwritten_classes(imports):
    handwritten_classes = []
    for i in imports:
        module_info = pyclbr.readmodule(i)

        for item in module_info.values():
            handwritten_classes.append((i, item.name))

    return handwritten_classes


def add_generated_classes(tmpl_vars):
    fn_route = os.path.join(os.path.dirname(__file__), 'generated_class.template')
    template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
    return template_route.render(tmpl=tmpl_vars) + '\n\n'


def get_args(validation_builder):
    args = []
    args.append('BODY_mime_type')
    args.append('BODY_content')
    for a in validation_builder:
        if type(a['validation']) == dict:
            var_name = a['validation']['name'].replace('-', '_')
            var_name = var_name.replace('$', '_')
            if a['source'] == 'get_param':
                args.append('GET_' + var_name)
            else:
                args.append('URI_' + var_name)

    for idx in range(len(args)):
        args[idx] = args[idx].replace(' ', '_')

    args = list(set(args))

    return args


def create_valid(c_el, x=None):
    return Validation_Element('body_param',
                              c_el.get('displayName', x),
                              c_el.get('description'),
                              c_el.get('type'),
                              c_el.get('enum'),
                              c_el.get('pattern'),
                              c_el.get('min_length'),
                              c_el.get('max_length'),
                              c_el.get('minimum'),
                              c_el.get('maximum'),
                              c_el.get('example'),
                              c_el.get('repeat'),
                              c_el.get('required'),
                              c_el.get('default')
                               )


def build_cls_name(path=None, method=None, display_name=None, force_path=False):
    if method == None:
        method = 'any'

    identifier = display_name
    if display_name == None or force_path == True:
        identifier = path

        if path == None:
            raise Exception("No class name could be determined")

    if identifier.startswith('/'):
        identifier = identifier[1:]

    if identifier.startswith('{'):
        identifier = identifier[1:]

    if identifier.endswith('}'):
        identifier = identifier[:-1]

    identifier = identifier.replace("/", "_")
    identifier = identifier.replace(" ", "_")
    identifier = identifier.replace("\\", "_")
    identifier = identifier.replace("{", "_")
    identifier = identifier.replace("}", "_")
    identifier = identifier.replace("-", "_")
    identifier = identifier.replace("$", "_")
    identifier = identifier.replace("~", "_")
    identifier = identifier.replace("=", "_")
    identifier = identifier.replace(".", "_")
    identifier = identifier.replace(":", "_")

    return identifier + '_' + method


def open_old_dict(d_type, current_file, old_f):
    if old_f != None:
        open_file = '../generated/structures/' + old_f + '_' + d_type + '.py'
        fn = os.path.join(os.path.dirname(__file__), open_file)
        old_dict = eval(Path(fn).read_text())
        return old_dict

    validations = os.listdir('./generated/structures/')
    highest_valid = 0
    highest_rtype = 0
    selected_valid = ''
    for v in validations:
        if v != '__init__.py' and v != current_file:
            if int(str.split(v, '_')[0]) > highest_valid and str.split(v, '_')[1] == 'valid.py':
                selected_valid = v

            if int(str.split(v, '_')[0]) > highest_rtype and str.split(v, '_')[1] == 'rtype.py':
                selected_rtype = v

    if selected_valid == '':
        return None

    open_file = '../generated/structures/' + selected_valid
    fn = os.path.join(os.path.dirname(__file__), open_file)
    old_dict = eval(Path(fn).read_text())
    return old_dict


def open_new_dict(d_type, current_dict, new_f):
    if new_f == None:
        return current_dict
    else:
        open_file = '../generated/structures/' + new_f + '_' + d_type + '.py'
        fn = os.path.join(os.path.dirname(__file__), open_file)
        new_dict = eval(Path(fn).read_text())
        return new_dict


def check_validations(old_dict, new_dict):
    changed = False
    if old_dict != None and new_dict != None:
        old_r_list = []
        new_r_list = []

        [old_r_list.append(old_r) for old_r in old_dict]
        [new_r_list.append(new_r) for new_r in new_dict]

        added_r = [item for item in new_r_list if item not in old_r_list]
        removed_r = [item for item in old_r_list if item not in new_r_list]

        for ad_r in added_r:
            changed = True
            info_print('Routed added to the build: ' + ad_r)

        for re_r in removed_r:
            changed = True
            info_print('Routed removed from the build: ' + re_r)

        for route in new_r_list:
            if new_dict[route] != []:
                new_res = new_dict.get(route, None)
                old_res = old_dict.get(route, None)

                if new_res != None and old_res != None:
                    res = populate_params(new_res, old_res)
                    n_get = res[0]
                    n_body =  res[1]
                    o_get = res[2]
                    o_body = res[3]

                    if compare_get(n_get, o_get, changed) == True:
                        changed = True
                    if compare_body(n_body, o_body, changed) == True:
                        changed = True

        if changed == False:
            info_print('No changes compared to the previous version')
    else:
        info_print('No previous validations for comparison found')


def populate_params(new_res, old_res):
    n_get = []
    n_body = []
    o_get = []
    o_body = []

    for n_re in new_res:
        if n_re['source'] == 'get_param':
            n_get.append(n_re['validation'])
        if n_re['source'] == 'body':
            n_body.append(n_re['validation'])

    for o_re in old_res:
        if o_re['source'] == 'get_param':
            o_get.append(o_re['validation'])
        if o_re['source'] == 'body':
            o_body.append(o_re['validation'])

    return n_get, n_body, o_get, o_body


def iterate_var_map(var_map, val):
    for var_key in var_map:
        if var_map[var_key][1] == None:
            info_print('The validation type ' + var_key + ' was added to ' + val)
        else:
            for var_key2 in var_map[var_key][0]:
                if var_map[var_key][0][var_key2] != var_map[var_key][1][var_key2]:
                    changed = True
                    info_print('The validation type ' + var_key + ' was added to ' + val)


def compare_get(n_get, o_get, changed):
    changed = False
    get_map = {}
    for idx in range(len(n_get)):
        get_map[n_get[idx]['name']] = [idx, None]

    for idx in range(len(o_get)):
        if o_get[idx]['name'] in get_map:
            get_map[o_get[idx]['name']][1] = idx
        else:
            changed = True
            info_print('The query parameter ' + get_map[o_get[idx]['name']] + ' was removed')

    for query_p in get_map:
        if get_map[query_p][1] == None:
            changed = True
            info_print('The query parameter ' + query_p + ' was added')
        else:
            for key in n_get[get_map[query_p][0]].keys():
                if n_get[get_map[query_p][0]][key] != o_get[get_map[query_p][1]][key]:
                    changed = True
                    info_print('The validation for query parameter ' + query_p + ' was changed: value of ' + key + ' was modified')

    return changed


def compare_body(n_body, o_body, changed):
    changed = False
    body_map = {}
    for idx in range(len(n_body)):
        for idx2 in range(len(n_body[idx])):
            body_map[n_body[idx][idx2]['mime-type']] = [[
                n_body[idx][idx2]['errors'],
                n_body[idx][idx2]['example'],
                n_body[idx][idx2]['schema'],
                n_body[idx][idx2]['params']
            ], None]

    for idx in range(len(o_body)):
        for idx2 in range(len(o_body[idx])):
            if o_body[idx][idx2]['mime-type'] in body_map:
                body_map[o_body[idx][idx2]['mime-type']][1] = [
                    n_body[idx][idx2]['errors'],
                    n_body[idx][idx2]['example'],
                    n_body[idx][idx2]['schema'],
                    n_body[idx][idx2]['params']
                ]
            else:
                changed = True
                info_print('The body validation with Mime Type ' + o_body[idx][idx2][
                    'mime-type'] + ' was removed')

    for val in body_map:
        if body_map[val][1] == None:
            changed = True
            info_print('The body validation with Mime Type ' + val + ' was added')
        else:
            if body_map[val][0][0] != body_map[val][1][0]:
                info_print('The potential errors for the body validation of ' + val + ' was changed')
                changed = True

            if body_map[val][0][1] != body_map[val][1][1]:
                info_print('The example for the body validation of ' + val + ' was changed')
                changed = True

            if body_map[val][0][2] != body_map[val][1][2]:
                changed = True
                info_print('The schema for the body validation of ' + val + ' was changed')

            var_map = {}
            for idx in range(len(body_map[val][0][3])):
                if type(body_map[val][0][3][idx]) == list:
                    var_map[body_map[val][0][3][idx][0]['validation']['name']] = [{
                        'repeat': [i['validation']['repeat'] for i in body_map[val][0][3][idx]],
                        'enum': [i['validation']['enum'] for i in body_map[val][0][3][idx]],
                        'minimum': [i['validation']['minimum'] for i in body_map[val][0][3][idx]],
                        'desc': [i['validation']['desc'] for i in body_map[val][0][3][idx]],
                        'min_length': [i['validation']['min_length'] for i in body_map[val][0][3][idx]],
                        'default': [i['validation']['default'] for i in body_map[val][0][3][idx]],
                        'pattern': [i['validation']['pattern'] for i in body_map[val][0][3][idx]],
                        'required': [i['validation']['required'] for i in body_map[val][0][3][idx]],
                        'maximum': [i['validation']['maximum'] for i in body_map[val][0][3][idx]],
                        'max_length': [i['validation']['max_length'] for i in body_map[val][0][3][idx]],
                        'type': [i['validation']['type'] for i in body_map[val][0][3][idx]],
                        'example': [i['validation']['example'] for i in body_map[val][0][3][idx]]
                    }, None]
                else:
                    var_map[body_map[val][0][3][idx]['validation']['name']] = [{
                        'repeat': body_map[val][0][3][idx]['validation']['repeat'],
                        'enum': body_map[val][0][3][idx]['validation']['enum'],
                        'minimum': body_map[val][0][3][idx]['validation']['minimum'],
                        'desc': body_map[val][0][3][idx]['validation']['desc'],
                        'min_length': body_map[val][0][3][idx]['validation']['min_length'],
                        'default': body_map[val][0][3][idx]['validation']['default'],
                        'pattern': body_map[val][0][3][idx]['validation']['pattern'],
                        'required': body_map[val][0][3][idx]['validation']['required'],
                        'maximum': body_map[val][0][3][idx]['validation']['maximum'],
                        'max_length': body_map[val][0][3][idx]['validation']['max_length'],
                        'type': body_map[val][0][3][idx]['validation']['type'],
                        'example': body_map[val][0][3][idx]['validation']['example']
                    }, None]

            for idx in range(len(body_map[val][1][3])):
                if type(body_map[val][1][3][idx]) == list:
                    if body_map[val][1][3][idx][0]['validation']['name'] in var_map.keys():
                        var_map[body_map[val][1][3][idx][0]['validation']['name']][1] = {
                            'repeat': [i['validation']['repeat'] for i in body_map[val][1][3][idx]],
                            'enum': [i['validation']['enum'] for i in body_map[val][1][3][idx]],
                            'minimum': [i['validation']['minimum'] for i in body_map[val][1][3][idx]],
                            'desc': [i['validation']['desc'] for i in body_map[val][1][3][idx]],
                            'min_length': [i['validation']['min_length'] for i in body_map[val][1][3][idx]],
                            'default': [i['validation']['default'] for i in body_map[val][1][3][idx]],
                            'pattern': [i['validation']['pattern'] for i in body_map[val][1][3][idx]],
                            'required': [i['validation']['required'] for i in body_map[val][1][3][idx]],
                            'maximum': [i['validation']['maximum'] for i in body_map[val][1][3][idx]],
                            'max_length': [i['validation']['max_length'] for i in body_map[val][1][3][idx]],
                            'type': [i['validation']['type'] for i in body_map[val][1][3][idx]],
                            'example': [i['validation']['example'] for i in body_map[val][1][3][idx]]
                        }
                    else:
                        changed = True
                        info_print('The validation type ' + body_map[val][1][3][idx][0]['validation'][
                            'name'] + ' was removed from ' + val)
                else:
                    if body_map[val][1][3][idx]['validation']['name'] in var_map:
                        var_map[body_map[val][1][3][idx]['validation']['name']][1] = {
                            'repeat': body_map[val][1][3][idx]['validation']['repeat'],
                            'enum': body_map[val][1][3][idx]['validation']['enum'],
                            'minimum': body_map[val][1][3][idx]['validation']['minimum'],
                            'desc': body_map[val][1][3][idx]['validation']['desc'],
                            'min_length': body_map[val][1][3][idx]['validation']['min_length'],
                            'default': body_map[val][1][3][idx]['validation']['default'],
                            'pattern': body_map[val][1][3][idx]['validation']['pattern'],
                            'required': body_map[val][1][3][idx]['validation']['required'],
                            'maximum': body_map[val][1][3][idx]['validation']['maximum'],
                            'max_length': body_map[val][1][3][idx]['validation']['max_length'],
                            'type': body_map[val][1][3][idx]['validation']['type'],
                            'example': body_map[val][1][3][idx]['validation']['example']
                        }
                    else:
                        changed = True
                        info_print('The validation type ' + body_map[val][1][3][idx]['validation'][
                            'name'] + ' was removed from ' + val)

            iterate_var_map(var_map, val)

    return changed


def check_returnt(old_dict, new_dict):
    if old_dict != None:
        old_keys = []
        new_keys = []
        for i in old_dict:
            if old_dict[i] != set([]):
                old_keys.append(i)

        for i in new_dict:
            if new_dict[i] != set([]):
                new_keys.append(i)

        added_rtype = set(new_keys) - set(old_keys)
        removed_rtype = set(old_keys) - set(new_keys)

        changed = False
        for a in added_rtype:
            changed = True
            info_print('Return type ' + a + ' was added')

        for r in removed_rtype:
            changed = True
            info_print('Return type ' + r + ' was added')

        new_keys = set(new_keys) - set(removed_rtype)

        for comp in new_keys:

            if new_dict[comp] != old_dict[comp]:
                changed = True
                ad = new_dict[comp] - old_dict[comp]
                rv = old_dict[comp] - new_dict[comp]

                for a in ad:
                    info_print('Return type ' + a + ' was added to ' + comp)

                for r in rv:
                    info_print('Return type ' + r + ' was removed from ' + comp)

        if changed == False:
            info_print('No return type changes')


def info_print(text):
    print '[INFO] ' + text

def warn_print(text):
    print '[WARN] ' + text

def time_print(text):
    print '[TIME] ' + text

class Mock_Request(object):

    def __init__(self, uri, get, body, mime):
        # URI inputs
        self.view_args = uri

        # GET inputs
        self.args = get

        # BODY inputs
        self.data = body

        # MIME type
        self.mimetype = mime