import socket
import threading

from .response import TS3Response
from .channels import TS3Channels
from .clients import TS3Clients
from . import utils

class TS3Connection():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.lock = threading.Lock()

        self.keepalivetimer = None
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.sf = self.socket.makefile(mode="r", buffering=1, encoding="utf-8", newline="\r")

        if self.sf.readline().strip() != "TS3":
            raise IOError("Opposite party did not send \"TS3\" message.")
        else:
            self.sf.readline() # flush welcome message
            self.connected = True

    def disconnect(self):
        if self.keepalivetimer is not None:
            self.keepalivetimer.cancel()
        self.socket.close()
        self.connected = False

    def reconnect(self):
        self.disconnect()
        self.connect()
        if hasattr(self, 'user') and hasattr(self, 'password'):
            self.login(self.user, self.password)

    def dokeepalive(self, interval):
        if self.connected:
            # this command does not require special priviliges and can therefore be used
            # for dirty keepalive requests
            self.sendcmd("whoami")
            self.keepalivetimer = threading.Timer(interval, self.dokeepalive, args=[interval])
            self.keepalivetimer.start()

    def keepalive(self, interval=60):
        self.keepalivetimer = threading.Timer(interval, self.dokeepalive, args=[interval])
        self.keepalivetimer.start()

    def getresponse(self):
        try:
            firstline = self.sf.readline()
        except socket.error:
            return None

        if len(firstline) == 0:
            return None
        elif firstline.startswith("error"):
            return TS3Response(firstline.strip())
        else:
            return TS3Response(self.sf.readline().strip(), firstline.strip())

    def send(self, string):
        cmdterminated = string + "\n"
        try:
            sent = self.socket.send(cmdterminated.encode())
        except ConnectionError as e:
            print("In send(): connection error!")

    def sendcmd(self, command, **kwargs):
        with self.lock:
            buf = command
            for key in kwargs:
                buf += " " + key
                buf += "=" + kwargs[key]
            self.send(buf)

            response = self.getresponse()
            return response

    def login(self, user, password):
        # save in case we need to reconnect
        self.user = user
        self.password = password

        u_esc = utils.escape(user)
        p_esc = utils.escape(password)
        return self.sendcmd("login", client_login_name=user, client_login_password=password)

    def getchannels(self, parameters=None):
        if parameters:
            res = self.sendcmd("channellist " + parameters)
        else:
            res = self.sendcmd("channellist")

        if res.ok:
            return TS3Channels(res)
        else:
            return None

    def getclients(self, parameters=None):
        if parameters:
            res = self.sendcmd("clientlist " + parameters)
        else:
            res = self.sendcmd("clientlist")

        if res.ok:
            return TS3Clients(res)
        else:
            return None

    def getserverinfo(self):
        res = self.sendcmd("serverinfo")
        if res.ok:
            return res[0]["virtualserver_name"]
        else:
            return None
