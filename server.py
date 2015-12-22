from twisted.internet import protocol, reactor, endpoints



class Server(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.name = ''

    def connectionMade(self):
        self.stream_addr = [self.transport.getPeer().host, 0]

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        print 'Data Received: ' + data
        cmd, args = data.split('#', 1)

        if cmd == 'Reg':
            self.handle_reg(args)
        elif cmd == 'StreamReq':
            self.handle_stream_req(args)

    def handle_reg(self, args):
        name = args

        if name in self.factory.clients:
            self.transport.write('Reg#NOK#Name Exists.')
        else:
            self.name = name
            self.factory.clients[name] = self
            self.transport.write('Reg#OK')

    def handle_stream_req(self, args):
        first_arg = args.split('#')[0]
        if first_arg == 'NOK':
            self.factory.stream_res += 1
        elif first_arg == 'OK':
            self.factory.stream_res += 1
            self.stream_addr[1] = int(args.split('#')[1])
            self.factory.stream_chain.append(self)
        else:
            if self.factory.stream_active:
                self.transport.write('StreamReq#NOK#A stream is already active.')
            else:
                self.factory.stream_active = True
                self.factory.stream_chain.append(self)
                for k in self.factory.clients:
                    if k != self.name:
                        self.factory.clients[k].transport.write('StreamReq#' + first_arg)

        if self.factory.stream_res == len(self.factory.clients) - 1:
            print 'Everyone responded for streaming, making chain.'
            for i in range(len(self.factory.stream_chain) - 1, 0, -1):
                print i, self.factory.stream_chain[i - 1].name
                self.factory.stream_chain[i - 1].stream_peer = self.factory.stream_chain[i].stream_addr
                self.factory.stream_chain[i - 1].transport.write(
                    'StreamReq#OK#%s#%d' % (
                        self.factory.stream_chain[i].stream_addr[0],
                        self.factory.stream_chain[i].stream_addr[1]
                    )
                )


class ServerFactory(protocol.Factory):

    def __init__(self):
        self.clients = {}
        self.stream_active = False
        self.stream_chain = []
        self.stream_res =(self, addr):
        return Server(self)

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:9669").listen(ServerFactory())
    reactor.run()
