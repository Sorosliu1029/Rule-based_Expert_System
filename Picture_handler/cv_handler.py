#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""

"""
from cv2.cv import *
close_threshold = 100
inf_number = 100000
def calculate_gradient(line):
    global grad, inf_number
    try:
        grad[line] = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
    except ZeroDivisionError:
        grad[line] = inf_number

def close_enough(dot1, dot2):
    global close_threshold
    return ((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2) < close_threshold

def mergable_lines(line1, line2):
    global grad
    if (close_enough(line1[0], line2[0]) and close_enough(line1[1], line2[1])):
        print(abs(grad.get(line1) - grad.get(line2)))
    return ((abs(grad.get(line1) - grad.get(line2)) < 5) and
            (close_enough(line1[0], line2[0]) and close_enough(line1[1], line2[1])))

def average_dot(line1, line2):
    return ((line1[0][0] + line2[0][0]) / 2, (line1[0][1] + line2[0][1]) / 2), \
            ((line1[1][0] + line2[1][0]) / 2, (line1[1][1] + line2[1][1]) / 2)

src = LoadImage('../test/test0.png', 0)
dst = None
color_dst = None
storage = CreateMemStorage(0)

dst = CreateImage(GetSize(src), 8, 1)
color_dst = CreateImage(GetSize(src), 8, 3)

Canny(src, dst, 10, 50, 3)
# CvtColor(dst, color_dst, CV_GRAY2BGR)
cv_lines = HoughLines2(dst, storage, CV_HOUGH_PROBABILISTIC, 1, CV_PI/180, 50, 50, 10)
grad = {}
map(calculate_gradient, cv_lines)
cv_line_numbers = len(cv_lines)
merged_lines = []
for i in range(cv_line_numbers):
    for j in range(i+1, cv_line_numbers):
        if mergable_lines(cv_lines[i], cv_lines[j]):
            merged_lines.append(average_dot(cv_lines[i], cv_lines[j]))

# for line in cv_lines:
#     print(line)
# print('----------------\n')
# for line in merged_lines:
#     print(line)
# print('----------------\n')
# for key, value in grad.items():
#     print(value)

for line in merged_lines:
    Line(color_dst, line[0], line[1], CV_RGB(255, 0, 0), 1, CV_AA, 0)

# Line(color_dst, lines[0][0], lines[0][1], CV_RGB(255, 0, 0), 1, CV_AA, 0)
NamedWindow('src', 1)
ShowImage('src', src)

NamedWindow('dst', 1)
ShowImage('dst', dst)

NamedWindow('hough', 1)
ShowImage('hough', color_dst)

WaitKey(0)
