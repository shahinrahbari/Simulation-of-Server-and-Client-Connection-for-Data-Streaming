import sys
import threading
import random

from twisted.internet import protocol, endpoints



class Client(protocol.Protocol):

    def __init__(self, name='', stream_port=0, stream_handler=None, starter=False):
        self.name = name
        self.stream_requested = False
        self.stream_port = stream_port
        self.stream_peer = []
        self.stream_handler = stream_handler
        self.starter = starter

    def connectionMade(self):
        self.transport.write('Reg#' + self.name)

    def sendMsg(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        print 'Data Received: ' + data
        cmd, args = data.split('#', 1)

        if cmd == 'Reg':
            self.handle_reg(args)
        if cmd == 'StreamReq':
            self.handle_stream_req(args)

    def handle_reg(self, args):
        res = args.split('#')[0]
        if res == 'NOK':
            print args.split('#')[1]
        elif res == 'OK':
            if self.starter:
                self.transport.write('StreamReq#' + self.name)

    def handle_stream_req(self, args):
        first_arg = args.split('#')[0]
        if first_arg == 'NOK':
            self.stream_requested = False
        elif first_arg == 'OK':
            self.stream_peer = [args.split('#')[1], int(args.split('#')[2])]
            self.stream_handler.peer = self.stream_peer

            if self.starter:
                stream_handler.transport.write('Haha', (self.stream_peer[0], self.stream_peer[1]))
                stream_handler.transport.write('Hoho', (self.stream_peer[0], self.stream_peer[1]))
                stream_handler.transport.write('Hihi', (self.stream_peer[0], self.stream_peer[1]))
                stream_handler.transport.write('EhemEhem', (self.stream_peer[0], self.stream_peer[1]))

        else:
            i = raw_input('Accept stream request %s? (y/n) ')
            if i == 'y':
                self.transport.write('StreamReq#OK#%d' % self.stream_port)
            else:
                self.transport.write('StreamReq#NOK')


class StreamHandler(protocol.DatagramProtocol):

    def __init__(self, peer=[], starter=False):
        self.peer = peer
        self.starter = starter

    def startProtocol(self):
        protocol.DatagramProtocol.startProtocol(self)

        if self.starter:
            self.transport.write('haha', (self.peer[0], self.peer[1]))

    def datagramReceived(self, data, (host, port)):
        print data
        if self.peer:
            self.transport.write(data, (self.peer[0], self.peer[1]))


if __name__ == '__main__':
    from twisted.internet import reactor

    port = random.randint(20000, 50000) # UDP port
    stream_handler = StreamHandler()
    point = endpoints.TCP4ClientEndpoint(reactor, sys.argv[1], int(sys.argv[2]))
    if len(sys.argv) > 4 and sys.argv[4] == 'starter':
        d = endpoints.connectProtocol(point, Client(name=sys.argv[3], stream_port=port, stream_handler=stream_handler, starter=True))
    else:
        d = endpoints.connectProtocol(point, Client(name=sys.argv[3], stream_port=port, stream_handler=stream_handler))

    reactor.listenUDP(port, stream_handler)
    reactor.run()
