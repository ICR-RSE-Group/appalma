import streamlit as st


class Login():
    """
    Login for ssh based login
    """

    def __init__(self, server="alma.icr.ac.uk", username=None, password=None, sftp="alma-app.icr.ac.uk", port=22):
        cols = st.columns([5,2])
        with cols[0]:
            tabUser, tabServer = st.tabs(["User", "(Server)"])
            with tabUser:
                cols1 = st.columns([2,2])    
                with cols1[0]:        
                    username = st.text_input("Username:", username, key="username")
                with cols1[1]:
                    password = st.text_input("Password:", "", type="password", key="password")
            with tabServer:
                cols2 = st.columns([2,2])    
                with cols2[0]:
                    server = st.text_input("Remote server:", "alma.icr.ac.uk")
                with cols2[1]:
                    sftp = st.text_input("SFTP server:", "alma-app.icr.ac.uk")

    def tst():
        pass