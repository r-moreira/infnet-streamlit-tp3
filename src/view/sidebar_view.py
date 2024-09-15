import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from typing import Literal

class SidebarView(AbstractStreamlitView):
    
    def __init__(self, session_state_service: SessionStateService) -> None:
        self.options = ["Home", "Settings"]
        self.session_state_service = session_state_service
    
    def render(self) -> Literal["Home", "Table 2675 Analysis", "Settings"]:        
        with st.sidebar:
            add_vertical_space(4) 
            
            option = option_menu("Main Menu", [
                    "Home", 
                    "Table 2675 Analysis",
                    "Settings",
                ], 
                icons=[
                    'house',
                    'table',
                    'gear'
                ],
                menu_icon="cast",
                default_index=self.options.index(self.session_state_service.get_menu_option()),
                styles={ 
                    "container": {"background-color": self.session_state_service.get_background_color()},
                    "nav-link-selected": {"background-color": self.session_state_service.get_primary_color()},
                }
            )
            
            st.divider()
                
            st.write("This is the sidebar view.")
            
            return option