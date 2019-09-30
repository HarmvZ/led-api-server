import zmq
# Singleton class as defined in:
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class ZMQClient:
    class __ZMQClient:
        def __init__(self):
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            self.socket.connect('tcp://zmq:5566')

        def perform_request(self, name, **kwargs):
            message = {'action': name, 'kwargs': kwargs}
            self.socket.send_pyobj(message)
            result = self.socket.recv_pyobj()
            return result

    instance = None

    def __init__(self):
        if not ZMQClient.instance:
            ZMQClient.instance = ZMQClient.__ZMQClient()

    def __getattr__(self, name):
        return getattr(self.instance, name)