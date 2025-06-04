import streamlit as st
from appalma.maker import PageStore
from appalma.visuals import PageConfig
from appalma.browse import FilesList
from appalma.cmd import CmdLocal
import pandas as pd
import os

PageStore().add_to_page("cfg", PageConfig(
                                page_icon="🍏", 
                                page_title="cca-app",
                                header_title="CCA-CRISPR-APP", 
                                header_colour="MediumSeaGreen",
                                sticky=True))

fldr_root = "data/CCA/RPE1_screens"


if True:
    
    fldrs_all = [fldr_root]
    files_things_dic = {}
        
    #TEST="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53null_C2_P84"
    #CTRL="/data/rds/DBC/UBCN/GENFUNC/SHARED/Lord_lab_analysis/CRISPR_singleguide/CRISPRn_RPE1_multigene_SNZ/data/negative_selection/TP53nullBRCA1null_P84"
    
    PageStore().add_to_page("ctrl-test", FilesList(None, filematch='*count.txt', depth=2, folders=fldrs_all, button="", show_search=False))
        
    full_screens_available = PageStore().pages["ctrl-test"].folders_files[fldr_root]
    screens_available = []
    for f in full_screens_available:        
        files_things_dic[f] = fldr_root + "/" + f
        splitted = f.split("/")
        x_screen = splitted[-1].replace(".count.txt", "")
        x_lib = "Yusa"
        x_cond = "BRCA1"
        x_clone = "C2"
        x_proj = x_screen.split("_")[-1]
        x_cl = "RPE1"
        x_clcond = "BRCA1"
        x_time = "T2A"
        files_things_dic[x_screen] = {
            "full_path": f,
            "x_screen": x_screen,
            "x_lib": x_lib,
            "x_cond": x_cond,
            "x_clone": x_clone,
            "x_proj": x_proj,
            "x_cl": x_cl,
            "x_clcond": x_clcond,
            "x_time": x_time
        }
        screens_available.append(x_screen)
    
    #screens_available = [x for x in screens_available if "._" not in x]
    #screens_available = [x.replace(fldr_root, "") for x in screens_available]

    with st.expander("Select screens", expanded=True):
            
        #tabTest, tabCtrl = st.tabs(["Test", "Control"])
        tabCtrl,tabTest = st.columns(2)

        with tabCtrl:                        
            try:                                
                sel_short_fl2 = st.selectbox("**Choose ctrl**", screens_available, index=0)        
                if sel_short_fl2:    
                    dic_screen_keys_ctrl = files_things_dic[sel_short_fl2]                                                                                                    
                    cols = st.columns(2)                    
                    with cols[0]:                    
                        ctrl_screen = st.text_input("ctrl.screen", value=dic_screen_keys_ctrl["x_screen"], key="ctrl_screen")
                        ctrl_lib = st.text_input("library.ctrl", value=dic_screen_keys_ctrl["x_lib"], key="ctrl_lib")
                        ctrl_cond = st.text_input("screen.condition.ctrl", value=dic_screen_keys_ctrl["x_cond"], key="ctrl_cond")
                        ctrl_clone = st.text_input("clone.ctrl", value=dic_screen_keys_ctrl["x_clone"], key="ctrl_clone")
                    with cols[1]:                    
                        ctrl_proj = st.text_input("projectID.ctrl", value=dic_screen_keys_ctrl["x_proj"], key="ctrl_proj")                
                        ctrl_cl = st.text_input("cl.ctrl", value=dic_screen_keys_ctrl["x_cl"], key="ctrl_cl")                
                        ctrl_clcond = st.text_input("cl.condition.ctrl", value=dic_screen_keys_ctrl["x_clcond"], key="ctrl_clcond")                
                        ctrl_time = st.text_input("timepoint.replicate.ctrl", value=dic_screen_keys_ctrl["x_time"], key="ctrl_time")                  
            except:
                st.write("No files found")
        with tabTest:            
            try:                                
                sel_short_fl1 = st.selectbox("**Choose test**", screens_available, index=0)                
                if sel_short_fl1:
                    dic_screen_keys = files_things_dic[sel_short_fl1]                                                                                
                    cols = st.columns(2)
                    with cols[0]:                    
                        tst_screen = st.text_input("test.screen", value=dic_screen_keys["x_screen"], key="tst_screen")
                        tst_lib = st.text_input("library.test", value=dic_screen_keys["x_lib"], key="tst_lib")
                        tst_cond = st.text_input("screen.condition.test", value=dic_screen_keys["x_cond"], key="tst_cond")
                        tst_clone = st.text_input("clone.test", value=dic_screen_keys["x_clone"], key="tst_clone")
                    with cols[1]:                    
                        tst_proj = st.text_input("projectID.test", value=dic_screen_keys["x_proj"], key="tst_proj")                
                        tst_cl = st.text_input("cl.test", value=dic_screen_keys["x_cl"], key="tst_cl")                
                        tst_clcond = st.text_input("cl.condition.test", value=dic_screen_keys["x_clcond"], key="tst_clcond")                
                        tst_time = st.text_input("timepoint.replicate.test", value=dic_screen_keys["x_time"], key="tst_time")                  
            except:
                st.write("No files found")


    
    if True:
    #with st.expander("Run CCA", expanded=True):
        if sel_short_fl1 and sel_short_fl2:   
            out_rds = fldr_root + "/CCA/" + ctrl_screen + "__" + tst_screen + ".csv"
            out_local = f"data/out/{ctrl_screen}__{tst_screen}.tsv"
            st.write("File:",ctrl_screen + "__" + tst_screen + ".csv")
            # check if the file exists            
            try:
                ssh.isfile(out_rds)
                if not os.path.exists(out_local):
                    with st.spinner("Downloading pre-calculated file from server...", show_time=True):
                        df = ssh.read_file(out_rds)                    
                        df.to_csv(out_local, sep="\t", index=False)
                        st.dataframe(df, use_container_width=True)                    
                else:
                    df = pd.read_csv(out_local, sep="\t")                
                    st.dataframe(df, use_container_width=True)
            except Exception as e:                
                #st.write("File does not exist", sel_short_fl1)
                if os.path.exists(out_local):
                    #st.write("Deleting local file", out_local)                    
                    os.remove(out_local)
                                            
                # we first need to downlload the files from the server
                temp_name_test = "data/test_tmp.count.txt"
                temp_name_ctrl = "data/ctrl_tmp.count.txt"
                                                
                if not os.path.exists(temp_name_test) or not os.path.exists(temp_name_ctrl):
                    with st.spinner("Downloading input files from server...", show_time=True):
                        path_fl1 = files_things_dic[sel_short_fl1]["full_path"]
                        path_fl2 = files_things_dic[sel_short_fl2]["full_path"]
                        ssh.download_remote_file(path_fl1, temp_name_test)
                        ssh.download_remote_file(path_fl2, temp_name_ctrl)

                aditi_cmds = []
                aditi_cmds.append("Rscript")
                aditi_cmds.append("thirdparty/bcrds/prepare_cca_input.R")
                aditi_cmds.append(ctrl_screen)
                aditi_cmds.append(tst_screen)
                aditi_cmds.append(ctrl_proj)
                aditi_cmds.append(ctrl_lib)
                aditi_cmds.append(ctrl_cl)
                aditi_cmds.append(ctrl_cond)
                aditi_cmds.append(ctrl_clcond)
                aditi_cmds.append(ctrl_clone)
                aditi_cmds.append(ctrl_time)
                aditi_cmds.append(tst_proj)
                aditi_cmds.append(tst_lib)
                aditi_cmds.append(tst_cl)                        
                aditi_cmds.append(tst_cond)
                aditi_cmds.append(tst_clcond)
                aditi_cmds.append(tst_clone)                        
                aditi_cmds.append(tst_time)                                                                                    
                                
                cca_cmds = []
            
                in_txt = f"data/CCA/{ctrl_screen}__{tst_screen}/{ctrl_screen}__{tst_screen}_test.txt"
                in_repmap = f"data/CCA/{ctrl_screen}__{tst_screen}/{ctrl_screen}__{tst_screen}_test.repmap"
                cca_cmds.append("thirdparty/cca/bin/crisprCountsAnalysis")
                cca_cmds.append(f"COUNTS={in_txt}")
                cca_cmds.append(f"REPMAP={in_repmap}")
                cca_cmds.append(f"OUT={out_local}")
                cca_cmds.append("AT_HOME=false")
                cmd_key = "_".join(cca_cmds).replace("=", "_").replace(" ", "_").replace("/", "_").replace("-", "_")
                                
                my_env = os.environ.copy()
                my_env["PATH"] = f"thirdparty/cca/bin:{my_env['PATH']}"            
                cmd_aditi = CmdLocal(cmd=aditi_cmds, cmd2=cca_cmds,env=my_env)
                with st.spinner("Run cmd line..."):
                    cmd_aditi.play()                                
                try:                    
                    df = pd.read_csv(out_local, sep="\t")                    
                    st.dataframe(df, use_container_width=True)
                    
                    with st.spinner("Writing to remote..."):
                        ssh.write_to_remote_file(df, out_rds, file_format="csv")
                except Exception as e:
                    pass
                
            
    
    
    
    
    



