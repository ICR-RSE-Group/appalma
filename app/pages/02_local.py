from appalma.visuals import PageConfig
from appalma.maker import PageStore
from appalma.cmd import CmdLocal


PageStore().add_to_page("cfg", PageConfig())
PageStore().add_to_page("local", CmdLocal())


