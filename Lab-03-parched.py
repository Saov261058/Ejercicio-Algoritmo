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
st.title("Laboratorio 3")

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

    # ===================== PREGUNTAS CLAVE =====================
    st.header("5. Preguntas Clave")

    st.subheader("Relación Rango vs Año")
    corr1 = vehiculo[["Electric_Range", "Model Year"]].corr()
    st.write("Correlación:")
    st.dataframe(corr1)

    st.subheader("Relación Precio vs Rango")
    corr2 = vehiculo[["Base_MSRP", "Electric_Range"]].corr()
    st.write("Correlación:")
    st.dataframe(corr2)

# GIMNASIO
with tab2:
    st.header("1. Exploracion Inicial")
    exploracion(gym)

    st.header("3. Filtrado")
    st.dataframe(gym[gym["Calories_Burned"] >= st.number_input("Calorias >=", 0.0)].head(20))
    st.dataframe(gym[gym["Fat_Percentage"] <= st.number_input("Grasa <=", 0.0, 100.0, 25.0)].head(20))

    st.header("4. Avanzado")
    gym["NivelFrecuencia"] = pd.cut(gym["Workout_Frequency"],
                                    bins=[-1,2,5,7],
                                    labels=["Baja","Moderada","Alta"])
    conteo = gym["NivelFrecuencia"].value_counts()
    st.dataframe(conteo)
    grafico(conteo, "Frecuencia Gimnasio", "Nivel", "Cantidad")

    st.write("Media Session Duration:", gym["Session_Duration"].mean())
    guardar(gym, "GymExerciseTracking_Actualizado.csv")

    # ===================== PREGUNTAS CLAVE =====================
    st.header("5. Preguntas Clave")

    st.subheader("Calorias vs Duracion")
    corr3 = gym[["Calories_Burned", "Session_Duration"]].corr()
    st.dataframe(corr3)

    st.subheader("Grasa vs Experiencia")
    grupo = gym.groupby("Experience_Level")["Fat_Percentage"].mean()
    st.dataframe(grupo)

# STEAM 
with tab3:
    st.header("1. Exploracion Inicial")
    exploracion(steam)

    st.header("3. Filtrado")
    st.dataframe(steam[steam["Precio"] > st.number_input("Precio >", 0.0)].head(20))
    st.dataframe(steam[steam["Descuento"] < st.number_input("Descuento <", 0.0, 100.0, 50.0)].head(20))

    st.header("4. Avanzado")
    steam["GamaJuego"] = pd.cut(steam["Precio"],
                               bins=[-1,10,24,1000],
                               labels=["Baja","Media","Alta"])
    conteo = steam["GamaJuego"].value_counts()
    st.dataframe(conteo)
    grafico(conteo, "Gama Juegos", "Gama", "Cantidad")

    st.write("Media Precio:", steam["Precio"].mean())
    guardar(steam, "steam_store_data_2024_Actualizado.csv")

    # ===================== PREGUNTAS CLAVE =====================
    st.header("5. Preguntas Clave")

    if "review_score" in steam.columns:
        st.subheader("Calificacion por Gama")
        grupo2 = steam.groupby("GamaJuego")["review_score"].mean()
        st.dataframe(grupo2)

        st.subheader("Top juegos mejor calificados")
        top = steam.sort_values("review_score", ascending=False).head(10)
        st.dataframe(top[["name","Precio","review_score"]])
    else:
        st.warning("No existe columna de calificaciones en el dataset")

# NETFLIX 
with tab4:
    st.header("1. Exploracion Inicial")
    exploracion(nf)

    st.header("3. Filtrado")
    st.dataframe(nf[(nf["type"]=="Movie") &
                    (nf["DuracionMin"] > st.number_input("Duracion >", 0))].head(20))
    st.dataframe(nf[nf["AnioAgregado"] < st.number_input("Año <", 2000, 2024, 2020)].head(20))

    st.header("4. Avanzado")
    nf["TipoAudiencia"] = "Otros"
    nf.loc[nf["rating"].isin(["G","TV-Y","TV-G","TV-Y7","TV-Y7-FV"]), "TipoAudiencia"] = "Niños"
    nf.loc[nf["rating"].isin(["PG","TV-PG"]), "TipoAudiencia"] = "Adolescentes"
    nf.loc[nf["rating"].isin(["PG-13","TV-14"]), "TipoAudiencia"] = "Adultos Jovenes"
    nf.loc[nf["rating"].isin(["R","TV-MA","NC-17"]), "TipoAudiencia"] = "Adultos"

    conteo = nf["TipoAudiencia"].value_counts()
    st.dataframe(conteo)
    grafico(conteo, "Netflix Audiencia", "Tipo", "Cantidad")

    st.write("Duracion promedio:", nf["DuracionMin"].mean())
    guardar(nf, "netflix_titles_Actualizado.csv")

    # ===================== PREGUNTAS CLAVE =====================
    st.header("5. Preguntas Clave")

    st.subheader("10 Titulos mas recientes")
    recientes = nf.sort_values("AnioAgregado", ascending=False).head(10)
    st.dataframe(recientes[["title","AnioAgregado"]])

    st.subheader("Paises con mas producciones")
    paises = nf["country"].value_counts().head(10)
    st.dataframe(paises)