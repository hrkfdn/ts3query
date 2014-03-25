import json # required for prettyprint

import utils

class TS3Response():
    def __init__(self, error, response=None):
        self.responsedict = {}

        for v in error.split(" "):
            if v.startswith("id="):
                self.errorid = v[3::]
            elif v.startswith("msg="):
                self.errormsg = utils.unescape(v[4::])

        # some responses only contain a status code
        if response is not None:
            for v in response.split(" "):
                s = v.split("=", 1)
                if len(s) > 1:
                    self.responsedict[s[0]] = utils.unescape(s[1])
                else:
                    self.responsedict[s[0]] = None

    def printresp(self):
        print("Error ID:", self.errorid, " - Error Message:", self.errormsg)
        print(json.dumps(self.responsedict, sort_keys=True, indent=4))
