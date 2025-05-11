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
        "inputs":[("working",scratch),("home",home)],
        "outputs":[("results",scratch),("home",home)]
        },
        """
                                                    
    def play(self):
        for group_name, tuples in self.settings_dic.items():
            st.write(group_name)
            for tpl in tuples:
                st.write(tpl)
            
            
                                
            def change_sel_group():
                pass
                #self.my_group = st.session_state.group                
                # retrieve user lists on this basis
                

            
            #self.my_group = st.radio("Select a group:", self.cmd_group.result, index=0, key="group",on_change=change_sel_group)
                                                                    
            #PageStore().set_global("my_group", self.my_group)
            



                
                
            

        

    