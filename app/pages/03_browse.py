
from appalma.maker import PageStore
from appalma.cmd import CmdSSHLite
from appalma.cmd import CmdSSH


PageStore().add_to_page("cfg")
ssh = PageStore().get_global("ssh")
#PageStore().add_to_page("browse", CmdSSHLite(ssh))
PageStore().add_to_page("browse", CmdSSH(ssh))


