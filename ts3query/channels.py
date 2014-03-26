class TS3Channels():
    def __init__(self, resp):
        self.chanlist = [{"cid":"0", "channel_name":"Root", "children":[]}]
        for c in resp.res["response"]:
            c["children"] = []
            self.addchan(self.chanlist, c)

    def addchan(self, tree, channel):
        if tree[-1]["cid"] == channel["pid"]:
            tree[-1]["children"].append(channel)
        else:
            self.addchan(tree[-1]["children"], channel)

