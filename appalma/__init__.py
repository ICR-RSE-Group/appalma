# appalma/__init__.py
from .maker import PageStore
from .visuals import PageConfig
from .login import Login
from .cmd import CmdLocal
from .cmd import CmdSSH
from .cmd import CmdSSHLite


try:
    __version__ = version("appalma")
except:
    __version__ = "unknown"