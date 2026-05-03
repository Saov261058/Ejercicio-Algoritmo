"""
Universidad del Valle de Guatemala
Laboratorio 3
Estudiantes: Sebastian Orantes y Lester López
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="DataInsight Analytics", layout="wide")
st.title("DataInsight Analytics - Laboratorio 2")

path = os.getcwd()

# CARGA DE DATOS 
vehiculo = pd.read_csv(f"{path}/Electric_Vehicle_Population-2.csv")
gym      = pd.read_csv(f"{path}/GymExerciseTracking.csv")
nf       = pd.read_csv(f"{path}/netflix_titles.csv")
steam    = pd.read_csv(f"{path}/steam_store_data_2024.csv")

# LIMPIEZA 
steam["Precio"] = steam["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
steam["Descuento"] = steam["salePercentage"].str.replace(r"[^\d.]", "", regex=True).replace("", "0").astype(float)

nf["DuracionMin"] = pd.to_numeric(nf["duration"].str.extract(r"(\d+)")[0], errors="coerce")
nf["AnioAgregado"] = pd.to_numeric(nf["date_added"].str.extract(r"(\d{4})")[0], errors="coerce")

