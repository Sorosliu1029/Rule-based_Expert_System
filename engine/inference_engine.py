# encoding:utf-8
"""

"""
import re
import sys
sys.path.append('..')
from basic.basic_rule import Rule

__author__ = 'liuyang'


re_a_rule = re.compile(r'(\{.*?\})')
re_if_part = re.compile(r'^\{IF:\s+(\[.*?\])')
re_then_part = re.compile(r'THEN:\s+(\'.*?\')')
re_description_part = re.compile(r'DESCRIPTION:\s+(\'.*?\')')


def generate_a_rule(rule):
    if_part = ''
    exec('if_part = ' + re_if_part.findall(rule)[0])
    then_part = re_then_part.findall(rule)
    description_part = re_description_part.findall(rule)
    return Rule(if_part, then_part[0].strip('"').strip("'"), description_part[0].strip('"').strip("'"))


def separate_rules(rules):
    rule_group = re_a_rule.findall(rules)
    return list(map(generate_a_rule, rule_group))


def read_from_outside(file):
    with open('../rules/' + file) as f:
        rules = ''.join(f.read().splitlines())
    return separate_rules(rules)


class Engine:
    """

    """
    def __init__(self, rule_library):
        self.rule_library = rule_library
        self.condition_stack = []            # using Python list as stack

    def push_condition_stack(self, rule):
        self.condition_stack.append(rule)

    def pop_condition_stack(self):
        return self.condition_stack.pop()

    def condition_stack_is_empty(self):
        return not self.condition_stack

    def get_rule_library(self):
        return '\n'.join(list(map(str, self.rule_library)))


    def __str__(self):
        s = ''
        s += ('*' * 60 + '\n')
        s += 'Shape Detection Engine -- a Rule-based Expert System\n'
        s += '--------------- Below is all the rules ---------------\n'
        s += self.get_rule_library()
        s += '---------------- End of all the rules ----------------\n'
        return s





if __name__ == '__main__':
    # test
    l = read_from_outside('rules.txt')
    e = Engine(l)
    print(e)