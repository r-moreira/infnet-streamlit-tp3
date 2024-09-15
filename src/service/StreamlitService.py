import streamlit as st

class StreamlitService:
    def __init__(self, configuration: dict) -> None:
        self.configuration = configuration
        
    def run(self) -> None:
        st.title(self.configuration["app"]["message"]["hello"])