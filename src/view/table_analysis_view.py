import streamlit as st
import time
import pandas as pd
from datetime import timedelta
from io import BytesIO
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from service.data_rio_parser_service import DataRioParserService
from streamlit_extras.add_vertical_space import add_vertical_space
from view.sidebar_view import SidebarView
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium import Choropleth
from folium.plugins import HeatMap
import json
import requests
from streamlit_folium import folium_static
from typing import Literal


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
        
        st.markdown("### Here you can analyze the table 2675 of the Data Rio")
        
        if not self.session_state_service.is_table_2675_dataframes_set():
            self.uploading_form()
        
        if self.session_state_service.is_table_2675_dataframes_set():   
        
            st.success("File uploaded successfully!")      
                
            dataset_option = self.sidebar_view.render_sub_menu()
            if dataset_option == "Countries":
                pass
                filtered_countries_df = self.render_multiselect_filter(
                    self.session_state_service.get_table_2675_countries_df(),
                    "Country"
                )
                filtered_countries_df = self.render_year_slider_filter(filtered_countries_df)
                
                self.display_table_2675_data(filtered_countries_df, "table2675_countries_data.csv")
                self.display_countries_plots(filtered_countries_df)
                self.display_folium_map(filtered_countries_df, "Country")
           
            elif dataset_option == "Continents":
                pass
                filtered_continents_df = self.render_multiselect_filter(
                    self.session_state_service.get_table_2675_continents_df(),
                    "Continent"
                )
                filtered_continents_df = self.render_year_slider_filter(filtered_continents_df)
                
                self.display_table_2675_data(filtered_continents_df, "table_2675_continents_data.csv")
                self.display_continents_plots(filtered_continents_df)
                self.display_folium_map(filtered_continents_df, "Continent")
    
    def uploading_form(self) -> None:
        add_vertical_space(2)
        
        with st.form("upload_2675", clear_on_submit=True):
            st.write("Please, upload the data from Data Rio Turism")
            file_content = st.file_uploader("Select the Data Rio file", type=["xls"])
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                time.sleep(1)
                df_continents, df_countries = self.parse_file_content(file_content)
                
                self.session_state_service.set_table_2675_continents_df(df_continents)
                self.session_state_service.set_table_2675_countries_df(df_countries)
                self.session_state_service.set_menu_option("Table 2675 Analysis")
                st.rerun()
                
    
    @st.cache_data(show_spinner=True, ttl=timedelta(days=7))
    def parse_file_content(_self, file_content: BytesIO) -> tuple[pd.DataFrame, pd.DataFrame]:            
        time.sleep(3)
            
        return _self.data_rio_parser_service.parse_table_2675(file_content)
    
    def display_table_2675_data(self, df: pd.DataFrame, download_filename: str) -> None:
        add_vertical_space(1)
        
        st.write(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "Download Data", 
                df.to_csv(),
                download_filename,
                use_container_width=True
            )
        
        with col2:
            clear_data = st.button(
                "Clear Data",
                on_click=self.session_state_service.clear_table_2675_dataframes,
                use_container_width=True
            )
            if clear_data:
                self.session_state_service.set_menu_option("Table 2675 Analysis")
                st.rerun()
                    
    def display_countries_plots(self, df: pd.DataFrame) -> None:
        add_vertical_space(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x="Country", y="Total", title="Total Tourists by Country", template="plotly_dark")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        with col2:
            fig = px.pie(df, names="Country", values="Total", title="Total Tourists by Country", template="plotly_dark")
            st.plotly_chart(fig)
        
        fig = go.Figure()
        for country in df["Country"].unique():
            country_data = df[df["Country"] == country]
            fig.add_trace(go.Scatter(x=country_data["Year"], y=country_data["Total"], mode='lines', name=country))
        fig.update_layout(title="Monthly Tourists by Country", template="plotly_dark")
        st.plotly_chart(fig)
    
    def display_continents_plots(self, df: pd.DataFrame) -> None:
        add_vertical_space(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x="Continent", y="Total", title="Total Tourists by Continent", template="plotly_dark")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        with col2:
            fig = px.pie(df, names="Continent", values="Total", title="Total Tourists by Continent", template="plotly_dark")
            st.plotly_chart(fig)
        
        fig = go.Figure()
        for continent in df["Continent"].unique():
            continent_data = df[df["Continent"] == continent]
            fig.add_trace(go.Scatter(x=continent_data["Year"], y=continent_data["Total"], mode='lines', name=continent))
        fig.update_layout(title="Monthly Tourists by Continent", template="plotly_dark")
        st.plotly_chart(fig)
    

    def display_folium_map(self, df: pd.DataFrame, display_type: Literal["Country", "Continent"]) -> None:
        if display_type == "Continent":
            geojson_path = "data/02_processed/custom.geo.json"
            with open(geojson_path) as f:
                geojson_data = json.load(f)
            key_on = "feature.properties.continent"
            columns = ["Continent", "Total"]
            legend_name = "Number of Tourists by Continent"
        else:
            geojson_url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"
            geojson_data = requests.get(geojson_url).json()
            key_on = "feature.properties.name"
            columns = ["Country", "Total"]
            legend_name = "Number of Tourists by Country"
        
        m = folium.Map(location=[0, 0], zoom_start=2, tiles=None)
        
        folium.TileLayer(
            tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
            attr='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name='Stadia Alidade Smooth Dark'
        ).add_to(m)
        
        Choropleth(
            geo_data=geojson_data,
            name="choropleth",
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        
        folium_static(m)
        
    def render_multiselect_filter(self, df: pd.DataFrame, column_name: dict) -> pd.DataFrame:
        add_vertical_space(1)
        
        options = sorted(df[column_name].unique())
        selected_options = st.multiselect(column_name, options, default=options[:7])
        
        if selected_options:
            df = df[df[column_name].isin(selected_options)]
        
        return df

    def render_year_slider_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        add_vertical_space(1)
        
        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())
        selected_year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))
        
        df = df[(df["Year"] >= selected_year_range[0]) & (df["Year"] <= selected_year_range[1])]
        
        return df