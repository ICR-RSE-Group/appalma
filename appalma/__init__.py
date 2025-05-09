# appalma/__init__.py
from .pages import Login

try:
    __version__ = version("appalma")
except:
    __version__ = "unknown"