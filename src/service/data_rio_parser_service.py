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
            'Year'  
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
        
        self.country_translation = {
            "África do Sul": "South Africa",
            "Angola": "Angola",
            "Cabo Verde": "Cape Verde",
            "Nigéria": "Nigeria",
            "Outros": "Others",
            "Costa Rica": "Costa Rica",
            "Panamá": "Panama",
            "Porto Rico": "Puerto Rico",
            "Canadá": "Canada",
            "Estados Unidos": "United States",
            "México": "Mexico",
            "Argentina": "Argentina",
            "Bolívia": "Bolivia",
            "Chile": "Chile",
            "Colômbia": "Colombia",
            "Equador": "Ecuador",
            "Guiana Francesa": "French Guiana",
            "Paraguai": "Paraguay",
            "Peru": "Peru",
            "República da Guiana": "Guyana",
            "Suriname": "Suriname",
            "Uruguai": "Uruguay",
            "Venezuela": "Venezuela",
            "China": "China",
            "Japão": "Japan",
            "República da Coréia": "South Korea",
            "Alemanha": "Germany",
            "Áustria": "Austria",
            "Bélgica": "Belgium",
            "Dinamarca": "Denmark",
            "Espanha": "Spain",
            "Finlândia": "Finland",
            "França": "France",
            "Grécia": "Greece",
            "Holanda": "Netherlands",
            "Hungria": "Hungary",
            "Inglaterra": "England",
            "Irlanda": "Ireland",
            "Itália": "Italy",
            "Noruega": "Norway",
            "Polônia": "Poland",
            "Portugal": "Portugal",
            "Suécia": "Sweden",
            "Suíça": "Switzerland",
            "Austrália": "Australia",
            "Nova Zelândia": "New Zealand",
            "Oriente Médio": "Middle East",
            "Arábia Saudita": "Saudi Arabia",
            "Iraque": "Iraq",
            "Israel": "Israel",
            "Países não especificados": "Unspecified Countries",
            "Cuba": "Cuba",
            "Índia": "India",
            "República Tcheca": "Czech Republic",
            "Rússia": "Russia",
            "Egito": "Egypt",
            "Gana": "Ghana",
            "Marrocos": "Morocco",
            "Moçambique": "Mozambique",
            "Quênia": "Kenya",
            "Tunísia": "Tunisia",
            "Outros países da África": "Other African Countries",
            "El Salvador": "El Salvador",
            "Guatemala": "Guatemala",
            "Haiti": "Haiti",
            "Honduras": "Honduras",
            "Nicarágua": "Nicaragua",
            "República Dominicana": "Dominican Republic",
            "Trinidad e Tobago": "Trinidad and Tobago",
            "Outros países da América Central e Caribe": "Other Central American and Caribbean Countries",
            "Guiana": "Guyana",
            "Bangladesh": "Bangladesh",
            "China, Hong Kong": "Hong Kong",
            "Cingapura": "Singapore",
            "Filipinas": "Philippines",
            "Indonésia": "Indonesia",
            "Irã": "Iran",
            "Líbano": "Lebanon",
            "Malásia": "Malaysia",
            "Paquistão": "Pakistan",
            "Síria": "Syria",
            "Tailândia": "Thailand",
            "Taiwan": "Taiwan",
            "Outros países da Ásia": "Other Asian Countries",
            "Bulgária": "Bulgaria",
            "Croácia": "Croatia",
            "Eslováquia": "Slovakia",
            "Eslovênia": "Slovenia",
            "Estônia": "Estonia",
            "Letônia": "Latvia",
            "Lituânia": "Lithuania",
            "Luxemburgo": "Luxembourg",
            "Reino Unido": "United Kingdom",
            "Romênia": "Romania",
            "Sérvia": "Serbia",
            "Turquia": "Turkey",
            "Ucrânia": "Ukraine",
            "Outros países da Europa": "Other European Countries",
            "Outros países da Oceania": "Other Oceanian Countries"
        }
        
        self.continent_translation = {
            'África': 'Africa',
            'América Central': 'Central America',
            'América Central e Caribe': 'Central America and Caribbean',
            'América do Norte': 'North America',
            'América do Sul': 'South America',
            'Ásia': 'Asia',
            'Europa': 'Europe',
            'Oceania': 'Oceania'
        }
    
    def _convert_xls_to_dataframe(self, xls_file_path: str) -> pd.DataFrame:
        xls = pd.ExcelFile(xls_file_path, engine='xlrd')
        all_sheets_df = pd.DataFrame()
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df['Year'] = sheet_name  
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
        def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
            for column in df.columns:
                df[column] = df[column].astype(str).str.strip()
                if df[column].str.isnumeric().all():
                    df[column] = pd.to_numeric(df[column])
            return df
            
        continents_df.drop(columns=['Continentes e países de residência permanente'], inplace=True)
        continents_df.loc[continents_df['Continente'] == 'América Central', 'Continente'] = 'América Central e Caribe'
        
        countries_df.rename(columns={'Continentes e países de residência permanente': 'País'}, inplace=True)
        countries_df['País'] = countries_df['País'].str.strip()
        countries_df.loc[countries_df['Continente'] == 'América Central', 'Continente'] = 'América Central e Caribe'
        countries_df.replace({'-': 0, ' - ': 0}, inplace=True)
        
        continents_df['Continente'] = continents_df['Continente'].map(self.continent_translation)
        countries_df['País'] = countries_df['País'].map(self.country_translation)
        countries_df['Continente'] = countries_df['Continente'].map(self.continent_translation)
        
        countries_df.rename(columns={'País': 'Country', 'Continente': 'Continent'}, inplace=True)
        continents_df.rename(columns={'Continente': 'Continent'}, inplace=True)

        return  _clean_dataframe(continents_df), _clean_dataframe(countries_df)

    def parse_table_2675(self, xls_file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        all_sheets_df = self._convert_xls_to_dataframe(xls_file_path)
        continents_df, countries_df = self._clean_and_separate_data(all_sheets_df)
        return self._clean_final_dataframes(continents_df, countries_df)