import json # required for prettyprint

from collections.abc import Mapping

from . import utils

class TS3Response(Mapping):
    def __init__(self, error, response=None):
        self.res = []
        self.errorid = -1
        self.errormsg = "TS3Response not initialized."

        for v in error.split(" "):
            if v.startswith("id="):
                self.errorid = int(v[3::])
            elif v.startswith("msg="):
                self.errormsg = utils.unescape(v[4::])

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
                self.res.append(tempdict)
    @property
    def ok(self):
        return self.errorid == 0

    def __str__(self):
        return self.tojson(True)

    def __repr__(self):
        return self.tojson(False)

    def tojson(self, pretty=False):
        idt = 4 if pretty else None
        return json.dumps(self.res, sort_keys=True, indent=idt)
                    
    def printresp(self):
        print(self.tojson(True))

    # implementation of Mapping abstract methods
    def __getitem__(self, key):
        return self.res[key]

    def __setitem__(self, key, value):
        self.res[key] = value

    def __delitem__(self, key):
        del self.res[key]

    def __iter__(self):
        return iter(self.res)

    def __len__(self):
        return len(self.res)
