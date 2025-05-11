import streamlit as st
from .maker import PageStore



class Settings():
    """
    Global settings store for state
    """

    def __init__(self, settings_dic):
        self.settings_dic = settings_dic
        """
        {
        "inputs":{"working":scratch,"home":home},
        "outputs":{"results":scratch,"home":home}
        },
        """
                                                    
    def play(self):
        for group_name, file_names in self.settings_dic.items():
            st.write(f"Settings group: **{group_name}**")
            for nm, fl in file_names.items():                
                setting_val = st.text_input(nm, fl, key=group_name+"_" + nm)
                PageStore().set_global(group_name+"_" + nm, setting_val)
                st.write(group_name+"_" + nm, setting_val)
                self.settings_dic[group_name][nm] = setting_val
            st.write("---  ")
                
                                                                
            def change_sel_group():
                pass
                #self.my_group = st.session_state.group                
                # retrieve user lists on this basis
                

            
            #self.my_group = st.radio("Select a group:", self.cmd_group.result, index=0, key="group",on_change=change_sel_group)
                                                                    
            #PageStore().set_global("my_group", self.my_group)
            



                
                
            

        

    