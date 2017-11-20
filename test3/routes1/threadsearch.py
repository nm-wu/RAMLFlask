import datetime
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test3.generated.generated_routes import Thread_Search
from RAMLFlask.Generated_Class_Base import Generated_Class_Base
from flask import request, g, jsonify
import functools
import elasticsearch
from flask.ext.restful import reqparse


class Thread_Search():
    class Get(Thread_Search.Get_Base):

        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            g.parser = reqparse.RequestParser(argument_class=ValidatableArgument)
            g.parser.add_argument('q', type=bounded_str, location='args')
            args = strict_parse_args(g.parser, request.args)

            #MOCK
            args.limit = ''
            args.offset = ''
            g.namespace_public_id = ''
            class Encoder():
                def jsonify(self, value):
                    return jsonify(value)
            g.encoder = Encoder()
            #MOCK

            try:
                search_engine = NamespaceSearchEngine(g.namespace_public_id)
                results = search_engine.threads.search(query=args.q, max_results = args.limit, offset = args.offset)

            except SearchInterfaceError:
                return Response_Element(False, ('Search Endpoint not available', 501))

            return Response_Element(True, (g.encoder.jsonify(results), 200))




#Line 21
class InputError(Exception):
    """Raised when bad user input is processed."""

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ValidatableArgument(reqparse.Argument):
    def handle_validation_error(self, error):
        raise InputError(str(error))


#Line 22
def bounded_str(value, key):
    if len(value) > 255:
        raise ValueError('Value {} for {} is too long'.format(value, key))
    return value


#Line 23
def strict_parse_args(parser, raw_args):
    """Wrapper around parser.parse_args that raises a ValueError if unexpected
    arguments are present."""
    args = parser.parse_args()
    unexpected_params = (set(raw_args) - {allowed_arg.name for allowed_arg in
                                          parser.args})
    if unexpected_params:
        raise InputError('Unexpected query parameters {}'.
                         format(unexpected_params))
    return args


#Line 26
class NamespaceSearchEngine(object):
    """Interface for interacting with the search backend within the namespace
    with public id `namespace_public_id`."""

    def __init__(self, namespace_public_id):
        self.messages = MessageSearchAdapter(index_id=namespace_public_id)
        self.threads = ThreadSearchAdapter(index_id=namespace_public_id)


def new_connection():
    """Get a new connection to the Elasticsearch hosts defined in config.
    """

    #MOCK
    return ''
    #MOCK


def wrap_es_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except elasticsearch.TransportError as e:
            raise SearchInterfaceError(e)

    return wrapper


class BaseSearchAdapter:
    """Adapter between the API and an Elasticsearch backend, for a single index
   "and document type."""

    def __init__(self, index_id, doc_type):
        # TODO(emfree) probably want to try to keep persistent connections
        # around, instead of creating a new one each time.
        self._connection = new_connection()
        self.index_id = index_id
        self.doc_type = doc_type

    @wrap_es_errors
    def search(self, query, max_results=100, offset=0):
        """Retrieve search results."""

        #MOCK
        return ''
        #MOCK


class MessageSearchAdapter(BaseSearchAdapter):
    def __init__(self, index_id):
        BaseSearchAdapter.__init__(self, index_id=index_id, doc_type='message')

    def index(self, object_repr):
        """(Re)index a message with API representation `object_repr`."""
        self._index_document(object_repr, parent=object_repr['thread_id'])

class ThreadSearchAdapter(BaseSearchAdapter):
    def __init__(self, index_id):
        BaseSearchAdapter.__init__(self, index_id=index_id, doc_type='thread')

        def index(self, object_repr):
            """(Re)index a thread with API representation `object_repr`."""
            self._index_document(object_repr)


#Line 29
class SearchInterfaceError(Exception):
    """Exception raised if an error occurs connecting to the Elasticsearch
    backend."""
    pass