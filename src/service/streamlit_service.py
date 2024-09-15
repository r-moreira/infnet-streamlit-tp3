import streamlit as st
from service.session_state_service import SessionStateService
from view.sidebar_view import SidebarView
from view.settings_view import SettingsView
from view.home_view import HomeView
from view.table_analysis_view import TableAnalysisView

class StreamlitService:
    def __init__(
        self,
        session_state_service: SessionStateService,
        sidebar_view: SidebarView,
        settings_view: SettingsView,
        home_view: HomeView,
        table_analysis_view: TableAnalysisView) -> None:
        
        self.sidebar_view = sidebar_view
        self.session_state_service = session_state_service
        self.settings_view = settings_view
        self.home_view = home_view
        self.table_analysis_view = table_analysis_view
        
    def run(self) -> None:
        st.set_page_config(
            page_title="DataRio Turism",
            page_icon="🌐"
        )
        
        self._set_page_theme()
        
        option = self.sidebar_view.render()
        
        if option == "Home":                 
            self.home_view.render()
        elif option == "Table 2675 Analysis":
            self.table_analysis_view.render()
        elif option == "Settings":
            self.settings_view.render()
            
    def _set_page_theme(self) -> None:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {self.session_state_service.get_background_color()};
                color: {self.session_state_service.get_text_color()};
            }}
            .stSidebar {{
                background-color: {self.session_state_service.get_secondary_background_color()};
            }}
            header {{
                background-color: {self.session_state_service.get_background_color()};
                color: {self.session_state_service.get_text_color()};
            }}
            button[data-testid="stBaseButton-secondary"] {{
                background-color: {self.session_state_service.get_secondary_background_color()};
                color: {self.session_state_service.get_text_color()};
            }}
            button[data-testid="stBaseButton-secondary"]:hover {{
                border-color: {self.session_state_service.get_primary_color()};
                color: {self.session_state_service.get_primary_color()};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )