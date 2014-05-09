from . import utils

class TS3Clients():
    def __init__(self, resp):
        # this is nasty, since TS3Response is actually a mapping.
        # json.dumps needs this, though: http://bugs.python.org/issue20774
        self.clientlist = resp.res

    def listinchannel(self, cid):
        clients = []
        for client in self.clientlist:
            if cid == client["cid"]:
                clients.append(client)
        return clients

    def __str__(self):
       return utils.tojson(self.clientlist, True)
