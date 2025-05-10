import streamlit as st

st.set_page_config(
    page_icon="🍃",
    page_title="demo-appalma",
    layout="wide",
    initial_sidebar_state="auto",
)

header = """
        <span style="color:black;">
        <img src="https://www.icr.ac.uk/images/default-source/in-page-imagery/icr_logo.svg?sfvrsn=1d8bc892_1"
        alt="icr" width="200px"></span><span style=        
        "color:firebrick;font-size:40px;"> - DEMO-APP-ALMA - </span><span style=        
        """
st.markdown(header, unsafe_allow_html=True)

st.write("---  ")

