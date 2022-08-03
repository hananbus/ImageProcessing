"""
Functions to use as distance functions in the video maker are declared here
"""

import numpy as np

import cv2


def euclidean(f1, f2):
    return np.linalg.norm(f1 - f2)


def motion_vector(f1, f2):
    f1_colored = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    f2_colored = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(f1_colored, f2_colored, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    return np.linalg.norm(flow)