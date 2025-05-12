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
    folders_tst = ["/data/rds/DIT/SCICOM/SCRSE/shared/data/RSE"]
    folders_ctrl = ["/data/rds/DIT/SCICOM/SCRSE/shared/data/cosmx-samples/Sample_Pancreas_2025"]
    #TEST="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53null_C2_P84"
    #CTRL="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53nullBRCA1null_P84"

    cols = st.columns(2)

    with cols[0]:
        selected_tstfldr = folders_tst[0]                    
        def select_folder1():
            selected_tstfldr = st.session_state.folder_select1            
        selected_tstfldr = st.selectbox("Select a test folder", folders_tst, on_change=select_folder1, key="folder_select1")
        txt_dir1 = f"find {selected_tstfldr} -type f -maxdepth 1 -name '*.csv'"
        cmd1 = FilesList(ssh, filematch='*.csv', folder=selected_tstfldr, button="Get tests")
        PageStore().add_to_page("sc1", cmd1)        
        fls_tst = cmd1.files_list
        sel_fl1 = st.radio("Choose test", fls_tst, index=0)
        
    with cols[1]:
        selected_ctrlfldr = folders_ctrl[0]                    
        def select_folder2():
            selected_ctrlfldr = st.session_state.folder_select2            
        selected_ctrlfldr = st.selectbox("Select a ctrl folder", folders_ctrl, on_change=select_folder2, key="folder_select2")
        txt_dir2 = f"find {selected_ctrlfldr} -type f -maxdepth 1 -name '*.csv'"
        cmd2 = CmdSSH(ssh, cmd=txt_dir2, output="code", spinner="", button="Get ctrls")
        PageStore().add_to_page("sc2", cmd2)
        st.write(cmd2.result)
        #fls_ctrl = [f.split("/")[-1] for f in cmd2.result]
        #sel_fl2 = st.radio("Choose control", cmd2.result, index=0)
    
    
    
    
    



