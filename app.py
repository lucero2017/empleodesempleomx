import streamlit as st
import pandas as pd
import plotly.express as px
from funciones import cargar_datos, predecir_ingreso_tipo

# --- Configuración general ---
st.set_page_config(page_title="Empleo y Desempleo EDOMEX", layout="wide")

# --- Fondo vino degradado y estilo formal ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #5e0b15, #800020);
}
.header {
    background-color: rgba(128, 0, 32, 0.9);
    border-radius: 15px;
    padding: 20px;
    color: #ffd700;
    text-align: center;
    border: 3px solid #ffd700;
    margin-bottom: 20px;
    font-weight: bold;
    font-size: 2.3em;
}
.section-title {
    color: #ffd700;
    font-weight: 700;
    margin-bottom: 15px;
    border-bottom: 2px solid #ffd700;
    padding-bottom: 5px;
}
.info-text {
    font-size: 1rem;
    margin-bottom: 20px;
    color: #000;
}
.footer {
    text-align: center;
    font-size: 0.85rem;
    color: #e8d7b4;
    margin-top: 40px;
}
div.stButton > button {
    background-color: #800020;
    color: #ffd700;
    border: 2px solid #ffd700;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #ffd700;
    color: #800020;
}
.stDataFrame, .stTable {
    background-color: rgba(253, 247, 228, 0.07);
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("""
<div class="header">
    🇲🇽 Empleo y Desempleo en el Estado de México
</div>
""", unsafe_allow_html=True)

# --- Cargar datos inicial ---
@st.cache_data
def cargar_datos_cache(ruta):
    return cargar_datos(ruta)

df_original = cargar_datos_cache("data/empleodesempleo.csv")

if 'df' not in st.session_state:
    st.session_state.df = df_original.copy()

# --- Subir CSV para actualización ---
st.sidebar.markdown("### 📁 Subir nuevo CSV")
archivo = st.sidebar.file_uploader("Sube aquí tu archivo CSV", type=["csv"])
if archivo:
    try:
        nuevo_df = pd.read_csv(archivo)
        if set(nuevo_df.columns) == set(st.session_state.df.columns):
            combinado = pd.concat([st.session_state.df, nuevo_df]).drop_duplicates().reset_index(drop=True)
            st.session_state.df = combinado
            st.sidebar.success("Datos actualizados correctamente.")
        else:
            st.sidebar.error("El archivo no tiene las columnas correctas.")
    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

# --- Generar lista de páginas por año dinámicas ---
años_disponibles = sorted(st.session_state.df["Año"].dropna().unique().astype(int))
paginas_dinamicas = [str(a) for a in años_disponibles]

paginas = ["Inicio"] + paginas_dinamicas + ["Gráficas Interactivas", "Predicción de Ingreso", "Descargas"]
pagina = st.sidebar.selectbox("Navegación", paginas)

# --- Página de Inicio ---
if pagina == "Inicio":
    st.markdown('<h2 class="section-title">Introducción General</h2>', unsafe_allow_html=True)
    st.image("empleo.jpg", use_container_width=True, caption="Situación de empleo y desempleo en EDOMEX")
    intro_texto = """
    <div class='info-text'>
    El Estado de México, una de las entidades federativas más importantes y pobladas del país, 
    presenta una dinámica laboral compleja y en constante evolución. La situación de empleo y desempleo
    refleja múltiples factores económicos, sociales y demográficos que impactan directamente en la calidad
    de vida de sus habitantes.<br><br>
    En los últimos años, la región ha enfrentado desafíos significativos como la crisis sanitaria global de 2020,
    que provocó una drástica caída en las oportunidades laborales y un aumento notable en las tasas de desempleo.
    Sin embargo, a partir de 2021, se observaron signos de recuperación progresiva, con la reapertura de sectores
    clave y la adaptación de nuevas modalidades de trabajo, incluyendo el teletrabajo y empleos informales.<br><br>
    Este análisis abarca desde el año 2020 hasta 2025, brindando una visión clara de las tendencias en el mercado laboral,
    los cambios en los ingresos promedio, los tipos de empleo predominantes, así como la distribución por sexo, edad y nivel educativo.<br><br>
    A través de este panel interactivo, los usuarios pueden explorar datos específicos por año, visualizar gráficas interactivas,
    y realizar predicciones personalizadas basadas en características individuales para conocer posibles ingresos y tipo de empleo.<br><br>
    La comprensión de estos datos es fundamental para tomar decisiones informadas en políticas públicas,
    iniciativas privadas y proyectos sociales orientados a mejorar las condiciones laborales en el Estado de México.
    </div>
    """
    st.markdown(intro_texto, unsafe_allow_html=True)



    st.dataframe(st.session_state.df)

# --- Páginas dinámicas por año con introducción ---
elif pagina in paginas_dinamicas:
    año = int(pagina)
    st.markdown(f'<h2 class="section-title">Análisis del Año {año}</h2>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-text">
    Durante {año}, el mercado laboral en el Estado de México reflejó cambios en sectores económicos, ingresos por género y fluctuaciones en posiciones de empleo debido a la recuperación post-pandemia y a los movimientos en la economía local.
    Explora a continuación el comportamiento en ingresos, sectores y distribución por género de este año.
    </div>
    """, unsafe_allow_html=True)

    df_año = st.session_state.df[st.session_state.df['Año'] == año]
    st.dataframe(df_año)

    fig1 = px.histogram(df_año, x="Sexo", color="Sexo",
                        title=f"Distribución por Sexo en {año}",
                        color_discrete_sequence=["#ffd700", "#800020"])
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.box(df_año, x="Sexo", y="Nivel_Ingresos", color="Sexo",
                  title=f"Ingreso Promedio por Sexo en {año}",
                  color_discrete_sequence=["#ffd700", "#800020"])
    st.plotly_chart(fig2, use_container_width=True)

    df_sector = df_año['Sector_Económico'].value_counts().reset_index()
    df_sector.columns = ['Sector_Económico', 'Cantidad']
    fig3 = px.bar(df_sector, x='Sector_Económico', y='Cantidad',
                  title=f"Sectores Económicos en {año}",
                  color_discrete_sequence=["#ffd700"])
    st.plotly_chart(fig3, use_container_width=True)

# --- Gráficas Interactivas ---
elif pagina == "Gráficas Interactivas":
    st.markdown('<h2 class="section-title">Gráficas Interactivas</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-text">
    Genera gráficas personalizadas seleccionando variables de interés para visualizar tendencias laborales de forma clara en el Estado de México.
    </div>
    """, unsafe_allow_html=True)
    columnas_x = ["Año", "Mes_Alto_Desempleo", "Sexo", "Posición_Ocupación",
                  "Sector_Económico", "Jornada", "Nivel_Estudios", "Profesión", "Tipo_Empleo"]
    columnas_y = ["Total_Población", "Edad", "Nivel_Ingresos"]

    col_x = st.selectbox("Eje X", columnas_x)
    col_y = st.selectbox("Eje Y (opcional)", ["None"] + columnas_y)
    tipo = st.selectbox("Tipo de gráfica", ["Histograma", "Barras", "Dispersión", "Pastel"])

    if st.button("Generar Gráfica"):
        if tipo == "Histograma":
            fig = px.histogram(st.session_state.df, x=col_x, color_discrete_sequence=["#ffd700"])
        elif tipo == "Barras" and col_y != "None":
            fig = px.bar(st.session_state.df, x=col_x, y=col_y, color_discrete_sequence=["#ffd700"])
        elif tipo == "Dispersión" and col_y != "None":
            fig = px.scatter(st.session_state.df, x=col_x, y=col_y, color_discrete_sequence=["#ffd700"])
        elif tipo == "Pastel":
            fig = px.pie(st.session_state.df, names=col_x, color_discrete_sequence=["#ffd700"])
        else:
            st.warning("Selecciona variables válidas.")
            fig = None
        if fig:
            fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)

# --- Predicción de Ingreso ---
elif pagina == "Predicción de Ingreso":
    st.markdown('<h2 class="section-title">Predicción de Ingreso</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-text">
    Ingresa tu edad, sexo, nivel de estudios, horas deseadas de trabajo y tipo de trabajo para predecir tu ingreso estimado mensual y tipo de empleo probable con base en datos reales del Estado de México.
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_prediccion"):
        edad = st.slider("Edad", 18, 70, 25)
        sexo = st.selectbox("Sexo", st.session_state.df["Sexo"].unique())
        nivel_estudios = st.selectbox("Nivel de Estudios", st.session_state.df["Nivel_Estudios"].dropna().unique())
        horas = st.slider("Horas que te gustaría trabajar por semana", 1, 80, 40)
        tipo_trabajo = st.selectbox("Tipo de trabajo", ["Formal", "Informal"])
        enviar = st.form_submit_button("Predecir")

    if enviar:
        ingreso, tipo = predecir_ingreso_tipo(
            st.session_state.df, edad, sexo, nivel_estudios, horas, tipo_trabajo
        )
        st.success(f"**Ingreso estimado:** ${ingreso:,.2f} MXN")
        st.info(f"**Tipo de empleo probable:** {tipo}")

# --- Descargas ---
elif pagina == "Descargas":
    st.markdown('<h2 class="section-title">Descargar Base de Datos</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-text">
    Descarga la base de datos actualizada con los datos de empleo y desempleo en el Estado de México para uso personal y análisis offline.
    </div>
    """, unsafe_allow_html=True)

    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar CSV", csv, "empleodesempleo_actualizado.csv", "text/csv")

# --- Footer ---
st.markdown('<div class="footer">© 2025 Empleo y Desempleo EDOMEX</div>', unsafe_allow_html=True)
