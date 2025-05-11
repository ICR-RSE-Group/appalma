import streamlit as st
from appalma.maker import PageStore
from appalma.browse import BrowseView


PageStore().add_to_page("cfg")
ssh = PageStore().get_global("ssh")

PageStore().add_to_page("bv", BrowseView(ssh,filematch = "*.out", folder="/home/ralcraft", displays=["code","text","info","df", "plot"]))
# bash: find all files in the current directory ending in out


