import math
from typing import Dict

import cv2
import numpy as np
from supervision.geometry.core import Point, Vector


def calculate_angle_between_lines(B, A, C):
    """ Degree of angle BAC """

    vector_AB = (B.x - A.x, B.y - A.y)
    vector_AC = (C.x - A.x, C.y - A.y)
    dot_product = vector_AB[0] * vector_AC[0] + vector_AB[1] * vector_AC[1]
    magnitude_AB = math.sqrt(vector_AB[0]**2 + vector_AB[1]**2)
    magnitude_AC = math.sqrt(vector_AC[0]**2 + vector_AC[1]**2)
    cosine_theta = dot_product / (magnitude_AB * magnitude_AC)
    theta_radians = math.acos(cosine_theta)
    theta_degrees = math.degrees(theta_radians)

    return theta_degrees


def find_perp_point(A, B, dist, at_first=True):
    AB_vector = np.array([B[0] - A[0], B[1] - A[1]])
    AB_perp = np.array([1, -AB_vector[0]/(AB_vector[1] + 0.0001)])
    AB_perp = AB_perp / (np.linalg.norm(AB_perp) + + 0.0001)

    # Calculate the coordinates of point C
    if at_first:
        first_point = np.array(A)
    else:
        first_point = np.array(B)

    C = first_point + dist * AB_perp

    return C.astype(int)

def get_safe_area(A, B, dist):
    safe_area = list()
    directs = [-1, 1, 1, -1]
    for i in range(4):
        perp_point = find_perp_point(A, B, directs[i] * dist, at_first=(i>1))
        safe_area.append(perp_point)
    return safe_area

def calculate_AB2C_dist(A, B, C):
    if np.linalg.norm(A - B) == 0:
        return np.linalg.norm(C - B)

    return np.abs(np.cross(A - B, C - A) / np.linalg.norm(A - B))

def convert_Point2Array(p):
    return np.array([p.x, p.y])

def convert_Array2Point(a):
    return Point(a[0], a[1])

def convert_points(point_1, point_2):
    if ((point_1[0] < point_2[0]) or
        (point_1[0] == point_2[0] and point_1[1] < point_2[1])):
        left_point = point_1
        right_point = point_2
    else:
        left_point = point_2
        right_point = point_1

    return left_point, right_point


class MyLineZone:
    """
    Count the number of objects that cross a line.
    """

    def __init__(self, start, end, direction=1, anchor="center", safe_area_dist=100):
        """
        Initialize a LineCounter object.

        Attributes:
            start (Point): The starting point of the line.
            end (Point): The ending point of the line.

        """
        start_np, end_np = convert_Point2Array(start), convert_Point2Array(end)
        left, right = convert_points(start_np, end_np)

        if ((direction == 2) or 
            (direction == 3 and left[1] <= right[1]) or
            (direction == 4 and left[1] > right[1])):
            left, right = right, left

        self.left_point = convert_Array2Point(left)
        self.right_point = convert_Array2Point(right)

        self.vector = Vector(start=self.left_point, end=self.right_point)
        self.tracker_state: Dict[str, bool] = {}
        self.out_count = 0
        self.in_count = 0
        self.anchor = anchor
        self.safe_area_dist = safe_area_dist

        start = convert_Point2Array(self.left_point)
        end = convert_Point2Array(self.right_point)
        self.safe_area = get_safe_area(start, end, self.safe_area_dist)

        self.tracked_indices = list()
        self.safe_area_first_appear = dict()
        self.total_frames_from_first_appear = 5


    def is_in_safe_area(self, point):
        distance = cv2.pointPolygonTest(np.array(self.safe_area), (point.x, point.y), measureDist=True)
        return distance >= 0

    def get_dist_from_line(self, point):
        A = convert_Point2Array(self.left_point)
        B = convert_Point2Array(self.right_point)
        C = convert_Point2Array(point)

        return calculate_AB2C_dist(A, B, C)

    def trigger(self, detections):
        """
        Update the in_count and out_count for the detections that cross the line.

        Attributes:
            detections (Detections): The detections for which to update the counts.
        """
        for i in detections:
            xyxy=i["bbox"]
            # print(xyxy)
            tracker_id=i["tracking_id"]
            # handle detections with no tracker_id
            if tracker_id is None:
                continue

            x1, y1, x2, y2 = xyxy

            if self.anchor == "center":
                target = Point(int((x2 + x1)/2), y2)
            elif self.anchor == "right":
                target = Point(x2, y2)
            else:
                target = Point(x1, y2)

            tracker_state = self.vector.is_in(point=target)

            # handle new detection
            if tracker_id not in self.tracker_state:
                self.tracker_state[tracker_id] = tracker_state
                if self.is_in_safe_area(target):
                    self.safe_area_first_appear[tracker_id] = {"state": tracker_state,
                                                               "dist": self.get_dist_from_line(target),
                                                               "count": 0}
                continue

            # remove id if out of safe zone
            if (not self.is_in_safe_area(target) and
                tracker_id in self.tracked_indices):
                self.tracked_indices.remove(tracker_id)

            # handle first appearance of object is near the safe zone
            if (tracker_id in self.safe_area_first_appear):
                if (tracker_state != self.safe_area_first_appear[tracker_id]["state"]):
                    self.safe_area_first_appear.pop(tracker_id)
                else:
                    self.safe_area_first_appear[tracker_id]["count"] += 1
                    if (self.safe_area_first_appear[tracker_id]["count"] == self.total_frames_from_first_appear):
                        current_dist = self.get_dist_from_line(target)
                        if (current_dist > self.safe_area_first_appear[tracker_id]["dist"]):
                            self.tracked_indices.append(tracker_id)
                            if tracker_state:
                                self.out_count += 1
                            else:
                                self.in_count += 1
                            self.safe_area_first_appear.pop(tracker_id)

                            continue

            # handle detection on the same side of the line
            if self.tracker_state.get(tracker_id) == tracker_state:
                continue

            self.tracker_state[tracker_id] = tracker_state


            if (calculate_angle_between_lines(target, self.left_point, self.right_point) <= 90 and
                calculate_angle_between_lines(target, self.right_point, self.left_point) <= 90):

                if tracker_id not in self.tracked_indices:
                    self.tracked_indices.append(tracker_id)
                    if tracker_state:
                        self.out_count += 1
                    else:
                        self.in_count += 1
                else:
                    if self.is_in_safe_area(target):
                        if tracker_state:
                            self.in_count -= 1
                        else:
                            self.out_count -= 1
                        self.tracked_indices.remove(tracker_id)
