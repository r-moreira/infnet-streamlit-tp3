import pandas as pd

class DataRioParserService:
    def __init__(self):
        self.table_2675_columns = [
            'Continentes e países de residência permanente',
            'Total',
            'Janeiro',
            'Fevereiro',
            'Março', 
            'Abril', 
            'Maio',
            'Junho', 
            'Julho',
            'Agosto', 
            'Setembro', 
            'Outubro',
            'Novembro', 
            'Dezembro',
            'year'  
        ]
        self.table_2675_continents = [
            'África',
            'América Central',
            'América Central e Caribe', 
            'América do Norte',
            'América do Sul',
            'Ásia', 
            'Europa',
            'Oceania'
        ]
    
    def _convert_xls_to_dataframe(self, xls_file_path: str) -> pd.DataFrame:
        xls = pd.ExcelFile(xls_file_path, engine='xlrd')
        all_sheets_df = pd.DataFrame()
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df['year'] = sheet_name  
            all_sheets_df = pd.concat([all_sheets_df, df], ignore_index=True)
        return all_sheets_df

    def _clean_and_separate_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        df.columns = self.table_2675_columns
        
        df.dropna(how='all', inplace=True)
        df = df[df.apply(lambda x: len(x.dropna()) == len(df.columns), axis=1)]
        df = df[df['Continentes e países de residência permanente'].str.strip().str.lower() != 'total']
        df.reset_index(drop=True, inplace=True)
        
        continents = []
        countries = []
        current_continent = None

        for _, row in df.iterrows():
            if pd.isna(row['Continentes e países de residência permanente']):
                continue
            if any(row['Continentes e países de residência permanente'].strip() == continent for continent in self.table_2675_continents):
                current_continent = row['Continentes e países de residência permanente']
                continents.append({'Continente': current_continent, **row.to_dict()})
            else:
                countries.append({'Continente': current_continent, **row.to_dict()})
        
        return pd.DataFrame(continents), pd.DataFrame(countries)

    def _clean_final_dataframes(self, continents_df: pd.DataFrame, countries_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        continents_df.drop(columns=['Continentes e países de residência permanente'], inplace=True)
        continents_df.loc[continents_df['Continente'] == 'América Central', 'Continente'] = 'América Central e Caribe'
        
        countries_df.rename(columns={'Continentes e países de residência permanente': 'País'}, inplace=True)
        countries_df['País'] = countries_df['País'].str.strip()
        countries_df.loc[countries_df['Continente'] == 'América Central', 'Continente'] = 'América Central e Caribe'
        countries_df.replace({'-': 0, ' - ': 0}, inplace=True)

        return continents_df, countries_df

    def get_from_table_2675(self, xls_file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        all_sheets_df = self._convert_xls_to_dataframe(xls_file_path)
        continents_df, countries_df = self._clean_and_separate_data(all_sheets_df)
        return self._clean_final_dataframes(continents_df, countries_df)