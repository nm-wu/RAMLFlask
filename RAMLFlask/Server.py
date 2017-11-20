import os
from importlib import import_module
from flask import Flask
import ConfigParser
import Printer

class Server:
    def __init__(self, generator, comparison, config_file='config.ini'):

        # Generator class
        self.gen = generator

        # Comparison class

        self.comp = comparison

        cparse = ConfigParser.ConfigParser()
        cparse.read(config_file)

        self.generated_dir = os.path.join('generated')
        self.routes_dir = os.path.join('routes')
        self.delegates_dir = os.path.join('delegates')

        if cparse.has_section('DIRECTORIES'):
            if cparse.has_option('DIRECTORIES', 'generated'):
                self.gen.generated_directory = cparse.get('DIRECTORIES', 'generated')
                self.comp.generated_directory = cparse.get('DIRECTORIES', 'generated')
            if cparse.has_option('DIRECTORIES', 'routes'):
                self.gen.routes_directory = cparse.get('DIRECTORIES', 'routes')
                self.comp.routes_directory = cparse.get('DIRECTORIES', 'routes')
            if cparse.has_option('DIRECTORIES', 'delegates'):
                self.gen.delegates_directory = cparse.get('DIRECTORIES', 'delegates')
                self.comp.delegates_directory = cparse.get('DIRECTORIES', 'delegates')

    def generate(self, generate=True, bind=True):
        if generate == True:
            self.gen.generate_code()
        if bind == True:
            self.gen.bind_routes()


    def compare(self, p_v=True, p_r=True, p_t=True, static_validations=None, static_rtypes=None, test_in=[]):
        self.comp.current_version = self.gen.current_file_name
        self.comp.test_res = self.gen.test_res
        self.comp.new_v_file = self.gen.new_v_file
        self.comp.new_r_file = self.gen.new_r_file

        if p_v == True:
            out = self.comp.static_valid_analysis(static_validations)
            for i in out:
                Printer.info_print(i)
        if p_r == True:
            out = self.comp.static_rtypes_analysis(static_rtypes)
            for i in out:
                Printer.info_print(i)
        if p_t == True:
            out = self.comp.test_analysis()
            for i in out:
                if i[0] == 'INFO':
                    Printer.info_print(i[1])
                else:
                    Printer.warn_print(i[1])


    def start_server(self):
        # Creates the basic Flask app
        self.app = Flask(__name__)

        self.app = Flask(__name__)

        folder = self.gen.generated_directory.replace('/', '.').replace('\\', '.') + '.'
        while folder[0] == '.':
            folder = folder[1:]

        while folder[-1] == '.':
            folder = folder[:-1]

        module = import_module(folder + '.route_mappings', 'route_imports')
        self.app.register_blueprint(module.route_imports, url_prefix='')
        self.app.run()


    def exec_all(self):
        self.generate(True, True)
        self.compare(True, True, True)
        self.start_server()