import pandas as pd
import streamlit as st
from typing import Literal

class SessionStateService:
    def __init__(self):
        if 'table_2675_continents_df' not in st.session_state:
            st.session_state.table_2675_continents_df = None
        if 'table_2675_countries_df' not in st.session_state:
            st.session_state.table_2675_countries_df = None
        if 'menu_option' not in st.session_state:
            st.session_state.menu_option = "Home"
        if 'background_color' not in st.session_state:
            st.session_state.background_color = "#0E1117"
        if 'secondary_background_color' not in st.session_state:
            st.session_state.secondary_background_color = "#262730"
        if 'text_color' not in st.session_state:
            st.session_state.text_color = "#FAFAFA"
        if 'primary_color' not in st.session_state:
            st.session_state.primary_color = "#FF4B4B"

    def is_table_2675_dataframes_set(self) -> bool:
        return self.get_table_2675_continents_df() is not None and self.get_table_2675_countries_df() is not None

    def set_table_2675_continents_df(self, df: pd.DataFrame) -> None:
        st.session_state.table_2675_continents_df = df
        
    def get_table_2675_continents_df(self) -> pd.DataFrame:
        return st.session_state.table_2675_continents_df
    
    def clear_table_2675_dataframes(self) -> None:
        st.session_state.table_2675_continents_df = None
        st.session_state.table_2675_countries_df = None
    
    def set_table_2675_countries_df(self, df: pd.DataFrame) -> None:
        st.session_state.table_2675_countries_df = df
        
    def get_table_2675_countries_df(self) -> pd.DataFrame:
        return st.session_state.table_2675_countries_df

    def set_menu_option(self, option: Literal["Home", "Settings", "Table 2675 Analysis"]) -> None:
        st.session_state.menu_option = option
        
    def get_menu_option(self) -> Literal["Home", "Settings", "Table 2675 Analysis"]:
        return st.session_state.menu_option

    def reset_colors(self) -> None:
        st.session_state.background_color = "#0E1117"
        st.session_state.secondary_background_color = "#262730"
        st.session_state.text_color = "#FAFAFA"
        st.session_state.primary_color = "#FF4B4B"
        
    def save_colors(
        self,
        background_color: str,
        secondary_background_color: str, 
        text_color: str,
        primary_color: str) -> None:
        
        st.session_state.background_color = background_color
        st.session_state.secondary_background_color = secondary_background_color
        st.session_state.text_color = text_color
        st.session_state.primary_color = primary_color
        
    def set_background_color(self, color: str) -> None:
        st.session_state.background_color = color
        
    def set_secondary_background_color(self, color: str) -> None:
        st.session_state.secondary_background_color = color
        
    def set_text_color(self, color: str) -> None:
        st.session_state.text_color = color
        
    def set_primary_color(self, color: str) -> None:
        st.session_state.primary_color = color
        
    def get_background_color(self) -> str:
        return st.session_state.background_color
    
    def get_secondary_background_color(self) -> str:
        return st.session_state.secondary_background_color
    
    def get_text_color(self) -> str:
        return st.session_state.text_color
    
    def get_primary_color(self) -> str:
        return st.session_state.primary_color