import streamlit as st

st.set_page_config(page_title='Sistema de asistencia', layout='wide')
st.header('Sistema de asistencia')


with st.spinner("cargando modelos y conectando a redis"):
    import face_rec

st.success('modelos cargados')
st.success('redis conectado')


    