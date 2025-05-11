import streamlit as st
from appalma.visuals import PageConfig
from appalma.maker import PageStore
from appalma.browse import BrowseView


PageStore().add_to_page("cfg", PageConfig())

ssh = PageStore().ssh_success()
if ssh:
    PageStore().add_to_page("bv", BrowseView(ssh,filematch = "*.out", folder="/home/ralcraft", displays=["code","text","info","df", "plot"]))
else:
    st.error("SSH Connection has not been made, please log on")



