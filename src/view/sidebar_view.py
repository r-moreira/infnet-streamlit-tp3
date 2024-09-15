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
        return self.render_main_menu()
   
    def render_main_menu(self) -> Literal["Home", "Table 2675 Analysis", "Settings"]:
        with st.sidebar:
            add_vertical_space(4) 
            
            page_option = option_menu("Main Menu", [
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
            
            return page_option
        
    def render_sub_menu(self) -> Literal["Countries", "Continents"] | None:
        if self.session_state_service.is_table_2675_dataframes_set():
            
            with st.sidebar:
                dataset_option = option_menu("Dataset Selection", [
                        "Countries", 
                        "Continents",
                    ], 
                    icons=[
                        'flag',
                        'globe'
                    ],
                    menu_icon="database",
                    default_index=0,
                    styles={ 
                        "container": {"background-color": self.session_state_service.get_background_color()},
                        "nav-link-selected": {"background-color": self.session_state_service.get_primary_color()},
                    }
                )
            
            return dataset_option