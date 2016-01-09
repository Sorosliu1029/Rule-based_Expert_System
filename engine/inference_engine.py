# encoding:utf-8
"""

"""
import re
import string
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
    return Rule(if_part, then_part[0].strip('"\''), description_part[0].strip('"\''))


def separate_rules(rules):
    rule_group = re_a_rule.findall(rules)
    return list(map(generate_a_rule, rule_group))


def read_rules(rule_file):
    with open('../rules/' + rule_file) as f:
        rules = ''.join(f.read().splitlines())
    return separate_rules(rules)


def read_facts(fact_file):
    with open('../facts/' + fact_file) as f:
        facts = list(map(string.strip, f.readlines()))
    return facts


class Engine:
    """

    """
    def __init__(self, rule_library, fact_library):
        self.rule_library = rule_library
        self.fact_library = fact_library
        self.condition_stack = []            # using Python list as stack

    def push_condition_stack(self, condition):
        self.condition_stack.append(condition)

    def pop_condition_stack(self):
        return self.condition_stack.pop()

    def top_condition_stack(self):
        try:
            return self.condition_stack[-1]
        except IndexError:
            return None

    def condition_stack_is_empty(self):
        return not self.condition_stack

    def get_rule_library(self):
        return '\n'.join(list(map(str, self.rule_library)))

    def __match_facts__(self, ant):
        return ant in self.fact_library

    def __hit_consequent__(self, cons):
        hit = False
        for rule in self.rule_library:
            if cons == getattr(rule, 'consequent'):
                hit = True
                ants = getattr(rule, 'antecedent')
                for ant in ants:
                    if not self.__match_facts__(ant):
                        self.push_condition_stack(ant)
                break
        return hit

    def goal(self, target):
        self.push_condition_stack(target)

    def run(self):
        while self.condition_stack:
            # test
            print(self.condition_stack)
            cons = self.pop_condition_stack()
            if not self.__hit_consequent__(cons):
                print('WARNING: No sufficient facts!\n')
                break

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
    r = read_rules('rules.txt')
    f = read_facts('facts.txt')
    e = Engine(r, f)
    print(e)
    e.goal('the shape is obtuse triangle')
    e.goal('the shape is equilateral triangle')
    e.run()