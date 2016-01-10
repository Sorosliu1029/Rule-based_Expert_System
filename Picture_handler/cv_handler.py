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
import math
__author__ = 'Soros Liu'


def show_image(image, title='New Image'):
    NamedWindow(title, 1)
    ShowImage(title, image)


def calculate_line_length(line):
    return ((line[0][0] - line[1][0]) ** 2 + (line[0][1] - line[1][1]) ** 2) ** 0.5


def calculate_line_angle(line):
    try:
        k = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
    except ZeroDivisionError:
        k = 100000
    finally:
        return math.degrees(math.atan(k))

class PreHandler():
    """

    """
    __close_threshold = 800
    __parallel_threshold = 20

    def __init__(self, source):
        self.grad = {}
        self.basic_facts = {}
        self.merged_lines = []
        self.src = LoadImage(source, 0)
        self.dst = CreateImage(GetSize(self.src), 8, 1)
        self.rst = CreateImage(GetSize(self.src), 8, 3)
        Canny(self.src, self.dst, 10, 50, 3)
        self.cv_lines = HoughLines2(self.dst, CreateMemStorage(0),
                                    CV_HOUGH_PROBABILISTIC, 1, CV_PI/180, 50, 50, 10)
        map(self.calculate_gradient, self.cv_lines)
        self.cv_line_num = len(self.cv_lines)
        self.merge_lines()
        self.calculate_basic_facts()
        # for fact in self.basic_facts.items():
        #     print(fact)
        # self.draw_lines()
        # show_image(self.src, 'src')
        # show_image(self.rst, 'rst')
        # WaitKey(0)

    def calculate_gradient(self, line):
        try:
            self.grad[line] = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
        except ZeroDivisionError:
            self.grad[line] = (line[0][1] - line[1][1])

    def close_enough(self, dot1, dot2):
        return ((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2) < self.__close_threshold

    def mergable_lines(self, line1, line2):
        return ((abs(self.grad.get(line1) - self.grad.get(line2)) < self.__parallel_threshold) and
                (self.close_enough(line1[0], line2[0]) and self.close_enough(line1[1], line2[1])))

    def average_dot(self, line1, line2):
        return ((line1[0][0] + line2[0][0]) / 2, (line1[0][1] + line2[0][1]) / 2), \
                ((line1[1][0] + line2[1][0]) / 2, (line1[1][1] + line2[1][1]) / 2)

    def merge_lines(self):
        for i in range(self.cv_line_num):
            for j in range(i+1, self.cv_line_num):
                if self.mergable_lines(self.cv_lines[i], self.cv_lines[j]):
                    self.merged_lines.append(self.average_dot(self.cv_lines[i], self.cv_lines[j]))

    def draw_lines(self):
        for line in self.merged_lines:
            Line(self.rst, line[0], line[1], CV_RGB(255, 0, 0), 1, CV_AA, 0)

    def calculate_basic_facts(self):
        for line in self.merged_lines:
            self.basic_facts[line] = (calculate_line_length(line),
                                      calculate_line_angle(line))

if __name__ == '__main__':
    # test
    handler = PreHandler('../test/test0.png')
