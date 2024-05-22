import streamlit as st
from home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

registration_form = face_rec.RegistrationForm()

st.set_page_config(page_title='registros')
st.subheader('registros')


person_name = st.text_input(label='Nombre',placeholder='Tu nombre completo')
number = st.text_input(label='Telefono',placeholder='Tu numero telefonico')
number = st.date_input(label='Fecha de nacimiento',format="DD/MM/YYYY",min_value=None,max_value=None,help="dd/mm/yy")
role = st.selectbox(label='Departamento',options=('Instrumentación',
                                                  'Biotecnologia',
                                                  'Sistemas',
                                                  'Biologia',
                                                  'Laboratorios'
                                                      ))

# step-2: Collect facial embedding of that person
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24') # 3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    # two step process
    # 1st step save data into local computer txt
    if embedding is not None:
        with open('face_embedding.txt',mode='ab') as f:
            np.savetxt(f,embedding)
    
    return av.VideoFrame.from_ndarray(reg_img,format='bgr24')

webrtc_streamer(key='registration',video_frame_callback=video_callback_func,
                 rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name,role)
    if return_val == True:
        st.success(f"{person_name} registered sucessfully")
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
        
    elif return_val == 'file_false':
        st.error('face_embedding.txt is not found. Please refresh the page and execute again.')