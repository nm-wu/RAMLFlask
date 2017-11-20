import datetime
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test3.generated.generated_routes import Thread_Search
from RAMLFlask.Generated_Class_Base import Generated_Class_Base
from flask import g, jsonify
from flask.ext.restful import reqparse
import structlog


class Thread_Search():
    class Post(Thread_Search.Post_Base):

        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            g.parser = reqparse.RequestParser(argument_class=ValidatableArgument)
            args = strict_parse_args(g.parser, self.req.args)

            #MOCK
            data = {
                'query': '',
                'sort': 'relevance'
            }
            #MOCK

            query = data.get('query')
            validate_search_query(query)

            sort = data.get('sort')
            validate_search_sort(sort)

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
                results = search_engine.threads.search(query=query, sort=sort, max_results=args.limit, offset=args.offset)
            except SearchEngineError as e:
                g.log.error('Search error: {0}'.format(e))
                Response_Element(False, ('Search error', 501))

            return Response_Element(True, (jsonify(results), 200))




#Line 17
class APIException(Exception):
    pass


class InputError(APIException):
    """Raised on invalid user input (missing required parameter, value too
    long, etc.)"""
    status_code = 400

    def __init__(self, message):
        self.message = message

class ValidatableArgument(reqparse.Argument):
    def handle_validation_error(self, error):
        raise InputError(str(error))


#Line 18
def strict_parse_args(parser, raw_args):
    """
    Wrapper around parser.parse_args that raises a ValueError if unexpected
    arguments are present.
    """
    args = parser.parse_args()
    unexpected_params = (set(raw_args) - {allowed_arg.name for allowed_arg in parser.args})
    if unexpected_params:
        raise InputError('Unexpected query parameters {}'.format(unexpected_params))
    return args


#Line 28
def validate_search_query(query):
    if query is None:
        return

    return


#Line 31
def validate_search_sort(sort):
    if sort not in ('datetime', 'relevance', None):
        raise InputError("Sort order must be 'datetime' or 'relevance'")


#Line 44
THREAD_MAPPING = {
    'properties': {
        'namespace_id': {'type': 'string'},
        'tags': {'type': 'nested', 'properties': {'id': {'type': 'string'}, 'name': {'type': 'string'}}},
        'last_message_timestamp': {'type': 'date', 'format': 'dateOptionalTime'},
        'object': {'type': 'string'},
        'message_ids': {'type': 'string'},
        'snippet': {'type': 'string'},
        'participants': {'type': 'nested', 'properties': {'email': {'type': 'string'}, 'name': {'type': 'string'}}},
        'first_message_timestamp': {'type': 'date', 'format': 'dateOptionalTime'},
        'id': {'type': 'string'},
        'subject': {'type': 'string'},
        'version': {'type': 'long'}
    }
}


MESSAGE_MAPPING = {
    '_parent': {
        'type': 'thread'
    },
    'properties': {
        'id': {'type': 'string'},
        'object': {'type': 'string'},
        'namespace_id': {'type': 'string'},
        'subject': {'type': 'string'},
        'from': {'type': 'nested', 'properties': {'email': {'type': 'string'}, 'name': {'type': 'string'}}},
        'to': {'type': 'nested', 'properties': {'email': {'type': 'string'}, 'name': {'type': 'string'}}},
        'cc': {'type': 'nested', 'properties': {'email': {'type': 'string'}, 'name': {'type': 'string'}}},
        'bcc': {'type': 'nested', 'properties': {'email': {'type': 'string'}, 'name': {'type': 'string'}}},
        'date': {'type': 'date', 'format': 'dateOptionalTime'},
        'thread_id': {'type': 'string'},
        'snippet': {'type': 'string'},
        'body': {'type': 'string'},
        'unread': {'type': 'boolean'},
        'files': {'type': 'nested', 'properties': {'size': {'type': 'long'}, 'id': {'type': 'string'}, 'content_type': {'type': 'string'}, 'filename': {'type': 'string'}}},
    }
}


NAMESPACE_INDEX_MAPPING = {
    'thread': THREAD_MAPPING,
    'message': MESSAGE_MAPPING
}


def new_connection():
    """
    Get a new connection to the Elasticsearch server defined in the config.
    """
    #MOCK
    return ''
    #MOCK


get_logger = structlog.get_logger
log = get_logger()


class DSLQueryEngine(object):
    """
    Generate Elasticsearch DSL queries from API queries.
    Convert Elasticsearch query responses to API responses.
    """

    def __init__(self, query_class):
        self.query_class = query_class

    def generate_query(self, api_query):
        """
        Generate an Elasticsearch DSL query from the Inbox API search query.
        """

        if api_query is None:
            return self.query_class(api_query, '').match_all()

        assert isinstance(api_query, list)

        # Single and-query
        if len(api_query) == 1:
            assert isinstance(api_query[0], dict)
            return self.query_class(api_query[0], 'and').generate()

        # List of and-queries to be or-ed together
        return self.query_class(api_query, 'or').generate()

    def process_results(self, es_results):
        """
        Extract the Inbox API search results from the Elasticsearch results.
        """
        raw_results = es_results['hits']

        # Total number of hits
        total = raw_results['total']

        # Hits returned (#(hits) <= `size` passed in the request)
        results = []
        for h in raw_results['hits']:
            r = dict(relevance=h['_score'],
                     object=h['_source'])

            results.append(r)

        return total, results


class Query(object):
    # TODO[k]: Document more here
    """ Representation of an Elasticsearch DSL query. """

    NESTED_FIELD_FORMAT = '{}.{}'

    def __init__(self, query, query_type='and'):
        self.query = query
        self.query_type = query_type

    def convert(self):
        query_dict = self.convert_and() if self.query_type == 'and' else \
            self.convert_or()
        return dict(query={'bool': query_dict})

    def convert_or(self):
        #d_list = [self.__class__(q) for q in self.query]

        # TODO[k]: DO SOMETHING WITH d_list!
        # return d_list
        raise NotImplementedError

    def convert_and(self):
        must_list = []
        for field in self.query.iterkeys():
            if field == 'all':
                d = self.multi_match(field, boost=True)
            else:
                d = self.match(field)

            must_list.append(d)
        return dict(must=must_list)

    def _field_dict(self, field, value):
        # TODO[k]: check works as expected with non-string values
        if isinstance(value, list):
            field_dict = {field: dict(query=' '.join(v for v in value),
                          lenient=True)}
        else:
            field_dict = {field: dict(query=value, type='phrase',
                          lenient=True)}

        return field_dict

    def match(self, field):
        value = self.query[field]

        # Can _match directly
        if field not in self.nested_fields:
            return self._match(field, value)

        # _match each sub-field for nested fields
        sub_fields = self.nested_fields[field]

        should_list = [self._match(self.NESTED_FIELD_FORMAT.format(field, s),
                                   value) for s in sub_fields]

        query_dict = {'bool': dict(should=should_list)}
        nested_dict = {
            'path': field,
            'score_mode': 'avg',
            'query': query_dict
        }

        return dict(nested=nested_dict)

    def _match(self, field, value):
        """ Generate an Elasticsearch match or match_phrase query. """
        field_dict = self._field_dict(field, value)
        return dict(match=field_dict)

    def multi_match(self, field, boost=True):
        """
        Generate an Elasticsearch multi_match query.
        Simple matches and phrase matches are supported.
        Boosting is applied by default, set boost=False to score all field
        matches equally.
        """
        assert field == 'all' and self._fields
        value = self.query[field]

        if boost:
            return self._boosted_multi_match(field, value)
        else:
            return self._simple_multi_match(field, value)

    def _simple_multi_match(self, field, value):
        d = dict(fields=self._fields.keys())

        field_dict = self._field_dict(field, value)
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def _boosted_multi_match(self, field, value):
        boosted_fields = []
        for f in self._fields:
            multiplier = self._fields.get(f)
            if multiplier:
                boosted_fields.append('{}^{}'.format(f, multiplier))
            else:
                boosted_fields.append(f)

        d = dict(fields=boosted_fields)

        field_dict = self._field_dict(field, value)
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def match_all(self):
        return dict(query={'match_all': {}})

    def generate(self):
        raise NotImplementedError


class MessageQuery(Query):
    nested_fields = {
        'from': ['email', 'name'],
        'to': ['email', 'name'],
        'cc': ['email', 'name'],
        'bcc': ['email', 'name'],
        'files': ['size', 'id', 'content_type', 'filename']
    }

    def __init__(self, query, query_type='and'):
        # TODO[k]: files have content_type, size, filename, id.
        # We exclude the namespace_id.
        attrs = ['id', 'object', 'subject', 'from', 'to', 'cc', 'bcc', 'date',
                 'thread_id', 'snippet', 'body', 'unread', 'files', 'version',
                 'state']
        self._fields = dict((k, None) for k in attrs)

        Query.__init__(self, query, query_type)

        self.apply_weights()

    def apply_weights(self):
        if not self.query or 'all' not in self.query:
            return

        # Arbitrarily assigned boost_score
        if 'weights' not in self.query:
            for f in ['subject', 'snippet', 'body']:
                self._fields[f] = 3
        else:
            self._fields.update(self.query['weights'])
            del self.query['weights']

    def generate(self):
        query_dict = self.convert()

        # TODO[k]:
        # Fix for case self.query is a list i.e. OR-query
        # Fix to support cross Thread/Message field queries
        if self.query.keys()[0] in self._fields or \
                self.query.keys()[0] == 'all':
            return query_dict

        query_dict.update(dict(type='thread'))
        return {'query': dict(has_parent=query_dict)}


class ThreadQuery(Query):
    nested_fields = {
        'tags': ['id', 'name'],
        'participants': ['email', 'name']
    }

    def __init__(self, query, query_type='and'):
        # TODO[k]: tags have name, id.
        # We exclude the namespace_id.
        attrs = ['id', 'object', 'subject', 'participants', 'tags',
                 'last_message_timestamp', 'first_message_timestamp']
        self._fields = dict((k, None) for k in attrs)

        Query.__init__(self, query, query_type)

        self.apply_weights()

    def apply_weights(self):
        if not self.query or 'all' not in self.query:
            return

        # Arbitrarily assigned boost_score
        if 'weights' not in self.query:
            for f in ['subject', 'snippet', 'participants', 'tags']:
                self._fields[f] = 3
        else:
            self._fields.update(self.query['weights'])
            del self.query['weights']

    def generate(self, min_children=1):
        query_dict = self.convert()

        # TODO[k]:
        # Fix for case self.query is a list i.e. OR-query
        # Fix to support cross Thread/Message field queries
        if self.query.keys()[0] in self._fields or \
                self.query.keys()[0] == 'all':
            return query_dict

        query_dict.update(dict(type='message',
                               min_children=min_children))
        return {'query': dict(has_child=query_dict)}


class BaseSearchAdaptor(object):
    """
    Base adaptor between the Nilas API and Elasticsearch for a single index and
    document type. Subclasses implement the document type specific logic.
    """
    def __init__(self, index_id, doc_type, query_class, log):
        self.index_id = index_id
        self.doc_type = doc_type
        self.query_engine = DSLQueryEngine(query_class)

        self.log = log

        # TODO(emfree): probably want to try to keep persistent connections
        # around, instead of creating a new one each time.
        self._connection = new_connection()


class MessageSearchAdaptor(BaseSearchAdaptor):
    """ Adaptor for the 'message' document type. """
    def __init__(self, index_id, log):
        BaseSearchAdaptor.__init__(self, index_id=index_id, doc_type='message',
                                   query_class=MessageQuery, log=log)

    def index(self, object_repr):
        self._index_document(object_repr, parent=object_repr['thread_id'])

    def bulk_index(self, objects):
        return self._bulk(objects, parent='thread_id')


class ThreadSearchAdaptor(BaseSearchAdaptor):
    """ Adaptor for the 'thread' document type. """
    def __init__(self, index_id, log):
        BaseSearchAdaptor.__init__(self, index_id=index_id, doc_type='thread',
                                   query_class=ThreadQuery, log=log)

    def index(self, object_repr):
        self._index_document(object_repr)

    def bulk_index(self, objects):
        return self._bulk(objects)

    def search(self, query, max_results, offset, sort):
        #MOCK
        return ''
        #MOCK


class NamespaceSearchEngine(object):
    """
    Interface to create and interact with the Elasticsearch datastore
    (i.e. index) for a namespace, identified by the namespace public id.
    """
    MAPPINGS = NAMESPACE_INDEX_MAPPING

    def __init__(self, namespace_public_id):
        self.index_id = namespace_public_id

        # TODO(emfree): probably want to try to keep persistent connections
        # around, instead of creating a new one each time.
        self._connection = new_connection()
        self.log = log.new(component='search', index=namespace_public_id)

        self.create_index()

        self.messages = MessageSearchAdaptor(index_id=namespace_public_id, log=self.log)
        self.threads = ThreadSearchAdaptor(index_id=namespace_public_id, log=self.log)

    def create_index(self):
        """
        Create an index for the namespace. If it already exists,
        re-configure it.
        """

        #MOCK
        return ''
        #MOCK


#Line 46
class SearchEngineError(Exception):
    """ Raised when connecting to the Elasticsearch server fails. """
    pass