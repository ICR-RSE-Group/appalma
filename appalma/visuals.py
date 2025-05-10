import streamlit as st

class PageConfig():
    """
    Header and title/icon for the app
    """

    def __init__(self, page_icon="💥", page_title="demo-appalma",
                 header_title="DEMO-APP-ALMA", header_colour="Crimson", 
                 header_html="", sticky=True):
        self.page_icon = page_icon
        self.page_title = page_title
        self.header_title = header_title
        self.header_colour = header_colour
        self.header_html = header_html
        self.sticky = sticky
                        
    def play(self):

        st.set_page_config(
            page_icon=self.page_icon,
            page_title=self.page_title,
            layout="wide",
            initial_sidebar_state="auto",
        )
                
        header = st.container()
        if self.header_html == "":            
            headertxt = '<span style="color:black;">'
            headertxt += '<img src="https://www.icr.ac.uk/images/default-source/in-page-imagery/icr_logo.svg?sfvrsn=1d8bc892_1" alt="icr" width="200px">'                        
            headertxt += f'</span><span style="color:{self.header_colour};font-size:40px;"> - {self.header_title} - </span>'
                    
        else  :
            headertxt = self.header_html
        
        header.write(headertxt, unsafe_allow_html=True)     
        if self.sticky:               
            header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

            st.markdown(
                """
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    background-color: white;
                    z-index: 999;
                }
                .fixed-header {
                    border-bottom: 1px solid black;
                }
            </style>
                """,
                unsafe_allow_html=True    
            )
