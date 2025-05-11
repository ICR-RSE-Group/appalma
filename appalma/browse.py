import streamlit as st
from .cmd import CmdSSH
import pandas as pd
from io import StringIO



class BrowseView():
    """
    Login for ssh based login
    """

    def __init__(self, ssh, filematch, folder, displays=["text"]):
        self.ssh = ssh
        self.filematch = filematch
        self.folder = folder        
        self.txt_dir = f"find {self.folder} -type f -maxdepth 1 -name '{self.filematch}'"
        self.cmd_dir = None
        self.cmd_file = None
        self.txt_contents = ""        
        self.displays = displays # this can be a list of displays which are shown on tabs text, code, info, df, plot (plot not implemented yet!)
        self.files_list = []
                                            
    def play(self):
        cols = st.columns([2,5])
        with cols[1]:
            st.write(f"folder={self.folder} filematch={self.filematch}")            
        with cols[0]:
            if st.button("List files"):            
                self.cmd_dir = CmdSSH(self.ssh, cmd=self.txt_dir, output="list", spinner="Retrieving files")
                self.cmd_dir.play()            
                # remove hpcuser from the list
                
                if len(self.cmd_dir.result) > 0:
                    # retrieve user lists on this basis
                    # remove the path from the result                        
                    # replace all the paths in the path with ""
                    self.files_list = [x.replace(self.folder, "") for x in self.cmd_dir.result]                    
                    self.sel_file = self.files_list[0]                                        
                    self.txt_contents = self.ssh.read_file(self.folder + self.sel_file)
                    # get file stats
                    self.cmd_file = CmdSSH(self.ssh, cmd=f"stat {self.folder + self.sel_file}", output="none", spinner="stat")
                    self.cmd_file.play()
                                                                                                                                                                                                    
        if self.cmd_dir:
            if not self.cmd_dir.ok:
                st.error(f"FAILED: {self.cmd_dir.error}")
            else:                                                
                def change_sel_file():
                    self.sel_file = st.session_state.file
                    # retrieve user lists on this basis                    
                    self.txt_contents = self.ssh.read_file(self.folder + self.sel_file)
                    # get file stats
                    self.cmd_file = CmdSSH(self.ssh, cmd=f"stat {self.folder + self.sel_file}", output="none", spinner="stat")
                    self.cmd_file.play()
                                                                                                    
                # find index of selected group                
                with cols[0]:
                    self.sel_file = st.radio("Select a file:", self.files_list, index=0, key="file",on_change=change_sel_file)

                with cols[1]:
                    #st.write(f"Selected file = {self.sel_file}")
                    tabs = st.tabs(self.displays)
                    for t in range(len(tabs)):
                        with tabs[t]:                                                        
                            if self.displays[t] == "text":                                
                                st.text(self.txt_contents)
                            elif self.displays[t] == "code":
                                st.code(self.txt_contents)
                            elif self.displays[t] == "info":                                
                                st.code(self.cmd_file.result)
                            elif self.displays[t] in ["df","plot"]:
                                try:
                                    df = pd.read_csv(StringIO(self.txt_contents))                                    
                                    if self.displays[t] == "df":
                                        st.dataframe(df)                                
                                    elif self.displays[t] == "plot":
                                        keys = df.columns
                                        cols = st.columns(3)
                                        with cols[0]:
                                            x = st.selectbox("X axis", keys)
                                        with cols[1]:
                                            y = st.selectbox("Y axis", keys)
                                        with cols[2]:
                                            z = st.selectbox("Z axis", keys)
                                        
                                        
                                        st.warning("Plot not implemented yet!")
                                except Exception as e:
                                    st.error(f"Error parsing output: {e}")                                
                            else:
                                st.error(f"Unknown display type: {self.displays[t]}")
                    
                
                


                
                
       

            

            
                
        
        

    