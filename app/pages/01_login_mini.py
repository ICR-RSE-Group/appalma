from appalma.visuals import PageConfig
from appalma.maker import PageStore
from appalma.login import SlurmLogin


PageStore().add_to_page("cfg", PageConfig())
PageStore().add_to_page("login-mini", SlurmLogin(minimal=True))


