import streamlit as st
from streamlit_option_menu import option_menu
from view.abstract_streamlit_view import AbstractStreamlitView
from typing import Literal

class SidebarView(AbstractStreamlitView):
    
    def render(self) -> Literal["Home", "Settings"]:
        with st.sidebar:
            option = option_menu("Main Menu", [
                    "Home", 
                    'Settings'
                ], 
                icons=[
                    'house',
                    'gear'],
                menu_icon="cast",
                default_index=0
            )
            
            st.divider()
                
            st.write("This is the sidebar view.")
            
            return option