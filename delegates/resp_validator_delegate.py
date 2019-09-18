from RAMLFlask.rsp_element import Response_Element

class Response_Validator_Delegate(object):
    """Delegation class"""

    def handle_delegation(self, request):
        return Response_Element()