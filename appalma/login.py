import streamlit as st
from .cmd import CmdSSH
from .maker import PageStore
from pyalma import SshClient


class Login():
    """
    Login for ssh based login
    """

    def __init__(self, server="alma.icr.ac.uk", username=None, password=None, sftp="alma-app.icr.ac.uk", port=22):
        self.server = server
        self.username = username
        self.password = password
        self.sftp = sftp
        self.port = port
        self.ssh = None
        self.cmd = None        
                                    
    def play(self):
        cols = st.columns([5,1])
        with cols[0]:
            tabUser, tabServer = st.tabs(["User", "(Server)"])
            with tabUser:
                cols1 = st.columns([2,2])    
                with cols1[0]:        
                    self.username = st.text_input("Username:", self.username, key="username")
                with cols1[1]:
                    self.password = st.text_input("Password:", self.password, type="password", key="password")
            with tabServer:
                cols2 = st.columns([2,2])    
                with cols2[0]:
                    self.server = st.text_input("Remote server:", self.server)
                with cols2[1]:
                    self.sftp = st.text_input("SFTP server:", self.sftp)                
        if st.button("Connect"):            
            self.ssh = SshClient(server=self.server, username=self.username, password=self.password, port=self.port)                  
            if self.ssh is not None:            
                PageStore().set_global("ssh", self.ssh)
            self.cmd = CmdSSH(self.ssh)
            self.cmd.play()

        

    