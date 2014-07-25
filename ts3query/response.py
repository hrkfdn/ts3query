import json # required for prettyprint

from collections.abc import Mapping

from . import utils

class TS3Response(Mapping):
    def __init__(self, error, response=None):
        self.res = []
        self.errorid = -1
        self.errormsg = "ERROR: TS3Response empty."

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
                    key = s[0]
                    if len(s) > 1:
                        val = utils.unescape(s[1])
                        try:
                            if "name" in key:
                                tempdict[key] = val
                            else:
                                tempdict[key] = int(val)
                        except ValueError:
                            tempdict[key] = val
                    else:
                        tempdict[key] = None
                self.res.append(tempdict)
    @property
    def ok(self):
        return self.errorid == 0

    def __str__(self):
        return utils.tojson(self.res, True)

    def __repr__(self):
        return utils.tojson(self.res, False)

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
