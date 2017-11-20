import os
import copy
from pathlib2 import Path
import imp
from werkzeug.datastructures import ImmutableMultiDict
from collections import OrderedDict

import Printer
from Mock_Request import Mock_Request

class Comparison:
    def __init__(self):
        self.current_version = ''
        self.test_res = []
        self.new_v_file = None
        self.new_r_file = None
        self.old_v_file = None
        self.old_r_file = None
        self.output = []


    @property
    def current_version(self):
        return self.current_version

    @current_version.setter
    def current_version(self, value):
        self.current_version = value

    @property
    def test_res(self):
        return self.test_res

    @test_res.setter
    def test_res(self, value):
        self.test_res = value

    @property
    def new_v_filter(self):
        return self.new_v_file

    @new_v_filter.setter
    def new_v_file(self, value):
        self.new_v_file = value

    @property
    def new_r_file(self):
        self.new_r_file

    @new_r_file.setter
    def new_r_file(self, value):
        self.new_r_file = value

    @property
    def old_v_file(self):
        return self.old_v_file

    @old_v_file.setter
    def old_v_file(self, value):
        self.old_v_file = value

    @property
    def old_r_file(self):
        return self.old_f

    @old_r_file.setter
    def set_old_r_file(self, old_f):
        self.old_r_file = old_f

    @property
    def generated_directory(self):
        return self.generated_directory

    @generated_directory.setter
    def generated_directory(self, value):
        self.generated_directory = value

    @property
    def routes_directory(self):
        return self.routes_directory

    @routes_directory.setter
    def routes_directory(self, value):
        self.routes_directory = value

    @property
    def delegates_directory(self):
        return self.delegates_directory

    @delegates_directory.setter
    def delegates_directory(self, value):
        self.delegates_directory = value

    def static_valid_analysis(self, new_f=None):
        # Analyze the validations
        self.new_dict = self.open_new_dict('valid', self.new_v_file, new_f)
        self.old_dict = self.open_old_dict('valid', self.current_version, self.old_v_file)
        self.check_validations(self.old_dict, self.new_dict)
        return self.dump_output()


    def static_rtypes_analysis(self, new_f=None):
        # Analyze the validations
        self.new_dict = self.open_new_dict('rtype', self.new_r_file, new_f)
        self.old_dict = self.open_old_dict('rtype', self.current_version, self.old_r_file)
        self.check_returnt(self.old_dict, self.new_dict)
        return self.dump_output()


    def test_analysis(self):
        import_name = self.generated_directory + '/generated_routes.py'
        md_gen = imp.load_source('generated_routes', import_name)

        for res in self.test_res:
            v_uri = {}
            v_args = ImmutableMultiDict([])
            v_data = ''
            v_mimetype = 'text/plain'

            if res.get('validation') != [] and res.get('validation') != None:
                for x in res['validation']:
                    if x['source'] == 'get_param':
                        if x['validation']['example'] == None:
                            self.output.append(('INFO', 'GET Parameter ' + x['validation']['name'] + ' of resource ' + res['name'] + ' does not have an example defined for testing'))
                        else:
                            d_items = []
                            for y in v_args:
                                d_items.append((y, v_args[y]))

                            d_items.append((x['validation']['name'], x['validation']['example']))
                            v_args = ImmutableMultiDict(d_items)

                    elif x['source'] == 'uri_param':
                        if x['validation']['example'] == None:
                            self.output.append(('INFO', 'URI Parameter ' + x['validation']['name'] + ' of resource ' + res['name'] + ' does not have an example defined for testing'))
                        else:
                            v_uri[x['validation']['name']] = x['validation']['example']
                    elif x['source'] == 'body':
                        for y in x['validation']:
                            v_mimetype = y['mime-type']
                            if y['example'] == None:
                                self.output.append(('INFO', 'BODY with schema ' + y['mime-type'] + ' of resource ' + res['name'] + ' does not have an example defined for testing'))
                            else:
                                v_data = y['example']

            mr = Mock_Request(v_uri, v_args, v_data, v_mimetype)

            tested_class = eval('md_gen.' + res['name'] + '(mr)')
            result = tested_class.validate_params_handler()
            if result.value == '' and result.code == 200 and result.proceed == True:
                self.output.append(('INFO', 'Test of ' + res['name'] + ': SUCCESS'))
            else:
                self.output.append(('WARN', 'Test of ' + res['name'] + ': FAIL'))

        return self.dump_output()

    def dump_output(self):
        saved_out = copy.deepcopy(self.output)
        self.output = []

        return saved_out

    def open_old_dict(self, d_type, current_file, old_f, old_dict=None):
        if old_dict != None:
            return old_dict

        dir = os.path.join(self.generated_directory, 'structures', '')
        dir = os.path.abspath(dir)

        if old_f != None:
            open_file = dir + old_f + '_' + d_type + '.py'
            fn = os.path.join(os.path.dirname(__file__), open_file)
            old_dict = eval(Path(fn).read_text())
            return old_dict

        validations = os.listdir(dir)
        c_f_name = current_file + '_valid.py'
        highest_valid = 0
        highest_rtype = 0
        selected_valid = ''
        for v in validations:
            if v != '__init__.py' and v != c_f_name:
                ending = d_type + '.py'
                if int(str.split(v, '_')[0]) > highest_valid and str.split(v, '_')[1] == ending:
                    selected_valid = v

        if selected_valid == '':
            return None

        open_file = os.path.join(dir, selected_valid)
        file = open(open_file, 'r').read()
        return eval(file)


    def open_new_dict(self, d_type, current_dict, new_f):
        if new_f == None:
            return current_dict
        else:
            dir = os.path.join('.', self.generated_directory, 'structures', '')
            dir = os.path.abspath('.' + dir)
            open_file = os.path.join(dir, new_f + '_' + d_type + '.py')
            file = open(open_file, 'r').read()
            return eval(file)


    def check_validations(self, old_dict, new_dict):
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
                self.output.append('Routed added to the build: ' + ad_r)

            for re_r in removed_r:
                changed = True
                self.output.append('Routed removed from the build: ' + re_r)

            for route in new_r_list:
                if new_dict[route] != []:
                    new_res = new_dict.get(route, None)
                    old_res = old_dict.get(route, None)

                    if new_res != None and old_res != None:
                        res = self.populate_params(new_res, old_res)
                        n_get = res[0]
                        n_body = res[1]
                        o_get = res[2]
                        o_body = res[3]

                        if self.compare_get(n_get, o_get) == True:
                            changed = True
                        if self.compare_body(n_body, o_body) == True:
                            changed = True

            if changed == False:
                self.output.append('No changes compared to the previous version')
        else:
            self.output.append('No previous validations for comparison found')

    def populate_params(self, new_res, old_res):
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

    def compare_get(self, n_get, o_get):
        changed = False
        get_map = {}
        for idx in range(len(n_get)):
            get_map[n_get[idx]['name']] = [idx, None]

        for idx in range(len(o_get)):
            if o_get[idx]['name'] in get_map:
                get_map[o_get[idx]['name']][1] = idx
            else:
                changed = True
                self.output.append('The query parameter ' + o_get[idx]['name'] + ' was removed')

        for query_p in get_map:
            if get_map[query_p][1] == None:
                changed = True
                self.output.append('The query parameter ' + query_p + ' was added')
            else:
                for key in n_get[get_map[query_p][0]].keys():
                    if n_get[get_map[query_p][0]].get(key) != o_get[get_map[query_p][1]].get(key):
                        changed = True
                        self.output.append(
                            'The validation for query parameter ' + query_p + ' was changed: value of ' + key + ' was modified')

        return changed

    def compare_body(self, n_body, o_body):
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
                        o_body[idx][idx2]['errors'],
                        o_body[idx][idx2]['example'],
                        o_body[idx][idx2]['schema'],
                        o_body[idx][idx2]['params']
                    ]
                else:
                    changed = True
                    self.output.append('The body validation with Mime Type ' + o_body[idx][idx2][
                        'mime-type'] + ' was removed')

        for val in body_map:
            if body_map[val][1] == None:
                changed = True
                self.output.append('The body validation with Mime Type ' + val + ' was added')
            else:
                if body_map[val][0][0] != body_map[val][1][0]:
                    self.output.append('The potential errors for the body validation of ' + val + ' have been changed')
                    changed = True

                if body_map[val][0][1] != body_map[val][1][1]:
                    self.output.append('The example for the body validation of ' + val + ' was changed')
                    changed = True

                if body_map[val][0][2] != body_map[val][1][2]:
                    changed = True
                    self.output.append('The schema for the body validation of ' + val + ' was changed')

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
                            self.output.append('The validation type ' + body_map[val][1][3][idx][0]['validation'][
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
                            self.output.append('The validation type ' + body_map[val][1][3][idx]['validation'][
                                'name'] + ' was removed from ' + val)

                if self.iterate_var_map(var_map, val) == True:
                    changed = True

        return changed

    def iterate_var_map(self, var_map, val):
        changed = False
        for var_key in var_map:
            if var_map[var_key][1] == None:
                changed = True
                self.output.append('The validation type ' + var_key + ' was added to ' + val)
            else:
                for var_key2 in var_map[var_key][0]:
                    if var_map[var_key][0][var_key2] != var_map[var_key][1][var_key2]:
                        changed = True
                        self.output.append('The validation type ' + var_key + ' was added to ' + val)

        return changed

    def check_returnt(self, old_dict, new_dict):
        if old_dict == None:
            for i in new_dict:
                self.output.append('Return type ' + i + ' was added')

        else:
            old_keys = []
            new_keys = []

            for i in old_dict:
                old_keys.append(i)

            for i in new_dict:
                new_keys.append(i)

            added_rtype = set(new_keys) - set(old_keys)
            removed_rtype = set(old_keys) - set(new_keys)

            changed = False

            for a in added_rtype:
                changed = True
                self.output.append('Return type ' + a + ' was added')

            for r in removed_rtype:
                changed = True
                self.output.append('Return type ' + r + ' was removed')

            iter_keys = set(old_keys) - removed_rtype
            for t in iter_keys:
                matching_dict = {}

                for i in old_dict[t]:
                    matching_dict[i['code']] = {
                        'old': [],
                        'new': []
                    }
                    matching_dict[i['code']]['old'].append(i['body'])

                for i in new_dict[t]:
                    if i['code'] in matching_dict:
                        matching_dict[i['code']]['new'].append(i['body'])
                    else:
                        matching_dict[i['code']] = {
                            'old': [],
                            'new': []
                        }
                        matching_dict[i['code']]['new'].append(i['body'])

                for x in matching_dict:
                    if matching_dict[x]['new'] != matching_dict[x]['old']:
                        changed = True
                        if matching_dict[x]['old'] == [] and matching_dict[x]['new'] == [None]:
                            self.output.append('Return type ' + str(x) + ' was added')
                        else:
                            self.output.append('Return type ' + str(x) + ' was modified: from ' + str(matching_dict[x]['old']) + ' to ' + str(matching_dict[x]['new']))

        if changed == False:
            self.output.append('No return type changes')