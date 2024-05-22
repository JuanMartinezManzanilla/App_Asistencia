from home import st
from home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time
st.set_page_config(page_title='Asistencia', layout='wide')
st.subheader('Asistencia')


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
    img = frame.to_ndarray(format="bgr24")
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'face',['name','Role'],thresh=0.5)
    
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time        
        print('Save Data to redis database')

    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(key="realtime", video_frame_callback=video_frame_callback,
                 rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })