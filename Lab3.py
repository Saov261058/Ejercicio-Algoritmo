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

# FUNCIONES REUTILIZABLES
def exploracion(df):
    st.write("Filas y columnas:", df.shape)
    st.write("Columnas:", list(df.columns))
    st.dataframe(df.head(6))
    st.dataframe(df.describe())

def grafico(conteo, titulo, x, y):
    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    st.pyplot(fig)

def guardar(df, nombre):
    df.to_csv(f"{path}/{nombre}", index=False)
    st.success(f"Archivo guardado: {nombre}")

# TABS 
tab1, tab2, tab3, tab4 = st.tabs(["Vehiculos Electricos", "Gimnasio", "Videojuegos", "Netflix"])

# VEHICULOS
with tab1:
    st.header("1. Exploracion Inicial")
    exploracion(vehiculo)

    st.header("2. Agregar")
    with st.form("vehiculo"):
        data = {
            "VIN (1-10)": st.text_input("VIN", "NUEVO00001"),
            "City": st.text_input("Ciudad", "Guatemala"),
            "Model Year": st.number_input("Año", 2000, 2025, 2022),
            "Make": st.text_input("Marca", "Tesla"),
            "Model": st.text_input("Modelo", "Model 3"),
            "Electric_Range": st.number_input("Rango", 0, 1000, 250),
            "Base_MSRP": st.number_input("MSRP", 0, 845000, 40000)
        }
        if st.form_submit_button("Agregar"):
            vehiculo.loc[len(vehiculo)] = data
            st.success(f"Total: {len(vehiculo)}")

    st.header("3. Filtrado")
    st.dataframe(vehiculo[vehiculo["Model Year"] < st.number_input("Año <", 2000, 2025, 2015)].head(20))
    st.dataframe(vehiculo[vehiculo["Base_MSRP"] < st.number_input("MSRP <", 0, 845000, 50000)].head(20))

    st.header("4. Avanzado")
    vehiculo["RangoCategoria"] = pd.cut(vehiculo["Electric_Range"],
                                       bins=[-1,100,250,9999],
                                       labels=["Bajo","Medio","Alto"])
    conteo = vehiculo["RangoCategoria"].value_counts()
    st.dataframe(conteo)
    grafico(conteo, "Vehiculos por Rango", "Categoria", "Cantidad")

    st.write("Media MSRP:", vehiculo["Base_MSRP"].mean())
    guardar(vehiculo, "Electric_Vehicle_Population_Actualizado.csv")