# appalma/__init__.py
from .maker import PageStore
from .visuals import PageConfig
from .login import SlurmLogin
from .cmd import CmdLocal
from .cmd import CmdSSH
from .browse import BrowseView


try:
    __version__ = version("appalma")
except:
    __version__ = "unknown"