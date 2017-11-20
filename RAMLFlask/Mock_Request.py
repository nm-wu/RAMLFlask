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