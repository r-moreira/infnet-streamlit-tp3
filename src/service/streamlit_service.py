import streamlit as st
from service.datario_parser_service import DataRioParserService
from view.sidebar_view import SidebarView

class StreamlitService:
    def __init__(self, 
        configuration: dict,
        data_rio_parser_service: DataRioParserService,
        sidebar_view: SidebarView) -> None:
        
        self.configuration = configuration
        self.sidebar_view = sidebar_view
        self.data_rio_parser_service = data_rio_parser_service
        
    def run(self) -> None:
        st.title(self.configuration["app"]["message"]["hello"])
        
        self.sidebar_view.render()