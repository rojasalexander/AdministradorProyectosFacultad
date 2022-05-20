import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta


data = pd.read_csv("data.csv") # datos del archivo csv 


#convertir los datos str a datetime AAAA-MM-DD
data["Inicio"] = pd.to_datetime(data["Inicio"], format="%Y-%m-%d")
data["Fin"] = pd.to_datetime(data["Fin"], format="%Y-%m-%d")


#ordenar las tareas por fecha de inicio
data.sort_values("Inicio",axis=0, ascending=True, inplace=True) #axis=0 para ordenar por columnas #ascending=True para ordenar de menor a mayor #inplace=True para que se modifique el dataframe original
# resetear el indice de cada tarea
data.reset_index(drop=True, inplace=True) #drop = True el indice actual se elimina y el indice numerico lo reemplaza #inplace=True para que se modifique el dataframe original

# añade la duracion de la tarea
data["Duracion"] = data["Fin"] - data["Inicio"] + timedelta(days=1)  
# se  añade la columna 
data["Desde Inicio"]= data["Inicio"] - data["Inicio"][0]

print(data)



