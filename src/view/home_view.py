import streamlit as st
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService

class HomeView(AbstractStreamlitView):
    def __init__(self, session_state_service: SessionStateService) -> None:
        self.session_state_service = session_state_service
        
    
    def render(self) -> None:
        st.title("Data Rio Turism Analysis")
        
        st.write("Welcome to the Data Rio Turism Analysis. Here you can analyze the data of the turism in Rio de Janeiro.")
        
        