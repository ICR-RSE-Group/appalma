import streamlit as st
from appalma.visuals import PageConfig
from appalma.maker import PageStore
from appalma.settings import Settings


PageStore().add_to_page("cfg", PageConfig())
ssh = PageStore().ssh_success()
if ssh:    
    scratch = PageStore().get_global("my_scratch")
    home = PageStore().get_global("my_home")        
    sts = Settings(
    {
        "inputs":{"working":scratch,"home":home},
        "outputs":{"results":scratch,"home":home}
    })
    PageStore().add_to_page("settings", sts)
else:
    st.error("SSH Connection has not been made, please log on")


