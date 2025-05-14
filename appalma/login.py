import streamlit as st
from .cmd import CmdSSH
from .maker import PageStore
from pyalma import SshClient


class SlurmLogin():
    """
    Login for ssh based login
    """

    def __init__(self, server="alma.icr.ac.uk", username=None, password=None, sftp="alma-app.icr.ac.uk", minimal=False,port=22):
        self.server = server
        self.username = username
        self.password = password
        self.sftp = sftp
        self.port = port
        self.minimal = minimal
        self.ssh = None
        self.cmd_group = None
        self.cmd_users = None
        
        self.removes = "hpcuser"
        self.scratch = "/data/scratch"
        self.known_groups = {"infotech": "/data/scratch/DCO/DIGOPS/SCIENCOM",
                             "dbcdobcag":"/data/scratch/DBC/UBCN/BCRBIOIN",
                             "dgershadg":"/data/scratch/DGE/DUDGE/MOPOPGEN",}
        
        self.my_scratch = ""
        self.my_home = ""
        self.my_group = ""
        self.my_users = []
        
                                    
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
        with st.spinner("Logging in", show_time=True):
            if st.button("Connect"):            
                self.ssh = SshClient(server=self.server, username=self.username, password=self.password, port=self.port)                  
                if self.ssh is not None:            
                    PageStore().set_global("ssh", self.ssh)
                                                                    
                # A set of commands to ascertain groups and usrs on slurm
                cmd_for_group = f"sacctmgr list association user={self.username} format=Account -P | tail -n +2"
                self.cmd_group = CmdSSH(self.ssh, cmd=cmd_for_group, output="list", spinner="Retrieving users's groups")
                self.cmd_group.play()
                # remove hpcuser from the list
                self.cmd_group.result = [x for x in self.cmd_group.result if x not in self.removes]
                

                if len(self.cmd_group.result) > 0:
                    # we know the group so we can get the paths and user lists     
                    self.my_group = self.cmd_group.result[0]
                    self.my_home = f"/home/{self.username}"
                    if self.my_group in self.known_groups:
                        self.my_scratch = f"{self.known_groups[self.my_group]}/{self.username}"
                    else:
                        self.my_scratch = f"{self.scratch}/{self.my_group}"
                    
                    if not self.minimal:
                        # retrieve user lists on this basis
                        cmd_for_users = f"sacctmgr list association account={self.my_group} format=User -P"
                        self.cmd_users = CmdSSH(self.ssh, cmd=cmd_for_users, output="list", spinner="Retrieving users's colleagues")
                        self.cmd_users.play()
                        if self.cmd_users.ok:
                            self.my_users = self.cmd_users.result
                    
                    
        if self.cmd_group:
            if not self.cmd_group.ok:
                st.error(f"FAILED: {self.cmd_group.error}")
            else:
                st.success("Connected to server")
                
                
                                                
                def change_sel_group():
                    self.my_group = st.session_state.group                
                    # retrieve user lists on this basis
                    if not self.minimal:
                        cmd_for_users = f"sacctmgr list association account={self.my_group} format=User -P"
                        self.cmd_users = CmdSSH(self.ssh, cmd=cmd_for_users, output="list", spinner="Retrieving users's colleagues")
                        self.cmd_users.play()
                        if self.cmd_users.ok:
                            self.my_users = self.cmd_users.result

                # find index of selected group                
                self.my_group = st.radio("Select a group:", self.cmd_group.result, index=0, key="group",on_change=change_sel_group)
                st.write(f"Selected group = {self.my_group}")
                st.write(f"Home path = {self.my_home}")
                st.write(f"Scratch path = {self.my_scratch}")
                PageStore().set_global("my_group", self.my_group)
                PageStore().set_global("my_home", self.my_home)
                PageStore().set_global("my_scratch", self.my_scratch)

                                                                                                            
                
                if not self.minimal:
                    st.write(f"Colleagues = {self.my_users}")                                        
                    PageStore().set_global("my_users", self.my_users)



                
                
            

        

    