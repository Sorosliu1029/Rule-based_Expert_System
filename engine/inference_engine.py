# encoding:utf-8
"""

"""
import re
import sys
sys.path.append('..')
from basic.basic_rule import Rule
from Picture_handler.cv_handler2 import Handler, FactGenerator

__author__ = 'liuyang'


re_a_rule = re.compile(r'(\{.*?\})')
re_if_part = re.compile(r'^\{IF:\s+(\[.*?\])')
re_then_part = re.compile(r'THEN:\s+(\'.*?\')')
re_description_part = re.compile(r'DESCRIPTION:\s+(\'.*?\')')


def generate_a_rule(rule):
    if_part = ''
    exec('if_part = ' + re_if_part.findall(rule)[0])
    then_part = re_then_part.findall(rule)[0]
    description_part = re_description_part.findall(rule)[0]
    return Rule(if_part, then_part.strip('"\''), description_part.strip('"\''))


def separate_rules(rules):
    rule_group = re_a_rule.findall(rules)
    return list(map(generate_a_rule, rule_group))


def read_rules(rule_file):
    with open('../rules/' + rule_file) as f:
        rules = ''.join(f.read().splitlines())
    return separate_rules(rules)


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

    def __match_facts__(self, ant, contour_index):
        facts = self.fact_library['Contour' + str(contour_index)]
        matched = False
        for fact in facts.line_facts:
            if ant == fact.fact:
                matched = True
                return matched
        for fact in facts.angle_facts:
            if ant == fact.fact:
                matched = True
                return matched
        return matched

    def __hit_consequent__(self, cons, contour_index):
        hit = False
        for rule in self.rule_library:
            if cons == getattr(rule, 'consequent'):
                hit = True
                ants = getattr(rule, 'antecedent')
                for ant in ants:
                    if not self.__match_facts__(ant, contour_index):
                        self.push_condition_stack(ant)
                break
        return hit

    def goal(self, target):
        self.condition_stack = []
        self.push_condition_stack(target)

    def run(self, contour_index):
        while self.condition_stack:
            # test
            # print(self.condition_stack)
            cons = self.pop_condition_stack()
            if not self.__hit_consequent__(cons, contour_index):
                return 'ERROR: No Sufficient Facts in Contour%d' % contour_index
        return 'SUCCESS: Find Required Shape in Contour%d' % contour_index

    def main_run(self):
        pass

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


def setup_engine(image_source):
    handler = Handler(image_source)
    handler.generate_contour_dict()
    generator = FactGenerator(handler.contour_dict)
    generator.generate_fact()
    r = read_rules('rules.txt')
    e = Engine(r, generator.handled_facts)
    return e


def set_goal(e, my_goal):
    e.goal(my_goal)


def main_run(e):
    results = []
    for i in range(len(e.fact_library)):
        result = e.run(i)
        results.append(result)
    return results


if __name__ == '__main__':
    # test
    e = setup_engine('../test/test41.png')
    set_goal(e, 'the shape is triangle')
    results = main_run(e)
