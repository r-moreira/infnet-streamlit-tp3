import streamlit as st
import time
from io import BytesIO
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from streamlit_extras.add_vertical_space import add_vertical_space

class HomeView(AbstractStreamlitView):
    def __init__(self, session_state_service: SessionStateService) -> None:
        self.session_state_service = session_state_service
        
    def render(self) -> None:
        st.title("🌐 Data Rio Tourism Analysis")
        
        st.markdown("### Explore Tourism Data in Rio de Janeiro")
        
        st.divider()
        
        st.markdown("""
            Welcome to the Data Rio Tourism Analysis app! Here, you can delve into comprehensive tourism data for Rio de Janeiro, sourced directly from [Data Rio](https://www.data.rio/search?groupIds=729990e9fbc04c6ebf81715ab438cae8).
        """)
        
        add_vertical_space(1)
        
        st.markdown("""
            #### Data Source
            We utilize the following dataset for our analysis:
            - **[Monthly arrival of tourists in Rio de Janeiro by air, according to continents and countries of permanent residence, between 2006-2019](https://www.data.rio/documents/a6c6c3ff7d1947a99648494e0745046d/about)**
        """)
        
        add_vertical_space(1)
        
        st.markdown("""
            #### Supported Tables
            The Data Rio website hosts numerous tables with various datasets. Currently, this app supports:
            - **Table 2675**: Monthly arrival of tourists by air, segmented by continents and countries of permanent residence.
        """)
        
        add_vertical_space(2)
        
        st.markdown("""
            #### How to Use
            - Navigate through the app using the sidebar.
            - Select different options to explore various aspects of the tourism data.
            - Customize your view and analysis using the settings provided.
        """)
        
        add_vertical_space(2)
        
        st.markdown("""
            We hope you find this app insightful and useful for your analysis of tourism trends in Rio de Janeiro. Happy exploring!
        """)