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
    for rule in rule_group:
        rule_obj = generate_a_rule(rule)
        print(rule_obj)
        print('\n')


def read_from_outside(file):
    with open('../rules/' + file) as f:
        rules = ''.join(f.read().splitlines())
    separate_rules(rules)

if __name__ == '__main__':
    # test
    read_from_outside('rules.txt')