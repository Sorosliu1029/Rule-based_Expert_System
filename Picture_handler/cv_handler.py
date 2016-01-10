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


def calculate_line_length(line):
    return ((line[0][0] - line[1][0]) ** 2 + (line[0][1] - line[1][1]) ** 2) ** 0.5


def calculate_line_angle(line):
    try:
        k = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
    except ZeroDivisionError:
        k = 100000
    finally:
        return math.degrees(math.atan(k))


class HandledLine:
    """

    """
    def __init__(self, line):
        self.point1 = line[0]
        self.point2 = line[1]
        self.length = calculate_line_length(line)
        self.angle = calculate_line_angle(line)

    def __str__(self):
        return '(%.2f, %.2f)-->(%.2f, %.2f): Length: %.2f, Angle:%.2f' % \
               (self.point1[0], self.point1[1], self.point2[0], self.point2[1], self.length, self.angle)


close_threshold = 800
parallel_threshold = 20


def show_image(image, title='New Image'):
    NamedWindow(title, 1)
    ShowImage(title, image)


def close_enough(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) < close_threshold


def mergable_lines(grad, line1, line2):
    return ((abs(grad.get(line1) - grad.get(line2)) < parallel_threshold) and
            (close_enough(line1[0], line2[0]) and close_enough(line1[1], line2[1])))


def average_point(point1, point2):
    return (point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2


def average_line(line1, line2):
    return average_point(line1[0], line2[0]), average_point(line1[1], line2[1])


class PreHandler:
    """

    """
    def __init__(self, source):
        self.grad = {}
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
        # test
        # for line in self.merged_lines:
        #     print(line)
        # self.draw_lines(self.merged_lines)
        # show_image(self.src, 'src')
        # show_image(self.rst, 'rst')
        # WaitKey(0)
        # test

    def calculate_gradient(self, line):
        try:
            self.grad[line] = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
        except ZeroDivisionError:
            self.grad[line] = (line[0][1] - line[1][1])

    def merge_lines(self):
        for i in range(self.cv_line_num):
            for j in range(i+1, self.cv_line_num):
                if mergable_lines(self.grad, self.cv_lines[i], self.cv_lines[j]):
                    self.merged_lines.append(HandledLine(average_line(self.cv_lines[i], self.cv_lines[j])))

    def draw_lines(self, lines):
        for line in lines:
            Line(self.rst, line.point1, line.point2, CV_RGB(255, 0, 0), 1, CV_AA, 0)


def get_meeting_point(line1, line2):
    if abs(line1.angle - line2.angle) < parallel_threshold2:
        return 'parallel'
    else:
        for point1 in [line1.point1, line1.point2]:
            for point2 in [line2.point1, line2.point2]:
                if close_enough(point1, point2):
                    return average_point(point1, point2)
    return None


def is_same_side(line1, line2, meeting_point):
    middle_point1 = average_point(line1.point1, line1.point2)
    middle_point2 = average_point(line2.point1, line2.point2)
    return meeting_point < middle_point1 and meeting_point < middle_point2


def get_included_angle(line1, line2):
    meeting_point = get_meeting_point(line1, line2)
    included_angle = max(line1.angle, line2.angle) - min(line1.angle, line2.angle)
    if not meeting_point:
        return None          # lines not met
    if meeting_point == 'parallel':
        return 'parallel'    # parallel lines have no included angle
    if is_same_side(line1, line2, meeting_point):
        return included_angle if included_angle < 90.0 else 180 - included_angle
    else:
        return included_angle if included_angle > 90.0 else 180 - included_angle


def is_parallel(line1, line2):
    return True if get_included_angle(line1, line2) == 'parallel' else False


def is_vertical(line1, line2):
    included_angle = get_included_angle(line1, line2)
    return True if included_angle and abs(included_angle - 90.0) < vertical_threshold else False


def is_acute(line1, line2):
    included_angle = get_included_angle(line1, line2)
    return included_angle and included_angle < 90.0


def is_obtuse(line1, line2):
    included_angle = get_included_angle(line1, line2)
    return included_angle and included_angle > 90.0


def is_equal(line1, line2):
    return abs(line1.length - line2.length) < equal_threshold


equal_threshold = 30
parallel_threshold2 = 5
vertical_threshold = 5


class Fact:
    """

    """
    def __init__(self, f, about):
        self.fact = f
        self.about = about

    def __str__(self):
        s = self.fact + '\n'
        s += '\n'.join(list(map(str, self.about)))
        return s


class FactGenerator:
    """

    """
    def __init__(self, lines, file_path):
        self.lines = lines
        self.facts = []
        self.file = open(file_path, 'r+')

    def __del__(self):
        if self.file:
            self.file.close()

    def __about_length(self, line1, line2):
        if is_equal(line1, line2):
            self.facts.append(Fact('two lines are equal', [line1, line2]))

    def __about_angle(self, line1, line2):
        if is_parallel(line1, line2):
            self.facts.append(Fact('two lines are parallel', [line1, line2]))
        elif is_vertical(line1, line2):
            self.facts.append(Fact('two lines are vertical', [line1, line2]))
            self.facts.append(Fact('one angle is right angle', [line1, line2]))
        elif is_acute(line1, line2):
            self.facts.append(Fact('one angle is acute angle', [line1, line2]))
        elif is_obtuse(line1, line2):
            self.facts.append(Fact('one angle is obtuse angle', [line1, line2]))

    def generate_fact(self):
        for i in range(len(self.lines)):
            for j in range(i+1, len(self.lines)):
                self.__about_length(self.lines[i], self.lines[j])
                self.__about_angle(self.lines[i], self.lines[j])

if __name__ == '__main__':
    # test
    handler = PreHandler('../test/test.png')
    generator = FactGenerator(handler.merged_lines, '../facts/facts.txt')
    generator.generate_fact()
    print(not generator.facts)
    print('-------lines-------')
    for line in handler.merged_lines:
        print(line)
    print('-------end---------')
    print('-------facts-------')
    for fact in generator.facts:
        handler.draw_lines(fact.about)
        print(fact)
    print('-------end---------')
    show_image(handler.rst, 'result')
    WaitKey(0)