import socket

from .response import TS3Response
from . import utils

class TS3Connection():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.sf = self.socket.makefile(mode="r", buffering=1, encoding="utf-8", newline="\r")

        if self.sf.readline().strip() != "TS3":
            raise IOError("Opposite party did not send \"TS3\" message.")
        else:
            self.sf.readline() # flush welcome message

    def getresponse(self):
        firstline = self.sf.readline().strip()
        if firstline.startswith("error"):
            return TS3Response(firstline)
        else:
            return TS3Response(self.sf.readline().strip(), firstline)

    def send(self, string):
        cmdterminated = string + "\n"
        self.socket.send(cmdterminated.encode())

    def sendcmd(self, command, **kwargs):
        buf = command
        for key in kwargs:
            buf += " " + key
            buf += "=" + kwargs[key]
        self.send(buf)

        response = self.getresponse()
        response.printresp()
        return response

    def login(self, user, password):
        u_esc = utils.escape(user)
        p_esc = utils.escape(password)
        self.sendcmd("login", client_login_name=user, client_login_password=password)
