from math import comb
import pandas as pd
import numpy as np 
import json

data_file="export_dataframe.xlsx"

xl= pd.ExcelFile(data_file)
covid_df=xl.parse("Sheet1")


#Casos por entidad

casos_entidad = covid_df.groupby(["ENTIDAD_RES"], as_index=False)["ID_REGISTRO"].count()
casos_entidad.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
casos_entidad["ENTIDAD_RES"].replace("AS", "Aguascalientes", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("BC", "Baja California", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("BS", "Baja California Sur", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("CC", "Campeche", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("CH", "Chihuahua", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("CL", "Coahuila", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("CM", "Colima", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("CS", "Chiapas", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("DF", "CDMX", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("DG", "Durango", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("GR", "Guerrero", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("GT", "Guanajuato", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("HG", "Hidalgo", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("JC", "Jalisco", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("MC", "Estado de Mexico", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("MN", "Michoacan", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("MS", "Morelos", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("NL", "Nuevo Leon", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("NT", "Nayarit", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("OC", "Oaxaca", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("PL", "Puebla", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("QR", "Quintana Roo", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("QT", "Queretaro", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("SL", "Sinaloa", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("SP", "San Luis Potosi", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("SR", "Sonora", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("TC", "Tabasco", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("TL", "Tlaxcala", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("TS", "Tamaulipas", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("VZ", "Veracruz", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("YN", "Yucatan", inplace=True)
casos_entidad["ENTIDAD_RES"].replace("ZS", "Zacatecas", inplace=True)

casos_entidad.to_json(r'covid_data/casos_entidad.json', orient="records")


#Casos diabete neumonia


diabetes_entidad = covid_df[covid_df["DIABETES"] == "SI "].groupby("ENTIDAD_RES", as_index=False)["ID_REGISTRO"].count()
diabetes_entidad.rename(columns={"ID_REGISTRO": "CASOS_DIABETES"}, inplace=True)

neumonia_entidad = covid_df[covid_df["NEUMONIA"] == "SI "].groupby("ENTIDAD_RES", as_index=False)["ID_REGISTRO"].count()
neumonia_entidad.rename(columns={"ID_REGISTRO": "CASOS_NEUMONIA"}, inplace=True)

tot_contagio = diabetes_entidad.merge(neumonia_entidad, how='inner', on='ENTIDAD_RES')

tot_contagio["ENTIDAD_RES"].replace("AS", "Aguascalientes", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("BC", "Baja California", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("BS", "Baja California Sur", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("CC", "Campeche", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("CH", "Chihuahua", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("CL", "Coahuila", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("CM", "Colima", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("CS", "Chiapas", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("DF", "CDMX", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("DG", "Durango", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("GR", "Guerrero", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("GT", "Guanajuato", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("HG", "Hidalgo", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("JC", "Jalisco", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("MC", "Estado de Mexico", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("MN", "Michoacan", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("MS", "Morelos", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("NL", "Nuevo Leon", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("NT", "Nayarit", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("OC", "Oaxaca", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("PL", "Puebla", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("QR", "Quintana Roo", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("QT", "Queretaro", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("SL", "Sinaloa", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("SP", "San Luis Potosi", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("SR", "Sonora", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("TC", "Tabasco", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("TL", "Tlaxcala", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("TS", "Tamaulipas", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("VZ", "Veracruz", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("YN", "Yucatan", inplace=True)
tot_contagio["ENTIDAD_RES"].replace("ZS", "Zacatecas", inplace=True)

tot_contagio.to_json(r'covid_data/diab_neu.json', orient="records")

#Muertes 2020

muertes_mes = covid_df[covid_df["FECHA_DEF_YR"] == 2020].groupby("FECHA_DEF_MT", as_index=False)["ID_REGISTRO"].count()
muertes_mes["MES"]=muertes_mes["FECHA_DEF_MT"]  
muertes_mes.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
muertes_mes.rename(columns={"FECHA_DEF_MT": "MES_NOMBRE"}, inplace=True)
      
muertes_mes["MES_NOMBRE"].replace(1, "Enero", inplace=True)
muertes_mes["MES_NOMBRE"].replace(2, "Febrero", inplace=True)
muertes_mes["MES_NOMBRE"].replace(3, "Marzo", inplace=True)
muertes_mes["MES_NOMBRE"].replace(4, "Abril", inplace=True)
muertes_mes["MES_NOMBRE"].replace(5, "Mayo", inplace=True)
muertes_mes["MES_NOMBRE"].replace(6, "Junio", inplace=True)
muertes_mes["MES_NOMBRE"].replace(7, "Julio", inplace=True)
muertes_mes["MES_NOMBRE"].replace(8, "Agosto", inplace=True)
muertes_mes["MES_NOMBRE"].replace(9, "Septiembre", inplace=True)
muertes_mes["MES_NOMBRE"].replace(10, "Octubre", inplace=True)
muertes_mes["MES_NOMBRE"].replace(11, "Noviembre", inplace=True)
muertes_mes["MES_NOMBRE"].replace(12, "Diciembre", inplace=True)
muertes_mes.to_json(r'covid_data/muertes_2020.json', orient="records")


#Paciente sexo


paciente_sexo = covid_df.groupby(["TIPO_PACIENTE", "SEXO"], as_index=False)["ID_REGISTRO"].count()
paciente_sexo.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
paciente_sexo["TIPO_PACIENTE"].replace("HOSPITALIZADO", "Hospitalizado", inplace=True)
paciente_sexo["TIPO_PACIENTE"].replace("AMBULATORIO", "Ambulatorio", inplace=True)
paciente_sexo["SEXO"].replace("HOMBRE", "Hombre", inplace=True)
paciente_sexo["SEXO"].replace("MUJER", "Mujer", inplace=True)
paciente_sexo.rename(columns={"ORIGEN": "SECTOR"}, inplace=True)
paciente_sexo.to_json(r'covid_data/paciente_sexo.json', orient="records")



