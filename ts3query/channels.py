from . import utils

class TS3Channels():
    def __init__(self, resp):
        self.chanlist = [{"cid":0, "channel_name":"Root", "children":[]}]

        # this is nasty, since TS3Response is actually a mapping.
        # json.dumps needs this, though: http://bugs.python.org/issue20774
        for c in resp.res:
            c["children"] = []
            self.addchan(self.chanlist, c)

    def addchan(self, tree, channel):
        if tree[-1]["cid"] == channel["pid"]:
            tree[-1]["children"].append(channel)
        else:
            self.addchan(tree[-1]["children"], channel)

    def __str__(self):
        return utils.tojson(self.chanlist, True)
