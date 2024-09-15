import streamlit as st
from view.sidebar_view import SidebarView

class StreamlitService:
    def __init__(
        self, 
        configuration: dict,
        sidebar_view: SidebarView) -> None:
        
        self.configuration = configuration
        self.sidebar_view = sidebar_view
        
    def run(self) -> None:
        st.title(self.configuration["app"]["message"]["hello"])
        
        self.sidebar_view.render()