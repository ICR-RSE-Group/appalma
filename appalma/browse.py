import streamlit as st
from .cmd import CmdSSHLite



class BrowseView():
    """
    Login for ssh based login
    """

    def __init__(self, ssh, filematch):
        self.ssh = ssh
        self.filematch = filematch
        self.lite = CmdSSHLite(ssh, filematch)
        
                    
    def play(self):
        cols = st.columns([1,8])
        self.filematch = f"ls -a"
        str_msg, str_error = self.lite.play()
        st.write(str_msg)
        st.write(str_error)
        
       

            

            
                
        
        

    