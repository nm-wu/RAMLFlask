import datetime
from collections import OrderedDict
from RAMLFlask.rsp_element import Response_Element
from test3.generated.generated_routes import Thread_Search
from RAMLFlask.Generated_Class_Base import Generated_Class_Base
from flask import g, jsonify, request
from flask.ext.restful import reqparse


class Thread_Search():
    class Post(Thread_Search.Post_Base):

        def add_validate_params_handler(self, cust_request):
            return Response_Element()

        def request_handler(self):
            g.parser = reqparse.RequestParser(argument_class=ValidatableArgument)
            args = strict_parse_args(g.parser, self.req.args)

            #MOCK
            data = {
                'query': ''
            }
            #MOCK

            query = data.get('query')

            validate_search_query(query)

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
                results = search_engine.threads.search(query=query, max_results=args.limit,offset=args.offset)
            except SearchEngineError:
                return Response_Element(False, ('Search error', 501))

            return Response_Element(True, (g.encoder.jsonify(results), 200))





#Line 17
class ValidatableArgument(reqparse.Argument):
    def handle_validation_error(self, error):
        raise InputError(str(error))


#Line 18
class InputError(Exception):
    """Raised when bad user input is processed."""
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


def strict_parse_args(parser, raw_args):
    """Wrapper around parser.parse_args that raises a ValueError if unexpected
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


#Line 41
THREAD_MAPPING = {
    'properties': {
        'namespace_id': {'type': 'string'},
        'tags': {'type': 'string'},
        'last_message_timestamp': {'type': 'date', 'format': 'dateOptionalTime'},
        'object': {'type': 'string'},
        'message_ids': {'type': 'string'},
        'snippet': {'type': 'string'},
        'participants': {'type': 'string'},
        'first_message_timestamp': {'type': 'date', 'format': 'dateOptionalTime'},
        'id': {'type': 'string'},
        'subject': {'type': 'string'}
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
        'from': {'type': 'string'},
        'to': {'type': 'string'},
        'cc': {'type': 'string'},
        'bcc': {'type': 'string'},
        'date': {'type': 'string'},
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
    Get a new connection to the Elasticsearch hosts defined in config.
    """

    #MOCK
    return ''
    #MOCK



class DSLQueryEngine(object):
    """
    Generates Elasticsearch DSL queries from API queries.
    Converts Elasticsearch query responses to API responses.
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

        #total = raw_results['total']

        results = []
        for h in raw_results['hits']:
            # TODO[k]: snippet too? with highlighting
            r = dict(relevance=h['_score'],
                     object=h['_source'])

            results.append(r)

        return results


class BaseSearchAdaptor(object):
    """
    Adapter between the API and an Elasticsearch backend, for a single index
    and document type.
    """
    def __init__(self, index_id, doc_type, query_class):
        # TODO(emfree): probably want to try to keep persistent connections
        # around, instead of creating a new one each time.
        self._connection = new_connection()
        self.index_id = index_id
        self.doc_type = doc_type

        self.query_engine = DSLQueryEngine(query_class)


class Query(object):
    # TODO[k]: Document more here
    """ Representation of an Elasticsearch DSL query. """
    def __init__(self, query, query_type='and'):
        self.query = query
        self.query_type = query_type

    def convert(self):
        query_dict = self.convert_and() if self.query_type == 'and' else \
            self.convert_or()
        return dict(query={'bool': query_dict})

    def convert_or(self):
        d_list = [self.__class__(q) for q in self.query]

        # TODO[k]: DO SOMETHING WITH d_list!
        return d_list

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
            field_dict = {field: dict(query=' '.join(v for v in value))}
        else:
            field_dict = {field: dict(query=value, type='phrase')}

        return field_dict

    def match(self, field):
        """ Generate an Elasticsearch match or match_phrase query. """
        field_dict = self._field_dict(field, self.query[field])
        return dict(match=field_dict)

    def multi_match(self, field, boost=True):
        """
        Generate an Elasticsearch multi_match query.
        Simple matches and phrase matches are supported.
        Boosting is applied by default, set boost=False to score all field
        matches equally.
        """
        assert field == 'all' and self._fields

        if boost:
            return self._boosted_multi_match(field)
        else:
            return self._simple_multi_match(field)

    def _simple_multi_match(self, field):
        d = dict(fields=self._fields.keys())

        field_dict = self._field_dict(field, self.query[field])
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def _boosted_multi_match(self, field):
        boosted_fields = []
        for f in self._fields:
            multiplier = self._fields.get(f)
            if multiplier:
                boosted_fields.append('{}^{}'.format(f, multiplier))
            else:
                boosted_fields.append(f)

        d = dict(fields=boosted_fields)

        field_dict = self._field_dict(field, self.query[field])
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def match_all(self):
        return dict(query={'match_all': {}})

    def generate(self):
        raise NotImplementedError


class MessageQuery(Query):
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
        if not self.query or not 'all' in self.query:
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


class Query(object):
    # TODO[k]: Document more here
    """ Representation of an Elasticsearch DSL query. """
    def __init__(self, query, query_type='and'):
        self.query = query
        self.query_type = query_type

    def convert(self):
        query_dict = self.convert_and() if self.query_type == 'and' else \
            self.convert_or()
        return dict(query={'bool': query_dict})

    def convert_or(self):
        d_list = [self.__class__(q) for q in self.query]

        # TODO[k]: DO SOMETHING WITH d_list!
        return d_list

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
            field_dict = {field: dict(query=' '.join(v for v in value))}
        else:
            field_dict = {field: dict(query=value, type='phrase')}

        return field_dict

    def match(self, field):
        """ Generate an Elasticsearch match or match_phrase query. """
        field_dict = self._field_dict(field, self.query[field])
        return dict(match=field_dict)

    def multi_match(self, field, boost=True):
        """
        Generate an Elasticsearch multi_match query.
        Simple matches and phrase matches are supported.
        Boosting is applied by default, set boost=False to score all field
        matches equally.
        """
        assert field == 'all' and self._fields

        if boost:
            return self._boosted_multi_match(field)
        else:
            return self._simple_multi_match(field)

    def _simple_multi_match(self, field):
        d = dict(fields=self._fields.keys())

        field_dict = self._field_dict(field, self.query[field])
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def _boosted_multi_match(self, field):
        boosted_fields = []
        for f in self._fields:
            multiplier = self._fields.get(f)
            if multiplier:
                boosted_fields.append('{}^{}'.format(f, multiplier))
            else:
                boosted_fields.append(f)

        d = dict(fields=boosted_fields)

        field_dict = self._field_dict(field, self.query[field])
        d.update(field_dict[field])
        d['type'] = 'most_fields'

        return dict(multi_match=d)

    def match_all(self):
        return dict(query={'match_all': {}})

    def generate(self):
        raise NotImplementedError


class ThreadQuery(Query):
    def __init__(self, query, query_type='and'):
        # TODO[k]: tags have name, id.
        # We exclude the namespace_id.
        attrs = ['id', 'object', 'subject', 'participants', 'tags',
                 'last_message_timestamp', 'first_message_timestamp']
        self._fields = dict((k, None) for k in attrs)

        Query.__init__(self, query, query_type)

        self.apply_weights()

    def apply_weights(self):
        if not self.query or not 'all' in self.query:
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


class MessageSearchAdaptor(BaseSearchAdaptor):
    def __init__(self, index_id):
        BaseSearchAdaptor.__init__(self, index_id=index_id, doc_type='message', query_class=MessageQuery)

    def index(self, object_repr):
        """(Re)index a message with API representation `object_repr`."""
        self._index_document(object_repr, parent=object_repr['thread_id'])


class ThreadSearchAdaptor(BaseSearchAdaptor):
    def __init__(self, index_id):
        BaseSearchAdaptor.__init__(self, index_id=index_id, doc_type='thread', query_class=ThreadQuery)

    def index(self, object_repr):
        """(Re)index a thread with API representation `object_repr`."""
        self._index_document(object_repr)

    #MOCK
    def search(self, query, max_results, offset):
        return ''
    #MOCK


class NamespaceSearchEngine(object):
    """
    Interface to create and interact with the Elasticsearch datastore
    (i.e. index) for a namespace, identified by the namespace public id.
    """
    MAPPINGS = NAMESPACE_INDEX_MAPPING

    def __init__(self, namespace_public_id):
        # TODO(emfree): probably want to try to keep persistent connections
        # around, instead of creating a new one each time.
        self.index_id = namespace_public_id

        self._connection = new_connection()
        self.create_index()

        self.messages = MessageSearchAdaptor(index_id=namespace_public_id)
        self.threads = ThreadSearchAdaptor(index_id=namespace_public_id)

    def create_index(self):
        #MOCK
        pass
        #MOCK


#Line 43
class SearchEngineError(Exception):
    """
    Exception raised if an error occurs connecting to the Elasticsearch
    backend.
    """
    pass