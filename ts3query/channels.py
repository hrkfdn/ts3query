class TS3Channels():
    def __init__(self, resp):
        self.chanlist = []
        for c in resp.res["response"]:
            self.chanlist.append(c["channel_name"])
