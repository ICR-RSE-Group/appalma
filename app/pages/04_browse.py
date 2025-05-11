import streamlit as st
from appalma.visuals import PageConfig
from appalma.maker import PageStore
from appalma.browse import BrowseView


PageStore().add_to_page("cfg", PageConfig())

ssh = PageStore().ssh_success()
if ssh:
    PageStore().add_to_page("bv", BrowseView(ssh,filematch = "*.out", 
                                             folder_key="inputs_working", 
                                             displays=["code","text","info","df", "plot"],
                                             edittable=True))
else:
    st.error("SSH Connection has not been made, please log on")



