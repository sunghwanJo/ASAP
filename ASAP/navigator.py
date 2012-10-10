from ASAP.exceptions import ProtocolNotFoundError
from ASAP.views import *

class Navigator(object):
    protocols = dict(test=lambda request: dict())
    
    @classmethod
    def get_view(cls, protocol):
        view = cls.protocols.get(protocol, None)
        if view == None:
            raise ProtocolNotFoundError(protocol)
        return view
