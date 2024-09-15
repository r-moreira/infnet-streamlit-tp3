import streamlit as st
import time
from io import BytesIO
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from service.data_rio_parser_service import DataRioParserService
from streamlit_extras.add_vertical_space import add_vertical_space

class TableAnalysisView(AbstractStreamlitView):
    def __init__(
        self,
        session_state_service: SessionStateService,
        data_rio_parser_service: DataRioParserService) -> None:
        
        self.session_state_service = session_state_service
        self.data_rio_parser_service = data_rio_parser_service
        
    
    def render(self) -> None:
        st.title("Table Analysis")
        
        st.write("Here you can analyze the tables of the Data Rio Turism Analysis.")
        
        self.uploading_form()
    
    def uploading_form(self) -> None:
        with st.form("upload_2675", clear_on_submit=True):
            st.write("Please, upload the data from Data Rio Turism, table: 2675.xls")
            file_content = st.file_uploader("Select the Data Rio file", type=["xls"])
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                self.uploading_status(file_content)
    
    
    def uploading_fragment(self, file_content: BytesIO) -> None:            
        with st.status("Uploading the file..."):
            time.sleep(1)
            
        st.success("File uploaded successfully!")