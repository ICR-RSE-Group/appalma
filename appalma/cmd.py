import streamlit as st
import pandas as pd
from io import StringIO
from contextlib import contextmanager, redirect_stdout
import os
import time
import subprocess
from pyalma import SshClient


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

    def __init__(self, server,sftp,username,password,port,cmd="ls -a"):
        self.cmd = cmd
        self.server = server
        self.username = username
        self.password = password
        self.sftp = sftp
        self.ssh = None
        self.port = port
                                
    def play(self):
        cols = st.columns([2,2,7])
        with cols[2]:
            with st.expander("Command output", expanded=False):                        
                output = st.empty()
        with cols[0]:
            if st.button("Press me"):            
                with st.spinner("", show_time=True):                    
                    with st_capture(output.code):                                          
                        try:
                            self.ssh = SshClient(server=self.server, username=self.username, password=self.password, port=self.port)                  
                        except Exception as e:
                            with cols[1]:
                                st.error("Error")
                                print("Error connecting to server", e)
                                return
                        print("Starting command", self.cmd)                        
                        start = time.time()
                        results_str, error_str = self.cmd_ssh(self.cmd)
                        end = time.time()            
                        print(f"Elapsed time {round(end - start, 3)} seconds")      
                        OK = error_str == None
                        print(results_str)
                        print(error_str)
                        with cols[1]:
                            if OK:                                                                                                
                                st.success("OK")
                            else:                                
                                st.error("FAILED")                          

    
    def cmd_ssh(self,params):
        print("---  ")
        results = self.ssh.run_cmd(self.cmd)
        results_str, error_str = results["output"], results["err"]                                                 
        return results_str, error_str
        
############################################################################        
class CmdLocal():
    """
    Login for local system.os
    """

    def __init__(self, cmd=["ls", "-a"]):
        self.cmd = cmd
                                
    def play(self):
        cols = st.columns([2,2,7])
        with cols[2]:
            with st.expander("Command output", expanded=False):                        
                output = st.empty()
        with cols[0]:        
            if st.button("Press me"):
                with st.spinner("", show_time=True):                    
                    with st_capture(output.code):                                    
                        print("Starting command", self.cmd)                        
                        start = time.time()
                        ret = self.cmd_runner_with_wait(self.cmd)
                        end = time.time()            
                        print(f"Elapsed time {round(end - start, 3)} seconds")                          
                        with cols[1]:
                            if ret == "done":
                                st.success("OK")
                            else:
                                st.error("FAILED")

    
    def cmd_runner_with_wait(self,params):
        print("---  ")
        result = subprocess.Popen(params,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
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
            output  = result.stdout.readline()
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
    
    
