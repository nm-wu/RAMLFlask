import os
import re
import importlib
import time
import copy
import jinja2
import inspect
import ramlfications
from random import choice
from string import ascii_uppercase

import Printer
import Name_Builder
from validation_element import Validation_Element


class Generator:
    def __init__(self, raml_file):
        PARSER_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "parser_config.ini")
        self.raml = ramlfications.parse(raml_file, PARSER_CONFIG)
        self.generated_directory = os.path.join('generated')
        self.routes_directory = os.path.join('routes')
        self.delegates_directory = os.path.join('delegates')

        # Initializes the list of mime types
        self.mime_types = []

        # Resources to test
        self.test_res = []

        # Initializes the placeholder for comparisons
        self.file_name = ''
        self.new_dict = {}
        self.new_dict2 = {}

        # Determines whether classes will return Success or Failure codes without further implementation
        self.rs = True

        # Allows to set if return parameters are enforced
        self.enre = False

    @property
    def return_success(self):
        return self.rs

    @return_success.setter
    def return_success(self, value):
        self.rs = value

    @property
    def enforce_response(self):
        return self.enre

    @enforce_response.setter
    def enforce_response(self, value):
        self.enre = value

    @property
    def raml_version(self):
        return self.raml_version

    @property
    def current_file_name(self):
        return self.file_name

    def set_raml_version(self, version):
        if version == None:
            return ''
        else:
            return '/v' + str(version)

    @property
    def test_res(self):
        return self.test_res

    @property
    def new_v_file(self):
        return self.new_dict

    @property
    def new_r_file(self):
        return self.new_dict2

    @property
    def generated_directory(self):
        return self.generated_dir

    @generated_directory.setter
    def generated_directory(self, value):
        self.generated_dir = value

    @property
    def routes_directory(self):
        return self.routes_dir

    @routes_directory.setter
    def routes_directory(self, value):
        self.routes_directory = value

    @property
    def delegates_directory(self):
        return self.delegates_dir

    @delegates_directory.setter
    def delegates_directory(self, value):
        self.delegates_dir = value


    def generate_code(self):

        # Create directories for the generated, and handwritten hw_imports_test, as well as for the delegates
        self.create_sys_folder(self.generated_directory)
        self.create_sys_folder(self.routes_directory)
        self.create_sys_folder(self.delegates_directory)

        # Print resource count
        Printer.info_print('Starting route generation: ' + str(len(self.raml.resources)) + ' hw_imports_test')

        # Create generated classes
        generated_classes = self.generate_base_implementation()
        self.create_file(self.generated_directory, 'generated_routes.py', generated_classes)

        # Create the structures folder
        self.create_sys_folder(os.path.join('.', self.generated_directory, 'structures'))

        #Export the dictionaries
        self.export_dicts()

        # Create the code for the delegates
        self.create_delegates_code()


    def bind_routes(self):
        if not os.path.exists(self.generated_directory):
            raise Exception("No generated hw_imports_test exist!")

        # Add basic imports
        bindings = 'from flask import Blueprint, request' + '\n'
        bindings += 'import generated_routes' + '\n'

        # Add imports for handwritten files
        handwritten_imports = self.generate_handwritten_imports(self.routes_directory)
        for imp in handwritten_imports:
            bindings += 'import ' + imp + '\n'

        # Add definition to allow for importing the route definitions
        bindings += '\nroute_imports = Blueprint(\'route_imports\', __name__)' + '\n\n'

        # Creates the string for the RAML version in the URI
        raml_version = self.set_raml_version(self.raml.version)

        handwritten_classes = self.generate_handwritten_classes(handwritten_imports)

        # Create route binding and reference to handler method
        for res in self.raml.resources:
            if res.method != None:
                base_name = Name_Builder.build_cls_name(res.path, res.display_name)
                class_name= base_name  + '.' + res.method.capitalize() + '_Base'
                flask_path = res.path.replace('{', '<').replace('}', '>')

                uri_vals = re.findall('<[A-Za-z0-9_:]+>', res.path)
                for idx,val in enumerate(uri_vals):
                    uri_vals[idx] = val.replace('<','').replace('>','').split(':', 1)[-1]

                uri_vals = ",".join(uri_vals)

                bindings += '@route_imports.route(\'' + raml_version + flask_path + '\', methods=[\'' + res.method + '\'])' + '\n'
                bindings += 'def handle_' + base_name + '_' + (''.join(choice(ascii_uppercase) for i in range(20))) + '(' + uri_vals + '):' + '\n'
                bindings += self.generate_handler(base_name, res.method, handwritten_classes)
                bindings += '    return handler.handle_request()\n\n\n\n'

        # Create route mapping file
        self.create_file(self.generated_directory, 'route_mappings.py', bindings)

    def create_sys_folder(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            text_file = open(os.path.join(dir, '__init__.py'), 'w')
            text_file.write('')
            text_file.close()

    def add_validation_elements(self, val_type, params, list=[]):
        if params is not None:
            for i in params:
                valid = Validation_Element(val_type, i.name, i.desc, i.type, i.enum, i.pattern, i.min_length,
                                           i.max_length,
                                           i.minimum, i.maximum, i.example, i.repeat, i.required, i.default)
                list.append(valid.dump())

        return list

    def generate_handwritten_imports(self, folder):
        handwritten_imports = []
        for x in os.walk(folder):
            folder = x[0].replace('/', '.').replace('\\', '.') + '.'
            while folder[0] == '.':
                folder = folder[1:]

            while folder[-1] == '.':
                folder = folder[:-1]

            for y in x[2]:
                f_split = y.split('.', 1)

                if f_split[0] != '__init__' and f_split[1] != 'pyc':
                    handwritten_imports.append(folder + '.' + f_split[0])

        return handwritten_imports

    def get_args(self, validation_builder):
        args = []
        args.append({'type': 'BODY', 'name': 'mime_type'})
        args.append({'type': 'BODY', 'name': 'content'})
        for a in validation_builder:
            if type(a['validation']) == dict:
                var_name = a['validation']['name'].replace('-', '_')
                var_name = var_name.replace('$', '_')
                if a['source'] == 'get_param':
                    args.append({'type': 'GET', 'name': var_name})
                else:
                    args.append({'type': 'URI', 'name': var_name})

        return args


    def add_generated_classes(self, tmpl_vars):
        fn_route = os.path.join(os.path.dirname(__file__), 'generated_class.template')
        template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
        return template_route.render(tmpl=tmpl_vars) + '\n\n'

    def create_valid(self, c_el, x=None):
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

    def create_file(self, dir, file_name, content):
        location = os.path.join(dir, file_name)
        text_file = open(location, 'w')
        text_file.write(content.encode('utf-8'))
        text_file.close()

    def create_delegate(self, name, del_type):
        fn_delegate = os.path.join(os.path.dirname(__file__), 'delegate.template')
        template_delegate = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_delegate)

        new_delegate = template_delegate.render(type=del_type)
        text_file = open(os.path.join('.', 'delegates', name + '_delegate.py'), 'w')
        text_file.write(new_delegate)
        text_file.close()

    def generate_handwritten_classes(self, imports):
        handwritten_classes = []
        for i in imports:
            module = importlib.import_module(i)
            parent_members = inspect.getmembers(module, inspect.isclass)
            for name, obj in parent_members:
                child_members = inspect.getmembers(obj)
                for y in child_members:
                    handwritten_classes.append(str(obj) + '.' + y[0])

        return handwritten_classes

    def generate_handler(self, base_name, method, handwritten_classes):
        folder = self.routes_directory.replace('/', '.').replace('\\', '.') + '.'
        while folder[0] == '.':
            folder = folder[1:]

        while folder[-1] == '.':
            folder = folder[:-1]

        combined_name = base_name + '.' + method.capitalize()

        handwritten_option = [item for item in handwritten_classes if '.'.join(item.split('.')[-2:]) == combined_name]
        if handwritten_option != []:
            return '    handler = ' + handwritten_option[0] + '(request)\n'
        else:
            return '    handler = generated_routes.' + combined_name + '_Base(request)\n'


    def generate_base_implementation(self):
        generated_classes = self.add_imports()

        class_container = {}

        # Iterate over all resources to generate automatic base implementations
        for res in self.raml.resources:
            # Add security delegates
            if res.security_schemes is None:
                security = 'return Response_Element()'
            else:
                for sec_scheme in res.security_schemes:
                    security = 'a_delegate = ' + sec_scheme.name + '_auth_delegate.' + sec_scheme.name.capitalize() + '_Auth_Delegate() \n'
                    security += '            a_delegate.handle_delegation(self.req)\n'
                    security += '            return Response_Element()'

            # Query parameter e.g. ?x=1
            validation_builder = self.add_validation_elements('get_param', res.query_params, [])

            # URI parameter in the base URI
            validation_builder = self.add_validation_elements('uri_param', res.uri_params, validation_builder)

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
                                    valid = self.create_valid(current_el[a], x)
                                    intermediate.append(valid.dump())
                                bodies['validation'][c]['params'].append(intermediate)

                            else:
                                valid = self.create_valid(current_el)
                                bodies['validation'][c]['params'].append(valid.dump())
                    c += 1

                validation_builder.append(bodies)

            parent_class = Name_Builder.build_cls_name(res.path, res.display_name)



            if res.method == None:
                new_method = 'NONE'
            else:
                new_method = res.method

            child_class = new_method.capitalize() + '_Base'
            cls_name = Name_Builder.build_cls_name(res.path, res.display_name) + '_' + new_method + '_Base'

            if res.method != None:
                self.test_res.append({'name': parent_class + '.' + child_class, 'validation': validation_builder})

            vb = copy.deepcopy(validation_builder)
            for i in vb:
                i['class'] = Name_Builder.build_cls_name(res.path, res.method, res.display_name)

            if res.method != None:
                self.new_dict[res.method.upper() + ' ' + res.path] = vb

            args_search = self.get_args(validation_builder)

            # Calculate the supported request types
            base_types = [200,400,500]
            supported_types = []
            if res.responses != None:
                for resp_c in res.responses:
                    if resp_c.method == res.method:

                        if resp_c.code == 200 or resp_c.code == 400 or resp_c.code == 500:
                            base_types.remove(resp_c.code)

                        if resp_c.body is None:
                            response = {
                                'code': resp_c.code,
                                'body': None
                            }
                            supported_types.append(response)
                        else:
                            for i in range(len(resp_c.body)):
                                response = {
                                    'code': resp_c.code,
                                    'body': resp_c.body[i].mime_type
                                }
                                supported_types.append(response)


            for i in base_types:
                supported_types.append({
                    'code': i,
                    'body': None
                })

            if res.method != None:
                self.new_dict2[res.method.upper() + ' ' + res.path] = supported_types

            # Generate classes for request handling automatically
            gen_class = self.add_generated_classes({
                'class_name': child_class,
                'parent_class': parent_class,
                'method': new_method,
                'return_val': 'return Response_Element()' if self.rs else 'Response_Element(True, (abort(400)))',
                'auth': security,
                'documentation': '\"\"\"' + res.description.data + '\"\"\"\n' if type(res.description.data) == str else '',
                'validation': validation_builder,
                'args_search': args_search,
                'resp_types': (self.enre, supported_types)
            })

            if parent_class not in class_container:
                class_container[parent_class] = {
                    'parent_def': 'class ' + parent_class + '():\n',
                    'child_classes': []
                }

            class_container[parent_class]['child_classes'].append(gen_class)

        for group in class_container:
            generated_classes += class_container[group]['parent_def']
            for child in class_container[group]['child_classes']:
                generated_classes += child

        return generated_classes


    def add_imports(self):
        # Add content to the generated classes
        generated_classes = ''

        generated_classes += 'import datetime\n'
        generated_classes += 'from collections import OrderedDict\n'

        if self.raml.security_schemes != None:
            for sec_scheme in self.raml.security_schemes:
                generated_classes += 'from delegates import ' + sec_scheme.name + '_auth_delegate' + '\n\n'

        for mt in self.mime_types:
            generated_classes += 'from delegates import ' + mt + '_delegate' + '\n\n'

        # Import the Response Element
        generated_classes += 'from RAMLFlask.rsp_element import Response_Element\n\n'

        # Add the base class to the generated file
        generated_classes += 'from RAMLFlask.Generated_Class_Base import Generated_Class_Base\n\n'

        # Add the response validator
        generated_classes +='from delegates import resp_validator_delegate\n\n'

        return generated_classes


    def create_delegates_code(self):
        # Creates the delegates files, if they do not exist
        if self.raml.security_schemes != None:
            for sec_scheme in self.raml.security_schemes:
                self.create_delegate(sec_scheme.name + '_auth', sec_scheme.name.capitalize() + '_Auth')

        self.create_delegate('pre_req', 'Pre_Req')
        self.create_delegate('post_req', 'Post_Req')

        self.create_delegate('resp_validator', 'Response_Validator')

        # Create delegates for all mime type body validations
        mt_set = copy.deepcopy(self.mime_types)
        mt_set.append('text/plain')
        for m_type in set(mt_set):
            new_del = m_type.replace('/', '_').replace('-', '_')
            self.create_delegate(new_del, 'validation')


    def export_dicts(self):
        self.file_name = time.strftime("%Y%m%d%H%M%S")
        # Export the dictionary with validation information
        file_name1 = time.strftime("%Y%m%d%H%M%S") + '_valid.py'

        fn_route = os.path.join(os.path.dirname(__file__), 'dict_ex.template')
        template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
        file_content = template_route.render(tmpl={'dictionary': self.new_dict})
        path = os.path.join(self.generated_directory, 'structures', '')
        self.create_file(path, file_name1, file_content)

        # Export the dictionary with return type information
        file_name2 = self.file_name + '_rtype.py'

        fn_route = os.path.join(os.path.dirname(__file__), 'dict_ex.template')
        template_route = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/")).get_template(fn_route)
        file_content = template_route.render(tmpl={'dictionary': self.new_dict2})
        self.create_file(os.path.join('.', self.generated_directory, 'structures', ''), file_name2, file_content)
