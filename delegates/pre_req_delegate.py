from RAMLFlask.rsp_element import Response_Element

class Pre_Req_Delegate(object):
    """Delegation class"""

    def handle_delegation(self, request):
        return Response_Element()