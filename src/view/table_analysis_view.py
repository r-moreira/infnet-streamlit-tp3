import streamlit as st
import time
import pandas as pd
import base64
from datetime import timedelta
from io import BytesIO
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from service.data_rio_parser_service import DataRioParserService
from streamlit_extras.add_vertical_space import add_vertical_space
from view.sidebar_view import SidebarView

class TableAnalysisView(AbstractStreamlitView):
    def __init__(
        self,
        session_state_service: SessionStateService,
        data_rio_parser_service: DataRioParserService,
        sidebar_view: SidebarView) -> None:
        
        self.session_state_service = session_state_service
        self.data_rio_parser_service = data_rio_parser_service
        self.sidebar_view = sidebar_view
        
    
    def render(self) -> None:
        st.title("Table Analysis")
        
        add_vertical_space(1) 
        
        st.write("Here you can analyze the tables of the Data Rio Turism Analysis.")
        
        add_vertical_space(2)
        
        self.uploading_form()
        
        if self.session_state_service.is_table_2675_dataframes_set():       
            st.success("File uploaded successfully!")            
            
            dataset_option = self.sidebar_view.render_sub_menu()
            
            if dataset_option == "Countries":
                self.display_table_2675_countries_data()
            elif dataset_option == "Continents":
                self.display_table_2675_continents_data()
    
    def uploading_form(self) -> None:
        with st.form("upload_2675", clear_on_submit=True):
            st.write("Please, upload the data from Data Rio Turism, table: 2675.xls")
            file_content = st.file_uploader("Select the Data Rio file", type=["xls"])
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                time.sleep(1)
                df_continents, df_countries = self.parse_file_content(file_content)
                
                self.session_state_service.set_table_2675_continents_df(df_continents)
                self.session_state_service.set_table_2675_countries_df(df_countries)
    
    @st.cache_data(show_spinner=True, ttl=timedelta(days=7))
    def parse_file_content(_self, file_content: BytesIO) -> tuple[pd.DataFrame, pd.DataFrame]:            
        time.sleep(2)
            
        return _self.data_rio_parser_service.parse_table_2675(file_content)
    
    def display_table_2675_continents_data(self) -> None:
        with st.expander("Show Raw Data"):
            st.write(self.session_state_service.get_table_2675_continents_df())
            
            st.download_button(
                "Download Data", 
                self.session_state_service.get_table_2675_continents_df().to_csv(), 
                "table_2675_continents_data.csv")
    
    def display_table_2675_countries_data(self) -> None:
        with st.expander("Show Raw Data"):
            st.write(self.session_state_service.get_table_2675_countries_df())
            
            st.download_button(
                "Download Data", 
                self.session_state_service.get_table_2675_countries_df().to_csv(),
                "table2675_countries_data.csv"
            )