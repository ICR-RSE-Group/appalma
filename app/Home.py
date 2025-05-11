import streamlit as st
from appalma.maker import PageStore
from appalma.visuals import PageConfig


PageStore().add_to_page("cfg", PageConfig())
st.write(
    """
    **App-Alma**: A python library for making it simple to create streamlit apps for managing your SSH connections and commands. 
    This is a simple demonstration of some of the widgets.  
    
    The github repository is [here: appalma](https://github.com/ICR-RSE-Group/appalma)
    """
)


