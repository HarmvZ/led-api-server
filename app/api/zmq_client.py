import zmq

from django.conf import settings
# Singleton class as defined in:
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class ZMQClient:
    class __ZMQClient:
        def __init__(self):
            self.context = zmq.Context()
            self.client = self.context.socket(zmq.REQ)
            self.client.connect(settings.SERVER_ENDPOINT)
            self.poll = zmq.Poller()
            self.poll.register(self.client, zmq.POLLIN)

        def perform_request(self, name, **kwargs):
            message = {'action': name, 'kwargs': kwargs}

            sequence = 0
            retries_left = settings.REQUEST_RETRIES
            while retries_left:
                sequence += 1
                self.client.send_pyobj(message)

                expect_reply = True
                while expect_reply:
                    socks = dict(self.poll.poll(settings.REQUEST_TIMEOUT))
                    if socks.get(self.client) == zmq.POLLIN:
                        reply = self.client.recv_pyobj()
                        if not reply:
                            break
                        else:
                            retries_left = settings.REQUEST_RETRIES
                            expect_reply = False
                    else:
                        # Socket is confused. Close and remove it.
                        self.client.setsockopt(zmq.LINGER, 0)
                        self.client.close()
                        self.poll.unregister(self.client)
                        retries_left -= 1
                        if retries_left == 0:
                            print("E: Server seems to be offline, abandoning")
                            break
                        print("I: Reconnecting and resending (%s)" % message)
                        # Create new connection
                        self.client = self.context.socket(zmq.REQ)
                        self.client.connect(settings.SERVER_ENDPOINT)
                        self.poll.register(self.client, zmq.POLLIN)
                        self.client.send_pyobj(message)
                
            return reply

    instance = None

    def __init__(self):
        if not ZMQClient.instance:
            ZMQClient.instance = ZMQClient.__ZMQClient()

    def __getattr__(self, name):
        return getattr(self.instance, name)