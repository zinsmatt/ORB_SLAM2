#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Matthieu Zins
"""

import numpy as np
import cv2
from scipy.spatial.transform.rotation import Rotation as Rot
import glob
import os

points_file = "/home/matt/dev/ORB_SLAM2/Examples/Monocular/MapPointsSave.txt"

pts = []
with open(points_file, "r") as fin:
    lines = fin.readlines()
for l in lines:
    pts.append(list(map(float, l.split())))
pts = np.vstack(pts)


trajectory_file = "/home/matt/dev/ORB_SLAM2/Examples/Monocular/KeyFrameTrajectory.txt"

rotations = []
positions = []
indices = []
with open(trajectory_file, "r") as fin:
    lines = fin.readlines()
for l in lines:
    data = list(map(float, l.split()))
    indices.append(int(data[0]))
    positions.append(data[1:4])
    rotations.append(Rot.from_quat(data[4:]).as_matrix())
    
    
    
folder = "/home/matt/dev/ORB_SLAM2/data/seq_01/"
images = sorted(glob.glob(os.path.join(folder, "*.png")))
                
K = np.array([[517.306408, 0.0, 320.0],
              [0.0, 516.469215, 180.0],
              [0.0, 0.0, 1.0]])
W, H = 640, 360

for idx, p, rot in zip(indices, positions, rotations):
    print(idx)
    img = cv2.imread(images[idx])
    
    R = rot.T
    t = -rot.T @ p
    
    uvs = K @ (R @ pts.T + t.reshape((-1, 1)))
    uvs /= uvs[2, :]
    uvs = np.round(uvs).astype(int).T
    for p in uvs[:, :2]:
        if p[0] >= 0 and p[0] < W and p[1] >= 0 and p[1] < H:
            img[p[1], p[0], :] = (0, 255, 0)
    cv2.imshow("fen", img)
    cv2.waitKey(-1)