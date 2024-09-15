import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService

class SettingsView(AbstractStreamlitView):  
    def __init__(self, session_state_service: SessionStateService) -> None:
        self.session_state_service = session_state_service
    
    def render(self) -> None:
        st.title("Settings")
        st.divider()
        st.header("Theme")
        
        picker, picker2, picker3, picker4 = st.columns(4)
        button, button2 = st.columns(2)
        
        with picker:
            background_color = st.color_picker(
                "1st Background Color",
                self.session_state_service.get_background_color()
            )
        
        with picker2:
            secondary_background_color = st.color_picker(
                "2nd Background Color", 
                self.session_state_service.get_secondary_background_color()
            )
            
        with picker3:
            text_color = st.color_picker(
                "Text Color",
                self.session_state_service.get_text_color()
            )
            
        with picker4:
            primary_color = st.color_picker(
                "Primary Color",
                self.session_state_service.get_primary_color()
            )

        with button:
            add_vertical_space(2)
            save_button = st.button(label='Save Colors', use_container_width=True, key='save_colors')
            
            if save_button:
                self.session_state_service.save_colors(
                    background_color, 
                    secondary_background_color, 
                    text_color,
                    primary_color
                )          
                self.session_state_service.set_menu_option("Settings")
            
                st.rerun()
                    
        with button2:
            add_vertical_space(2)
            reset_button = st.button(label='Reset Colors', use_container_width=True)
            if reset_button:
                self.session_state_service.reset_colors()
                self.session_state_service.set_menu_option("Settings")
                st.rerun()