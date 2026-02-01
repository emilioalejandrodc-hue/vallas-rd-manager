import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Configuración de página
st.set_page_config(page_title="Vallas RD - Gerencia", layout="wide")

ARCHIVO_DB = "base_datos_vallas.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DB):
        return pd.DataFrame(columns=["Nombre", "Latitud", "Longitud", "Precio", "Tamano", "Estado", "Foto"])
    return pd.read_csv(ARCHIVO_DB)

# Título
st.title("📊 Tablero de Control - Vallas Publicitarias")

# Cargar datos
df = cargar_datos()

# Métricas (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Total Vallas", len(df))
col2.metric("Disponibles", len(df[df['Estado'] == 'Disponible']), delta_color="normal")
col3.metric("Ocupadas", len(df[df['Estado'] == 'Ocupada']), delta_color="inverse")

# Mapa
st.subheader("📍 Mapa en Tiempo Real")
m = folium.Map(location=[18.7357, -70.1627], zoom_start=8)

if not df.empty:
    for _, row in df.iterrows():
        color = 'green' if row['Estado'] == 'Disponible' else 'red' if row['Estado'] == 'Ocupada' else 'orange'
        icon = 'check' if row['Estado'] == 'Disponible' else 'ban' if row['Estado'] == 'Ocupada' else 'wrench'
        
        html = f"""
        <b>{row['Nombre']}</b><br>
        <span style="color:{color}">{row['Estado']}</span><br>
        Precio: RD$ {row['Precio']}<br>
        Size: {row['Tamano']}
        """
        if pd.notna(row['Foto']) and "http" in str(row['Foto']):
            html += f"<br><a href='{row['Foto']}' target='_blank'>Ver Foto</a>"
            
        folium.Marker(
            [row['Latitud'], row['Longitud']],
            popup=folium.Popup(html, max_width=200),
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)

st_folium(m, width="100%", height=500)

# Tabla de Datos (Solo lectura o edición ligera)
st.subheader("📋 Listado Detallado")
st.dataframe(df, use_container_width=True)