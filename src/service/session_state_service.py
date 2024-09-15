import streamlit as st


class SessionStateService:
    def __init__(self):
        if 'background_color' not in st.session_state:
            st.session_state.background_color = "#0E1117"
        if 'secondary_background_color' not in st.session_state:
            st.session_state.secondary_background_color = "#262730"
        if 'text_color' not in st.session_state:
            st.session_state.text_color = "#FAFAFA"
        if 'primary_color' not in st.session_state:
            st.session_state.primary_color = "#FF4B4B"

    def reset_colors(self) -> None:
        st.session_state.background_color = "#0E1117"
        st.session_state.secondary_background_color = "#262730"
        st.session_state.text_color = "#FAFAFA"
        
    def save_colors(self, background_color: str, secondary_background_color: str, text_color: str) -> None:
        st.session_state.background_color = background_color
        st.session_state.secondary_background_color = secondary_background_color
        st.session_state.text_color = text_color
        
    def set_background_color(self, color: str) -> None:
        st.session_state.background_color = color
        
    def set_secondary_background_color(self, color: str) -> None:
        st.session_state.secondary_background_color = color
        
    def set_text_color(self, color: str) -> None:
        st.session_state.text_color = color
        
    def get_background_color(self) -> str:
        return st.session_state.background_color
    
    def get_secondary_background_color(self) -> str:
        return st.session_state.secondary_background_color
    
    def get_text_color(self) -> str:
        return st.session_state.text_color
        