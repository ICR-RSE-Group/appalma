# appalma/__init__.py
from .maker import PageStore
from .visuals import PageConfig
from .pages import Login
from .cmd import CmdLocal
from .cmd import CmdSSH


try:
    __version__ = version("appalma")
except:
    __version__ = "unknown"