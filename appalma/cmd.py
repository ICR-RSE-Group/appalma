import streamlit as st
import pandas as pd
from io import StringIO
from contextlib import contextmanager, redirect_stdout
import os
import time
import subprocess


# Helper function that streams stdout to a streamlit component
@contextmanager
def st_capture(output_func):    
    try:
        with StringIO() as stdout, redirect_stdout(stdout):
            old_write = stdout.write

            def new_write(string):
                ret = old_write(string)
                output_func(stdout.getvalue())
                return ret
            
            stdout.write = new_write
            yield
    except Exception as e:
        st.error(str(e))
                
class CmdSSH():
    """
    Login for local system.os
    """

    def __init__(self,ssh,button="",spinner="",cmd_edit=False,output="print",cmd="ls -a"):        
        self.ssh = ssh
        self.button=button
        self.spinner=spinner
        self.cmd_edit = cmd_edit
        self.cmd = cmd
        self.output = output
        self.selected_line = ""        
        self.error = ""
        self.result = ""
        self.ok = False
        
                                
    def play(self):        
        if self.cmd_edit:
            self.cmd = st.text_area("Command:", self.cmd, height=100, key="cmd")
                
        if self.button == "":            
            self.play_inner()
        else:            
            if st.button(self.button):
                self.play_inner()
    
    def play_inner(self):        
        """
        ouput = ["print", "df", "text", "code", "radio", "list"]
        """        
        with st.spinner(self.spinner, show_time=True):                                
            output = st.empty()
            with st_capture(output.code):
                print("Starting command", self.cmd)                        
                start = time.time()
                results = self.ssh.run_cmd(self.cmd)
                results_str, error_str = results["output"], results["err"]                                               
                end = time.time()            
                print(f"Elapsed time {round(end - start, 3)} seconds")      
                OK = error_str == None                
                self.result = results_str
                self.error = error_str
                self.ok = OK
                if not OK:                                                                                                                
                    st.error(f"FAILED: {error_str}")
                else:                
                    if self.output == "print":
                        print(results_str)                
                    elif self.output == "df":
                        try:
                            df = pd.read_csv(StringIO(results_str))
                            st.dataframe(df)
                        except Exception as e:
                            st.error(f"Error parsing output: {e}")
                    elif self.output == "text":
                        st.text(results_str)
                    elif self.output == "code":
                        st.code(results_str)
                    elif self.output == "radio":
                        lines = results_str.split("\n")
                        if len(lines) > 0:
                            self.selected_line = st.radio("Select a line:", lines)
                            st.text(self.selected_line)
                    elif self.output == "list":
                        lines = results_str.split("\n")
                        if len(lines) > 0:
                            self.result = lines
            with output:
                st.write("")
                
                                    
############################################################################        
class CmdLocal():
    """
    Login for local system.os
    """

    def __init__(self, cmd=["ls", "-a"], cmd2=[], button="Execute", env=[]):
        self.cmd = cmd
        self.button = button
        self.cmd2 = cmd2
        self.env = env        
        self.key="_".join(self.cmd).replace("/","_").replace(" ","_").replace("-","_")        
                                        
    def play(self):                        
        if st.button(self.button, key=self.key):
            with st.expander("Command output", expanded=False):                        
                output = st.empty()        
            ret = ""
            with st.spinner("", show_time=True):                    
                with st_capture(output.code):                                    
                    print("Starting command", self.cmd)                        
                    start = time.time()
                    ret = self.cmd_runner_with_wait(self.cmd)
                    end = time.time()            
                    print(f"Elapsed time {round(end - start, 3)} seconds")                                              
                    if len(self.cmd2) > 0:
                        print("Starting command", self.cmd2)                        
                        start2 = time.time()
                        ret = self.cmd_runner_with_wait(self.cmd2)
                        end2 = time.time()            
                        print(f"Elapsed time 2 {round(end2 - start2, 3)} seconds")
                        print(f"Total time {round(end2 - start, 3)} seconds")
            if ret == "done":
                st.success("OK")
            else:
                st.error("FAILED")

    
    def cmd_runner_with_wait(self,params):
        print("---  ")
        if self.env == []:
            result = subprocess.Popen(params,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        else:
            result = subprocess.Popen(params,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,env=self.env)
        error_msg = False
        any_exceptions = False        
        # Wait until process terminates
        while result.poll() is None:            
            output = result.stdout.readline()
            if output:
                while output:
                    if "SEVERE" in output.strip().decode('utf-8'):
                        any_exceptions = True
                    if "ERROR" in output.strip().decode('utf-8'):
                        any_exceptions = True
                    print(output.strip().decode('utf-8'))
                    output  = result.stdout.readline()
            error = result.stderr.readline()
            while error:
                if not error_msg:
                    print("---------  ")
                    print("Additional messages found:")
                    error_msg = True
                print("#",error.strip().decode('utf-8'))
                if "SEVERE" in error.strip().decode('utf-8'):
                    any_exceptions = True
                if "ERROR" in error.strip().decode('utf-8'):
                    any_exceptions = True
                error  = result.stderr.readline()
            time.sleep(0.001)
            results_str  = result.stdout.readline()
            if output:
                print(output.strip().decode('utf-8'))
            result.poll()
            print("---------  ")                        
            if any_exceptions:
                print("!!! failed")
                return "failed"
            else:                
                return "done"    
    ############################################################################
    
    
