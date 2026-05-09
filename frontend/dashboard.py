import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(
    page_title="Signal | AI Trend Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Diseño oscuro minimalista con CSS
st.markdown("""
<style>
    /* Ajustes generales del fondo para asegurar estilo oscuro y tech */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Estilos para el Título Principal */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    /* Subtítulo */
    .sub-title {
        font-size: 1.2rem;
        color: #A0AEC0;
        margin-top: -5px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Encabezado
st.markdown('<p class="main-title">⚡ Signal</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-powered trend intelligence platform</p>', unsafe_allow_html=True)

# 4. Botón de Acción
if st.button("Analyze Current Signals", type="primary", use_container_width=True):
    
    # Mostrar Spinner mientras se espera la API
    with st.spinner("Extracting and analyzing signals from the web..."):
        try:
            # Petición a la API local (usamos 127.0.0.1 en lugar de localhost para evitar conflictos con IPv6)
            response = requests.get("http://127.0.0.1:8000/api/summary", timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validación de error interno en el JSON
                if "error" in data and "Error" in data.get("main_topics", [""])[0]:
                    st.error(data.get("summary", "An unknown AI error occurred."))
                else:
                    # Renderizar el 'summary' general
                    st.success(data.get("summary", "No summary provided."))
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Renderizar los 'main_topics'
                    st.subheader("🎯 Core Themes")
                    topics = data.get("main_topics", [])
                    if topics:
                        # Crear dinámicamente el número de columnas necesarias
                        cols = st.columns(len(topics))
                        for i, topic in enumerate(topics):
                            with cols[i]:
                                # Pintar el tópico como un contenedor/métrica
                                st.info(f"**{topic}**")
                    else:
                        st.write("No themes identified.")
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Renderizar las 'top_signals'
                    st.subheader("📡 Top Signals")
                    signals = data.get("top_signals", [])
                    
                    if signals:
                        # Mostrar en un grid de 2 columnas para optimizar espacio
                        sig_cols = st.columns(2)
                        for i, signal in enumerate(signals):
                            col = sig_cols[i % 2]
                            with col:
                                # Tarjeta visual usando st.container
                                with st.container(border=True):
                                    st.markdown(f"#### {signal.get('topic', 'Unknown Topic')}")
                                    
                                    importance = signal.get("importance", "Medium")
                                    # Lógica simple de colores
                                    if importance.lower() == "high":
                                        indicator = "🔴 High"
                                    elif importance.lower() == "medium":
                                        indicator = "🟡 Medium"
                                    else:
                                        indicator = f"🔵 {importance}"
                                        
                                    st.markdown(f"**Importance:** {indicator}")
                                    st.write(signal.get("explanation", "No explanation available."))
                    else:
                        st.write("No top signals detected.")
            else:
                st.error(f"API Error: Server returned status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: The backend API is not responding. Please make sure FastAPI is running on http://127.0.0.1:8000.")
        except requests.exceptions.Timeout:
            st.error("Request Timeout: The analysis took too long. Please try again.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
