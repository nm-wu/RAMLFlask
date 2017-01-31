class Response_Element(object):
    """Response object for usage in various generated and handwritten classes"""

    def __init__(self, proceed=True, resp=('', 200)):
        self.proceed = proceed
        self.response = resp