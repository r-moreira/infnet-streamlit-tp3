import streamlit as st
from view.abstract_streamlit_view import AbstractStreamlitView

class SidebarView(AbstractStreamlitView):

    @staticmethod
    def render():
        st.sidebar.title("Sidebar")
        st.sidebar.write("This is the sidebar.")