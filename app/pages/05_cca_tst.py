import streamlit as st
from appalma.maker import PageStore
from appalma.visuals import PageConfig
from appalma.browse import FilesList
from appalma.cmd import CmdSSH

PageStore().add_to_page("cfg", PageConfig(
                                page_icon="🍏", 
                                page_title="cca-app",
                                header_title="CCA-CRISPR-APP", 
                                header_colour="MediumSeaGreen",
                                sticky=True))

ssh = PageStore().ssh_success()
if not ssh:
    st.error("SSH Connection has not been made, please log on via home page")
else:    
    folders_tst = ["/data/scratch/DCO/DIGOPS/SCIENCOM/ralcraft/Syed/CCA/TP53null_C2_P84/TP53null_C2_P84",
                   "/data/scratch/DCO/DIGOPS/SCIENCOM/ralcraft/Syed/CCA/TP53nullBRCA1null_P84/TP53nullBRCA1null_P84"]
    folders_ctrl = ["/data/scratch/DCO/DIGOPS/SCIENCOM/ralcraft/Syed/CCA/TP53nullBRCA1null_P84/TP53nullBRCA1null_P84", 
                    "/data/scratch/DCO/DIGOPS/SCIENCOM/ralcraft/Syed/CCA/TP53null_C2_P84/TP53null_C2_P84"]
    #TEST="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53null_C2_P84"
    #CTRL="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53nullBRCA1null_P84"
    
    PageStore().add_to_page("ctrl-test", FilesList(ssh, filematch='*.out', folders=list(set(folders_tst + folders_ctrl)), button=""))
            
    cols = st.columns(2)

    with cols[0]:                
        def select_folder1():
            sel_short_fl1 = st.session_state.folder_select1     
            sel_fl1 = selected_tstfldr + sel_short_fl1 
        selected_tstfldr = st.selectbox("Select a test folder", folders_tst, on_change=select_folder1, key="folder_select1")                                              
        try:
            fls_tst = PageStore().pages["ctrl-test"].folders_files[selected_tstfldr]
            fls_tst = [x.replace(selected_tstfldr, "") for x in fls_tst]
            sel_short_fl1 = st.selectbox("Choose test", fls_tst, index=0)        
        except:
            st.write("No files found")
    with cols[1]:
        def select_folder2():
            sel_short_fl2 = st.session_state.folder_select2     
            sel_fl2 = selected_ctrlfldr + sel_short_fl2       
        selected_ctrlfldr = st.selectbox("Select a ctrl folder", folders_ctrl, on_change=select_folder2, key="folder_select2")                 
        try:
            fls_ctrl = PageStore().pages["ctrl-test"].folders_files[selected_ctrlfldr]
            fls_ctrl = [x.replace(selected_ctrlfldr, "") for x in fls_ctrl]
            sel_short_fl2 = st.selectbox("Choose ctrl", fls_ctrl, index=0)        
        except:
            st.write("No files found")

    
    if selected_ctrlfldr and selected_tstfldr:
        st.write("---  ")
        cols = st.columns(2)
        with cols[0]:                
            input1 = st.text_input("Input 1", value="CCA", key="input1")
            check1 = st.checkbox("Check 1", value=True, key="check1")
            options = st.multiselect("Options", ["Option 1", "Option 2", "Option 3"], default=["Option 1", "Option 2"], key="options")
            radio1 = st.radio("Radio 1", ["Option 1", "Option 2", "Option 3"], index=0, key="radio1")
            select1 = st.selectbox("Select 1", ["Option 1", "Option 2", "Option 3"], index=0, key="select1")
        with cols[1]:                
            input2 = st.text_input("Input 2", value="CCA", key="input2")
            check2 = st.checkbox("Check 2", value=True, key="check2")
            options2 = st.multiselect("Options", ["Option 1", "Option 2", "Option 3"], default=["Option 1", "Option 2"], key="options2")
            radio2 = st.radio("Radio 2", ["Option 1", "Option 2", "Option 3"], index=0, key="radio2") 
            select2 = st.selectbox("Select 2", ["Option 1", "Option 2", "Option 3"], index=0, key="select2")
        st.write("---  ")
        if st.button("Run"):
            st.write(f"Input 1: {input1}")
            st.write(f"Check 1: {check1}")
            st.write(f"Options: {options}")
            st.write(f"Radio 1: {radio1}")
            st.write(f"Select 1: {select1}")
            st.write(f"Input 2: {input2}")
            st.write(f"Check 2: {check2}")
            st.write(f"Options 2: {options2}")
            st.write(f"Radio 2: {radio2}")
            st.write(f"Select 2: {select2}")
    
    
    
    
    



