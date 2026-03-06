import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sklearn.datasets as skds
import sklearn.preprocessing as skpp
import sklearn.model_selection as skms
import sklearn.cluster as skcl
import sklearn.metrics as skm

st.set_page_config(page_title="K-Means Interactivo", layout="wide")
st.title("Clustering Interactivo con K-Means y Plotly")

# --- CARGA Y PREPARACIÓN DE DATOS ---
@st.cache_data
def cargar_datos():
    iris = skds.load_iris()
    xtrain, xtest, ytrain, ytest = skms.train_test_split(
        iris.data, iris.target, test_size=0.3, random_state=6
    )
    
    scaler = skpp.MinMaxScaler()
    xtrain_df = pd.DataFrame(scaler.fit_transform(xtrain), columns=["SL","SW","PL","PW"])
    xtest_df = pd.DataFrame(scaler.transform(xtest), columns=["SL","SW","PL","PW"])
    
    df_test = xtest_df.copy()
    df_test["Clase_Real"] = ytest.astype(str)
    return xtrain_df, df_test

xtrain, df_test = cargar_datos()

# --- CONTROLES INTERACTIVOS ---
st.sidebar.markdown("### Ajustes del Modelo")
k_elegido = st.sidebar.slider("Número de Puntos aleatorios (K):", min_value=2, max_value=10, value=3)

# --- ENTRENAMIENTO Y PREDICCIÓN ---
modelo = skcl.KMeans(n_clusters=k_elegido, random_state=6)
modelo.fit(xtrain)

df_test["Prediccion"] = modelo.predict(df_test[["SL","SW","PL","PW"]]).astype(str)

# Obtenemos los centroides
centroides_df = pd.DataFrame(modelo.cluster_centers_, columns=["SL","SW","PL","PW"])

# --- SECCIÓN 1: GRÁFICOS DE CLUSTERING Y CENTROIDES ---
st.header("1. Comparación de Clusters")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Clasificación Real")
    fig_real = px.scatter(
        df_test, x="SL", y="PW", color="Clase_Real",
        hover_data=["SW", "PL"],
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_real, use_container_width=True)

with col2:
    st.markdown(f"#### Predicción K-Means (K={k_elegido})")
    fig_pred = px.scatter(
        df_test, x="SL", y="PW", color="Prediccion",
        hover_data=["SW", "PL", "Clase_Real"],
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    # Agregar las marcas de los Centroides al gráfico de predicción
    fig_pred.add_trace(
        go.Scatter(
            x=centroides_df["SL"], 
            y=centroides_df["PW"],
            mode='markers',
            marker=dict(symbol='x', size=12, color='black', line=dict(width=2, color='white')),
            name='Centroides',
            hoverinfo='skip'
        )
    )
    st.plotly_chart(fig_pred, use_container_width=True)


#Los centroides ahora aparecerán marcados con una 'X' sobre los grupos formados, indicando el núcleo de cada cluster.*

# --- SECCIÓN 2: MÉTODO DEL CODO ---
st.header("2. Método del Codo (Elbow Method)")
st.markdown("Analiza la inercia para encontrar el número óptimo de agrupaciones.")

# Calculamos la inercia para diferentes valores de K
inercias = []
rango_k = range(1, 11)
for i in rango_k:
    m_temp = skcl.KMeans(n_clusters=i, random_state=6).fit(xtrain)
    inercias.append(m_temp.inertia_)

df_codo = pd.DataFrame({'K': rango_k, 'Inercia': inercias})

fig_codo = px.line(
    df_codo, x='K', y='Inercia', markers=True,
    title="Curva de Inercia",
    labels={'K': 'Número de Clusters (K)', 'Inercia': 'Suma de distancias al cuadrado'}
)

# Línea vertical para mostrar el K actual elegido por el usuario
fig_codo.add_vline(x=k_elegido, line_dash="dash", line_color="red", annotation_text=f"K Actual: {k_elegido}")

st.plotly_chart(fig_codo, use_container_width=True)
