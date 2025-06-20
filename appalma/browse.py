import streamlit as st
import pandas as pd
from io import StringIO
from .cmd import CmdLocal, CmdSSH
from .maker import PageStore


class FilesList():
    """
    List files in a folder
    """

    def __init__(self, ssh, filematch, folders, button="", depth=1, show_search=False):
        self.ssh = ssh
        self.filematch = filematch
        self.folders = folders
        self.button = button
        self.depth = depth
        self.init = False
        self.folders_files = {}
        self.show_search = show_search
        

    def play(self):
        
        if self.button:
            if st.button(self.button, key=self.button):
                self.play_inner()
        elif not self.init:                                
            self.play_inner()
                                    
    def play_inner(self): 
        self.init = True
        for fldr in self.folders:
            cmd_txt = f"find {fldr} -maxdepth {self.depth} -type f -name '{self.filematch}'"
            if self.show_search:
                st.write(cmd_txt)
            if self.ssh is None:
                cmd_file = CmdLocal(cmd=cmd_txt, button="Retrieving files")
                cmd_file.play()            
            else:
                cmd_file = CmdSSH(ssh=self.ssh, cmd=cmd_txt, output="list")
                cmd_file.play()            
            self.folders_files[fldr] = cmd_file.result
                                                                            
#####################################################################################
class BrowseView():
    """
    Login for ssh based login
    """

    def __init__(self, ssh, filematch, folder_key, displays=["text"], edittable=False):        
        self.ssh = ssh
        self.filematch = filematch
        self.folder_key = folder_key
        self.folder = "" 
        self.txt_dir = f"find {self.folder} -type f -maxdepth 1 -name '{self.filematch}'"
        self.cmd_dir = None
        self.cmd_file = None
        self.edittable = edittable
        self.txt_contents = ""        
        self.displays = displays # this can be a list of displays which are shown on tabs text, code, info, df, plot (plot not implemented yet!)
        self.files_list = []
                                            
    def play(self):        
        self.folder = PageStore().get_global(self.folder_key)
        self.txt_dir = f"find {self.folder} -type f -maxdepth 1 -name '{self.filematch}'"        
        if self.edittable:
            self.txt_dir = st.text_input("Search",self.txt_dir)
        cols = st.columns([2,5])                    
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
                    
                
                


                
                
       

            

            
                
        
        

    