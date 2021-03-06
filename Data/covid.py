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
            covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCI??N"].values, inplace=True)

def clean_paises(field):
    covid_df[field].replace("M????xico", "M??xico", inplace=True)
    covid_df[field].replace("Hait????", "Hait??", inplace=True)
    covid_df[field].replace("Espa????a", "Espa??a", inplace=True)
    covid_df[field].replace("Canad????", "Canad??", inplace=True)
    covid_df[field].replace("Rep????blica Oriental del Uruguay", "Rep??blica Oriental del Uruguay", inplace=True)
    covid_df[field].replace("Rep????blica de Honduras", "Rep??blica de Honduras", inplace=True)
    covid_df[field].replace("Rep????blica de Corea", "Rep??blica de Corea", inplace=True)
    covid_df[field].replace("Rep????blica de Costa Rica", "Rep??blica de Costa Rica", inplace=True)
    covid_df[field].replace("Rep????blica Dominicana", "Rep??blica Dominicana", inplace=True)
    covid_df[field].replace("Rep????blica de Panam????", "Rep??blica de Panam??", inplace=True)
    covid_df[field].replace("Rep????blica de Mauricio", "Rep??blica de Mauricio", inplace=True)
    covid_df[field].replace("Rep????blica de Angola", "Rep??blica de Angola", inplace=True)
    covid_df[field].replace("Jap????n", "Jap??n", inplace=True)
    covid_df[field].replace("Per????", "Per??", inplace=True)
    covid_df[field].replace("Taiw????n", "Taiw??n", inplace=True)
    covid_df[field].replace("Gran Breta????a (Reino Unido)", "Gran Breta??a (Reino Unido)", inplace=True)
    covid_df[field].replace("Archipi????lago de Svalbard", "Archipi??lago de Svalbard", inplace=True)
    covid_df[field].replace("Ir????n", "Ir??n", inplace=True)
    covid_df[field].replace("Hungr????a", "Hungr????a", inplace=True)
    covid_df[field].replace("Ascensi????n", "Ascensi??n", inplace=True)
    covid_df[field].replace("Principado de M????naco", "Principado de M??naco", inplace=True)
    covid_df[field].replace("Turqu????a", "Turqu????a", inplace=True)
    covid_df[field].replace("Pakist????n", "Pakist??n", inplace=True)
    covid_df[field].replace("Camer????n", "Camer??n", inplace=True)
    covid_df[field].replace("Sud????frica", "Sud??frica", inplace=True)
    covid_df[field].replace("Sud????n", "Sud??n", inplace=True)
    covid_df[field].replace("L????bano", "L??bano", inplace=True)

        
load_files()

#print(covid_df.isnull().sum())
#covid_df.dropna(inplace=True)
#dup1=covid_df
#dup2=covid_df

#dup1[dup1.duplicated()]
#dup2.drop_duplicates(kepp='first', inplace=True)

print(covid_df['ENTIDAD_RES'].value_counts())