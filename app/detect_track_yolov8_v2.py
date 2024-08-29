import time
import cv2
from ultralytics import YOLO
from supervision.draw.color import  ColorPalette
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np
import torch

# Load the YOLO model
path = "assets/model/model.pt"
model_p = YOLO(path)
model_p.fuse()
startTime=0
# Function to read class names from file
def read_class_names(file_path):
    with open(file_path, 'r') as file:
        class_names = file.read().strip().split('\n')
    return class_names
class_names = read_class_names('assets/model/class.txt')  # replace with the actual path to your class.txt

def tracking_person(frame,chk_track,classes,polygon):
    global startTime
    if chk_track:    
        results = model_p.track(frame, conf=0.5, 
                                iou=0.25,
                                tracker="assets/model/custom_bytetrack.yaml",
                                verbose=False,
                                persist=True,
                                stream_buffer=True,
                                device=0 if torch.cuda.is_available() else 'cpu')
        
        currentTime = time.time()
        fps = 1 / (currentTime - startTime)
        startTime = currentTime
        if results[0].boxes is None or results[0].boxes.id is None:
            return [], fps
        objects = []
        for index in range(len(results[0].boxes.data)):
            cls = int(results[0].boxes.cls[index])
            if cls in classes:
                bbox = results[0].boxes.data[index]
                bbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
                tracking_id = str(int(results[0].boxes.id[index]))
                confidence_2 = float(results[0].boxes.conf[index].cpu().numpy())
                confidence = f"{confidence_2:.2f}"
                cls = str(cls)
                location = ((bbox[0] + bbox[2]) / 2, bbox[3])
                rule=False
                for boud in polygon:
                    if Polygon(boud).contains(Point(location)):
                        rule = True
                        # print(rule)
                        break
                    else: 
                        rule = False
                object = {
                    "bbox": bbox,
                    "confidence": confidence,
                    "class_id": cls,
                    "tracking_id": tracking_id,
                    "is_in_bound": rule
                }
                objects.append(object)
            else:
                return [], fps
    else:
        # Run batched inference on a list of images
        results = model_p(frame,conf=0.7)  # return a list of Results objects
        currentTime = time.time()
        fps = 1 / (currentTime - startTime)
        startTime = currentTime
        # Filter results
        filtered_results = []


        for result in results:
            for box in result.boxes:
                if int(box.cls) in classes:
                    filtered_results.append(box)
        
        return filtered_results,fps
    return objects, fps

def visualize(frame, objects,chk_track,chk_nolabel,chk_nobox,warning_obj):
    color = ColorPalette.default()
    thickness = 2 
    if chk_track:
        for obj in objects:
 
            if warning_obj:
                if obj["is_in_bound"]:
                    x1, y1, x2, y2 = obj["bbox"]
                    class_id = obj["class_id"] if obj["class_id"] is not None else None
                    idx = int(class_id) if class_id is not None else 0
                    track_id = obj["tracking_id"]
                    class_name = class_names[int(class_id)]
                    text=f"ID: {track_id} {class_name}"
                    # color=(0, 0, 255)
                    if not chk_nobox:
                        cv2.rectangle(
                            img=frame,
                            pt1=(x1, y1),
                            pt2=(x2, y2),
                            color=(0, 0, 255),
                            thickness=thickness,
                        )
                        cv2.circle(
                            frame,
                            (int((x2 + x1) / 2), y2),
                            radius=5,
                            color=(0, 255, 0),
                            thickness=-1,
                            lineType=cv2.LINE_AA,
                        )
                    if not chk_nolabel:
                        cv2.putText(
                            img=frame,
                            text=text,
                            org=(x1, y1 - 10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5,
                            color=(0, 0, 255),
                            thickness=2,
                        )
                    continue
  
            x1, y1, x2, y2 = obj["bbox"]
            class_id = obj["class_id"] if obj["class_id"] is not None else None
            idx = int(class_id) if class_id is not None else 0
            track_id = obj["tracking_id"]
            class_name = class_names[int(class_id)]
            text=f"ID: {track_id} {class_name}"
            color = (
                color.by_idx(idx)
                if isinstance(color, ColorPalette)
                else color
            )
            if not chk_nobox:
                cv2.rectangle(
                    img=frame,
                    pt1=(x1, y1),
                    pt2=(x2, y2),
                    color=color.as_bgr(),
                    thickness=thickness,
                )
                cv2.circle(
                    frame,
                    (int((x2 + x1) / 2), y2),
                    radius=5,
                    color=(0, 255, 0),
                    thickness=-1,
                    lineType=cv2.LINE_AA,
                )
            if not chk_nolabel:
                cv2.putText(
                    img=frame,
                    text=text,
                    org=(x1, y1 - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=color.as_bgr(),
                    thickness=2,
                )

        
        # cv2.imshow("frame", frame)
    else:
        # Draw filtered results on the frame
        for box in objects:
            class_name = class_names[int(box.cls)]
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert bounding box coordinates to integers
            if not chk_nobox:
                rect = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            if not chk_nolabel:
                cv2.putText(frame, f' {class_name} Conf: {box.conf[0]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    return frame

def capture_video():
    file_path= "rtsp://admin:SNXLBC@192.168.101.102:554/H.264"
    return cv2.VideoCapture(file_path)

def main():
    video = capture_video()
    ret, frame = video.read()
    # # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter('tao.mp4', fourcc, 20.0, (640, 480))  # Adjust frame size and FPS as needed
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # cap = cv2.VideoCapture(source)
    output_writers = cv2.VideoWriter(
        f'save/tao.mp4', fourcc, 5, (frame.shape[1], frame.shape[0])) 
    boud=[[(700, 850), (1900, 850), (1900, 1900), (850, 1900)],[(100, 100), (300, 100), (300, 300), (100, 300)]]

    while True:
        ret, frame = video.read()

        if not ret:
            video.release()
            video = capture_video()
            continue
        # frame=frame[::3,::3]
        objects, fps = tracking_person(frame,True,[0],boud)
        frame = visualize(frame, objects, True,False,False,True)
        # Convert list of points to numpy arrays and draw contours
        for contour in boud:
            contour_array = np.array(contour, dtype=np.int32)
            cv2.polylines(frame, [contour_array], isClosed=True, color=(0, 255, 0), thickness=5)
       
        output_writers.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # video.release()
    output_writers.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
