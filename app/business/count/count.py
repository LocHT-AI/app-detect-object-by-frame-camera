import os
import json
from supervision import Point
from business.count.line import MyLineZone



def points2line( points, direction, safe_area_dist, anchor="center"):
    start = Point(points[0], points[1])
    end = Point(points[2], points[3])
    line_counter = MyLineZone(start=start, 
                                end=end, 
                                anchor=anchor, 
                                direction=direction,
                                safe_area_dist=safe_area_dist)

    return line_counter


def transform_data(data):
    result = []
    for item in data:
        # Convert the set of tuples to a sorted list of tuples to maintain order
        tuples_list = sorted(list(item))
        
        # Extract the individual coordinates
        x1, y1 = tuples_list[0]
        x2, y2 = tuples_list[1]
        
        # Transform to the desired format
        transformed_item = [x1, y1, x2, y2]
        
        # Append the transformed item to the result list
        result.append(transformed_item)
    
    return result
def draw_line(lines_input):
    # # Extract the coordinates from the set
    # point1, point2 = list(lines[0])

    # # Extract x and y values from both points
    # x1, y1 = point1
    # x2, y2 = point2
    lines = transform_data(lines_input)

    # Create the final list of dictionaries
    final_lines = []
    for line in lines:
        line_dict = {
            "points": line,
            "direction": 1,
            "safe_area_dist": 10
        }
        final_lines.append(line_dict)
    json_path=f"a.json"
    prev_result = None
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            prev_result = json.load(f)
    line_zones = list()
    i= 0
    for line in final_lines:
        i += 1
        line_zone = points2line(line["points"], line["direction"], line["safe_area_dist"])
        if prev_result is not None:
            line_zone.in_count = prev_result[line[f"{i}"]]["in_count"]
            line_zone.out_count = prev_result[line[f"{i}"]]["out_count"]
        line_zones.append(line_zone)
    return line_zones

def counter( detection,line_zones):
    # print(detection)
    in_counts = list()
    out_counts = list()
    for i, line_zone in enumerate(line_zones):
        line_zone.trigger(detection)
        in_counts.append(line_zone.in_count)
        out_counts.append(line_zone.out_count)
    return in_counts,out_counts


# check_quit = False
# r = redis.Redis(port=6379)

# def count_object():
#     while True:
#         # print("cc")
#         quit, index_2=get_data("check_quit",r)
#         if quit:
#             global check_quit
#             check_quit = json.loads(quit[b"check_quit"])
#             # print(check_quit)
#             if check_quit:
#                 # print(check_quit)
#                 break
#         data, index = get_data("track", r)
#         if data:
#             byte_frame = data[b"frame"]
#             frame = cv2.imdecode(np.frombuffer(byte_frame, np.uint8), cv2.IMREAD_COLOR)    
#             infor = json.loads(data[b"infor"])
#             object = infor["object"]
#             # print(object)
#             # print(infor)
#             in_count,out_count = counter(object)
#             # print(f"{in_count}  {out_count}")
#             cv2.putText(frame, f"In: {in_count}  Out: {out_count}", (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),2)
#             cv2.line(frame, (0,250), (1920,250), (0,255,0), thickness=2)
#             frame_data = serialize_img(frame)
#             result = {"frame": frame_data}
#             r.xadd("visualize", result, maxlen=2)

# def serialize_img(img):

#     _, img_buffer_arr = cv2.imencode(".jpg", img)
#     img_bytes = img_buffer_arr.tobytes()
#     return img_bytes      
# previous_index = None
# def get_data(key_redis,conn):
#     global previous_index
#     try:
#         p = conn.pipeline()
#         p.xrevrange(key_redis, count=1)
#         msg = p.execute()
#         index = None
#         if msg and len(msg[0]) > 0:
#             index = msg[0][0][0].decode("utf-8")
#         if ((index is None) or 
#             (previous_index is not None and 
#                 previous_index == index)):
#             return None, index
#         previous_index = index
#         data = msg[0][0][1]
#         return data, index
    
#     except Exception as e:
#         print(e)
#         return None, None