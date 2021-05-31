import pandas as pd
import numpy as np 
import math
import json
import os.path

data_file = "COVID_MX_2020.xlsx"
catalog_file ="Catalogos.xlsx"
desc_file="descriptor.json"

catalogs = {}
mappings = {}
covid_df = None

def load_files():
    global covid_df
    global mappings
    #read the descriptor from the json file
    j_file = open(desc_file,"r")
    desc=json.loads(j_file.read())
    mappings=desc["fields"]
    load_catalogs(desc)
    j_file.close()

    print("Loading data source...")
    #load the main data source
    if not os.path.exists('export_dataframe.xlsx'):
        xl = pd.ExcelFile(data_file)
        covid_df = xl.parse('Hoja1')
        #Describe our main data set
        #print(covid_df.index)       #gives me the range of the indices (numer of rows)
        
        #Gives me rows and columns
        print("The data set contains "+ str(covid_df.shape[0]) + " rows by "+ str(covid_df.shape[1]) +" columns")
        
        #print(covid_df.dtypes)      #Describes my data spurce by telling me how did pandas identify each each column
        #print(covid_df.head(5))     #Prints the top n values of my data source
        print("Done")
        print("Cleaning data...")
        merge_clean_data()
        print("Done")
        pd.set_option('display.max_columns', None)
        print(covid_df.head(7))     #Prints the top n values of my data source
        #Save clean data
        covid_df.to_excel(r'export_dataframe.xlsx', index=False, header=True)
    else:
        xl=pd.ExcelFile('export_dataframe.xlsx')
        covid_df = xl.parse('Sheet1')
    



def load_catalogs(desc):
    print("Loading catalog...")
    cat_xl = pd.ExcelFile(catalog_file)
    for i in desc["catalogs"]:
        print("Catalogo: "+i)
        catalogs[i] = cat_xl.parse(i)
        #limpiar datos NaN
        catalogs[i].dropna(inplace=True)
        #Validate all the numeric columns to be integer
        dtypes = catalogs[i].dtypes.to_dict()
        if 'float64' in dtypes.values():
            for col_nan, typ in dtypes.items():
                if typ == 'float64':
                    catalogs[i][col_nan] = catalogs[i][col_nan].astype(int)
        
        
        #print(catalogs[i].dtypes)
        #print(catalogs[i].head())
    cat_num = catalogs["MUNICIPIOS"]
    cat_num['CODIGO'] = cat_num["CLAVE_ENTIDAD"].astype(str) + "_"+ cat_num["CLAVE_MUNICIPIO"].astype(str)

    print("Done")

def merge_clean_data():
    for fields in mappings:
        field=fields["name"]
        print(field)
        if fields["format"] == "ID":
            covid_df.set_index(field)
        elif fields["format"] == "DATE":
            #CLEAN DATA OF EMPTY FIELDS
            covid_df[field] = pd.to_datetime(covid_df[field], errors='coerce').fillna('')
            #SPREAD VALUES IN DIFFERENT FIELDS
            covid_df[field + '_YR'] = covid_df[field].apply(lambda x: x.year if x!= '' else x)
            covid_df[field + '_MT'] = covid_df[field].apply(lambda x: x.month if x!= '' else x)
            covid_df[field + '_DY'] = covid_df[field].apply(lambda x: x.day if x!= '' else x)
            covid_df[field + '_WK'] = covid_df[field].apply(lambda x: x.week if x!= '' else x)
        elif fields["format"] == "MUNICIPIOS":
            catalog = catalogs[fields["format"]]
            relation = fields['relation']
            covid_df[field] = covid_df[relation].astype(str) + "_" + covid_df[field].astype(str)
            covid_df[field].replace(catalog['CODIGO'].values, catalog['MUNICIPIO'].values, inplace=True )
        elif fields["format"] == "ENTIDADES":
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE_ENTIDAD"].values, catalog["ABREVIATURA"].values, inplace=True)
        elif fields["name"] == "PAIS_NACIONALIDAD":
            clean_paises(field)           

        elif fields["format"] in catalogs.keys():
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCIÓN"].values, inplace=True)

def clean_paises(field):
    covid_df[field].replace("MÃ©xico", "México", inplace=True)
    covid_df[field].replace("HaitÃ­", "Haití", inplace=True)
    covid_df[field].replace("EspaÃ±a", "España", inplace=True)
    covid_df[field].replace("CanadÃ¡", "Canadá", inplace=True)
    covid_df[field].replace("RepÃºblica Oriental del Uruguay", "República Oriental del Uruguay", inplace=True)
    covid_df[field].replace("RepÃºblica de Honduras", "República de Honduras", inplace=True)
    covid_df[field].replace("RepÃºblica de Corea", "República de Corea", inplace=True)
    covid_df[field].replace("RepÃºblica de Costa Rica", "República de Costa Rica", inplace=True)
    covid_df[field].replace("RepÃºblica Dominicana", "República Dominicana", inplace=True)
    covid_df[field].replace("RepÃºblica de PanamÃ¡", "República de Panamá", inplace=True)
    covid_df[field].replace("RepÃºblica de Mauricio", "República de Mauricio", inplace=True)
    covid_df[field].replace("RepÃºblica de Angola", "República de Angola", inplace=True)
    covid_df[field].replace("JapÃ³n", "Japón", inplace=True)
    covid_df[field].replace("PerÃº", "Perú", inplace=True)
    covid_df[field].replace("TaiwÃ¡n", "Taiwán", inplace=True)
    covid_df[field].replace("Gran BretaÃ±a (Reino Unido)", "Gran Bretaña (Reino Unido)", inplace=True)
    covid_df[field].replace("ArchipiÃ©lago de Svalbard", "Archipiélago de Svalbard", inplace=True)
    covid_df[field].replace("IrÃ¡n", "Irán", inplace=True)
    covid_df[field].replace("HungrÃ­a", "Hungrí­a", inplace=True)
    covid_df[field].replace("AscensiÃ³n", "Ascensión", inplace=True)
    covid_df[field].replace("Principado de MÃ³naco", "Principado de Mónaco", inplace=True)
    covid_df[field].replace("TurquÃ­a", "Turquí­a", inplace=True)
    covid_df[field].replace("PakistÃ¡n", "Pakistán", inplace=True)
    covid_df[field].replace("CamerÃºn", "Camerún", inplace=True)
    covid_df[field].replace("SudÃ¡frica", "Sudáfrica", inplace=True)
    covid_df[field].replace("SudÃ¡n", "Sudán", inplace=True)
    covid_df[field].replace("LÃ­bano", "Líbano", inplace=True)

        
load_files()

#print(covid_df.isnull().sum())
#covid_df.dropna(inplace=True)
#dup1=covid_df
#dup2=covid_df

#dup1[dup1.duplicated()]
#dup2.drop_duplicates(kepp='first', inplace=True)

print(covid_df['ENTIDAD_RES'].value_counts())