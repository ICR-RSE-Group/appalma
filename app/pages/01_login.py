
from appalma.maker import PageStore
from appalma.login import SlurmLogin


PageStore().add_to_page("cfg")
PageStore().add_to_page("login", SlurmLogin())


