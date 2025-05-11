import streamlit as st
from appalma.maker import PageStore
from appalma.cmd import CmdSSH


PageStore().add_to_page("cfg")
ssh = PageStore().get_global("ssh")
tabRadio, tabList,tabCode,tabDf,tabText,tabButton = st.tabs(["tabRadio", "tabList","tabCode","tabDf","tabText", "tabButton"])
with tabRadio:    
    PageStore().add_to_page("browse1", CmdSSH(ssh,output="radio"))
with tabList:    
    PageStore().add_to_page("browse2", CmdSSH(ssh,output="list"))
with tabCode:
    PageStore().add_to_page("browse3", CmdSSH(ssh,output="code"))
with tabDf:
    PageStore().add_to_page("browse4", CmdSSH(ssh,output="df"))
with tabText:
    PageStore().add_to_page("browse5", CmdSSH(ssh,output="text"))
with tabButton:
    PageStore().add_to_page("browse6", CmdSSH(ssh,btton="Click me",output="text"))


