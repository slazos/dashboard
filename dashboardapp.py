import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

archivo = 'c:/Users/rdepi/OneDrive/Imágenes/Documentos/programas/actividad.csv'

# Cargar un subconjunto de filas del archivo Excel en un DataFrame
df = pd.read_csv(archivo)

st.set_page_config(
    page_title='Police Department Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)

st.sidebar.header('Please Filter Here:')
incident_year = st.sidebar.multiselect(
    'Select the Incident Year:',
    options=df['Incident Year'].unique(),
    default=df['Incident Year'].unique()
)

Resolution = st.sidebar.multiselect(
    'Select the Resolution:',
    options=df['Resolution'].unique(),
    default=df['Resolution'].unique()
)

police_district = st.sidebar.multiselect(
    'Select the Police District:',
    options=df['Police District'].unique(),
    default=df['Police District'].unique()
)

df_selection = df.query(
    '`Incident Year` == @incident_year & Resolution == @Resolution & `Police District` == @police_district'
)

# Filtrar el DataFrame según las selecciones del usuario
filtered_df = df[
    df['Incident Year'].isin(incident_year) &
    df['Resolution'].isin(Resolution) &
    df['Police District'].isin(police_district)
]

# Mostrar el DataFrame filtrado
st.dataframe(filtered_df)

st.title(":bar_chart: Incidents Dashboard")
st.markdown("##")


total_incident = df.groupby("Incident Year").size().reset_index(name="Total Incidents")

fig_total_incident = px.bar(total_incident, x="Incident Year", y="Total Incidents",
                            orientation="v", title="<b>Total incidents per year</b>",
                            color_discrete_sequence=["#0083B8"],
                            template="plotly_white")


st.plotly_chart(fig_total_incident)

total_incidents_supervisor = df.groupby("Supervisor District").size().reset_index(name="Total Incidents")

fig_total_incidents_supervisor = px.bar(total_incidents_supervisor, x="Supervisor District", y="Total Incidents",
                                        orientation="v", title="<b>Total incidents by Supervisor District</b>",
                                        color_discrete_sequence=["#0083B8"],
                                        template="plotly_white")

st.plotly_chart(fig_total_incidents_supervisor)

fig_total_incidents_supervisor.update_layout(xaxis=dict(tickmode="linear"),
                                             plot_bgcolor="rgba(0,0,0,0)",
                                             yaxis=dict(showgrid=False))



fig = px.scatter_mapbox(df,
                        lon=df["Longitude"],
                        lat=df["Latitude"],
                        zoom=3,
                        color_discrete_sequence=["#0083B8"],
                        width=1200,
                        height=900,
                        title='Incidents Scatter Map')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 10})

st.plotly_chart(fig)
