#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Matthieu Zins
"""

import cv2
import numpy as np
import glob
import os

folder = "seq_01"

l = sorted(glob.glob(os.path.join(folder, "*.png")))

text = []
for i, f in enumerate(l):
    img = cv2.imread(f)
    img = cv2.resize(img, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f, img)
    text.append("%d %s" % (i, os.path.basename(f)))
    
with open(os.path.join(folder, "rgb.txt"), "w") as fout:
    for s in text:
        fout.write(s + "\n")
           


