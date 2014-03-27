import json # required for prettyprint

from . import utils

class TS3Response():
    def __init__(self, error, response=None):
        self.res = {"response": []}
        for v in error.split(" "):
            if v.startswith("id="):
                self.res["errorid"] = int(v[3::])
            elif v.startswith("msg="):
                self.res["errormsg"] = utils.unescape(v[4::])

        # some responses only contain a status code
        if response is not None:
            r = response.split("|")
            for chunk in r:
                tempdict = {}
                for v in chunk.split(" "):
                    s = v.split("=", 1)
                    if len(s) > 1:
                        tempdict[s[0]] = utils.unescape(s[1])
                    else:
                        tempdict[s[0]] = None
                self.res["response"].append(tempdict)

    @property
    def ok(self):
        if 'errorid' in self.res:
            return self.res["errorid"] == 0
        else:
            return False

    def tojson(self, pretty=False):
        idt = 4 if pretty else None
        return json.dumps(self.res, sort_keys=True, indent=idt)
                    
    def printresp(self):
        print(self.tojson(True))
