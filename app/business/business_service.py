import os
import json
import numpy as np
import redis
import cv2
from business.count.count import counter
from business.face_id.face_id import recognize_faces , initialize_face_recognition
from business.face_id.add_face import add_with_camera , add_with_data




check_quit = False
r = redis.Redis(port=6379)

def business(check_count,check_id):
    knn, infor = initialize_face_recognition()
    facedetect = cv2.CascadeClassifier('business/face_id/data/haarcascade_frontalface_default.xml')
    COL_NAMES = ['NAME', 'TIME']
    while True:
        # print("cc")
        quit, index_2=get_data("check_quit",r)
        if quit:
            global check_quit
            check_quit = json.loads(quit[b"check_quit"])
            # print(check_quit)
            if check_quit:
                # print(check_quit)
                break
        data, index = get_data("track", r)
        if data:
            byte_frame = data[b"frame"]
            frame = cv2.imdecode(np.frombuffer(byte_frame, np.uint8), cv2.IMREAD_COLOR)    
            infor = json.loads(data[b"infor"])
            object = infor["object"]
            lines = []
            # print(f"{check_count}  {check_id}")
            if check_count :
                in_count,out_count = counter(object,lines)
                cv2.putText(frame, f"In: {in_count}  Out: {out_count}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),1)
                cv2.line(frame, (0,250), (1080,250), (0,255,0), thickness=2)
            if check_id:
                attendance,frame = recognize_faces(frame, facedetect, knn, infor)
            frame_data = serialize_img(frame)
            result = {"frame": frame_data}
            r.xadd("visualize", result, maxlen=2)

def serialize_img(img):
    _, img_buffer_arr = cv2.imencode(".jpg", img)
    img_bytes = img_buffer_arr.tobytes()
    return img_bytes      
previous_index = None
def get_data(key_redis,conn):
    global previous_index
    try:
        p = conn.pipeline()
        p.xrevrange(key_redis, count=1)
        msg = p.execute()
        index = None
        if msg and len(msg[0]) > 0:
            index = msg[0][0][0].decode("utf-8")
        if ((index is None) or 
            (previous_index is not None and 
                previous_index == index)):
            return None, index
        previous_index = index
        data = msg[0][0][1]
        return data, index
    
    except Exception as e:
        print(e)
        return None, None