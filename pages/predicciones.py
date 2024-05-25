import streamlit as st
from home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time
import os
from twilio.rest import Client
from dotenv import load_dotenv
st.set_page_config(page_title='Asistencia', layout='wide')
st.subheader('Asistencia')

load_dotenv()  # Cargar variables desde el archivo .env

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

token = client.tokens.create()

with st.spinner('Extrayendo información de Redis'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success('cargado correctamente')
st.success('base de datos conectado')

waitTime = 30 # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred() # real time prediction class

def video_frame_callback(frame):
    global setTime

    img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'facial',['name','Role'],thresh=0.5)

    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time
        print('Save Data to redis database')


    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)