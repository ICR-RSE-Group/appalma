
from appalma.maker import PageStore
from appalma.pages import Login


PageStore().add_to_page("cfg")
PageStore().add_to_page("login", Login())


