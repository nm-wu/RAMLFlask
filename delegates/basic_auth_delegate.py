from RAMLFlask.rsp_element import Response_Element

class Basic_Auth_Delegate(object):
    """Delegation class"""

    def handle_delegation(self, request):
        return Response_Element()