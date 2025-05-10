
from appalma.maker import PageStore
from appalma.cmd import CmdLocal


PageStore().add_to_page("cfg")
PageStore().add_to_page("local", CmdLocal())


