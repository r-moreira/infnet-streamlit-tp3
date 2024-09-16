import streamlit as st
import time
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta
from io import BytesIO
from view.abstract_streamlit_view import AbstractStreamlitView
from service.session_state_service import SessionStateService
from service.data_rio_parser_service import DataRioParserService
from streamlit_extras.add_vertical_space import add_vertical_space
from view.sidebar_view import SidebarView
from geopy.geocoders import Photon

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
                filtered_countries_df = self.render_multiselect_filter(
                    self.session_state_service.get_table_2675_countries_df(),
                    {
                        "Country": "País"
                    }
                )
                filtered_countries_df = self.render_year_slider_filter(filtered_countries_df)
                
                self.display_table_2675_data(filtered_countries_df, "table2675_countries_data.csv")
                self.display_countries_plots(filtered_countries_df)
           
            elif dataset_option == "Continents":
                filtered_continents_df = self.render_multiselect_filter(
                    self.session_state_service.get_table_2675_continents_df(),
                    {
                        "Continent": "Continente"
                    }
                )
                filtered_continents_df = self.render_year_slider_filter(filtered_continents_df)
                
                self.display_table_2675_data(filtered_continents_df, "table_2675_continents_data.csv")
                self.display_continents_plots(filtered_continents_df)
    
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
                    
    def display_continents_plots(self, df: pd.DataFrame) -> None:
        add_vertical_space(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x="Continente", y="Total", title="Total Tourists by Continent", template="plotly_dark")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        with col2:
            fig = px.pie(df, names="Continente", values="Total", title="Total Tourists by Continent", template="plotly_dark")
            st.plotly_chart(fig)
        
        fig = go.Figure()
        for continent in df["Continente"].unique():
            continent_data = df[df["Continente"] == continent]
            fig.add_trace(go.Scatter(x=continent_data["year"], y=continent_data["Total"], mode='lines', name=continent))
        fig.update_layout(title="Monthly Tourists by Continent", template="plotly_dark")
        st.plotly_chart(fig)
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=0,
                longitude=0,
                zoom=1,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_fill_color='[200, 30, 0, 160]',
                    get_radius='Total',
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
        ))
            
    def display_countries_plots(self, df: pd.DataFrame) -> None:
        add_vertical_space(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x="País", y="Total", title="Total Tourists by Country", template="plotly_dark")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        with col2:
            fig = px.pie(df, names="País", values="Total", title="Total Tourists by Country", template="plotly_dark")
            st.plotly_chart(fig)
        
        fig = go.Figure()
        for country in df["País"].unique():
            country_data = df[df["País"] == country]
            fig.add_trace(go.Scatter(x=country_data["year"], y=country_data["Total"], mode='lines', name=country))
        fig.update_layout(title="Monthly Tourists by Country", template="plotly_dark")
        st.plotly_chart(fig)
        
        df = self.prepare_dataframe_for_pydeck(df, "País")
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=0,
                longitude=0,
                zoom=1,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_fill_color='[color, 140, 0, 160]',
                    get_radius='Total',
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
        ))
    
    def display_continents_plots(self, df: pd.DataFrame) -> None:
        add_vertical_space(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x="Continente", y="Total", title="Total Tourists by Continent", template="plotly_dark")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)
        
        with col2:
            fig = px.pie(df, names="Continente", values="Total", title="Total Tourists by Continent", template="plotly_dark")
            st.plotly_chart(fig)
        
        fig = go.Figure()
        for continent in df["Continente"].unique():
            continent_data = df[df["Continente"] == continent]
            fig.add_trace(go.Scatter(x=continent_data["year"], y=continent_data["Total"], mode='lines', name=continent))
        fig.update_layout(title="Monthly Tourists by Continent", template="plotly_dark")
        st.plotly_chart(fig)
        
        df = self.prepare_dataframe_for_pydeck(df, "Continente")
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=0,
                longitude=0,
                zoom=1,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_fill_color='[color, 140, 0, 160]',
                    get_radius='Total',
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
        ))
            
        
    def render_multiselect_filter(self, df: pd.DataFrame, col_map: dict) -> pd.DataFrame:
        add_vertical_space(1)
        
        for display_name, column_name in col_map.items():
            options = sorted(df[column_name].unique())
            selected_options = st.multiselect(display_name, options, default=options[:1]) #TODO: Select some options by default
            
            if selected_options:
                df = df[df[column_name].isin(selected_options)]
    
        return df   

    def render_year_slider_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        add_vertical_space(1)
        
        min_year = int(df["year"].min())
        max_year = int(df["year"].max())
        selected_year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))
        
        df = df[(df["year"] >= selected_year_range[0]) & (df["year"] <= selected_year_range[1])]
        
        return df
    
    def prepare_dataframe_for_pydeck(self, df: pd.DataFrame, location_column: str) -> pd.DataFrame:
        geolocator = Photon(user_agent="geoapiExercises")
        
        def get_lat_long(location):
            try:
                print(f"Getting lat/long for {location}")
                location_data = geolocator.geocode(f"País, {location}")
                return location_data.latitude, location_data.longitude
            except Exception as e:
                print(f"Error getting lat/long for {location} - {e}")
                return 0, 0
        
        # Get unique locations
        unique_locations = df[location_column].unique()
        
        # Fetch lat/long for unique locations
        location_coords = {location: get_lat_long(location) for location in unique_locations}
        
        # Map lat/long back to the original dataframe
        df["latitude"] = df[location_column].map(lambda x: location_coords[x][0])
        df["longitude"] = df[location_column].map(lambda x: location_coords[x][1])
        
        # Normalize the tourist data for coloring
        df['color'] = df['Total'] / df['Total'].max() * 255
        
        return df