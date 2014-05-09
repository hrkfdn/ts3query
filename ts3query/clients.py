class TS3Clients():
    def __init__(self, resp):
        self.clientlist = resp

    def listinchannel(self, cid):
        clients = []
        for client in self.clientlist:
            if cid == int(client["cid"]):
                clients.append(client)
        return clients
