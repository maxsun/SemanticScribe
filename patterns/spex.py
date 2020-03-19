'''Special Expressions; SpEx'''
import re
import time
from pprint import pprint
from typing import Callable, Dict, List, NamedTuple, Tuple


import spex_automata as A
import spex_types as T


def first_pass_process(patterns: Dict, text: str) -> T.TokenSetFast:
    tokens = []
    for pat_type, pat in patterns.items():
        for m in re.finditer(pat, text):
            r = T.Range(m.span(0)[0], m.span(0)[1])
            tokens.append(T.Token(pat_type, m.group(0), r))

    tokens = T.TokenSetFast(tokens)
    return tokens


def process(patterns: Dict, tokens: List[T.Token]) -> T.TokenSetFast:
    results = tokens
    for pat_name in patterns:
        start_time = time.time()
        x = patterns[pat_name](results)
        duration = time.time() - start_time
        print('Found %s %s(s) in %.2fs.' % (len(x), pat_name, duration))
        results = results + x
    return results


cap_words2 = A.Spec('cap_word')
cap_words2.add_req(lambda x, _: x.type == 'word')
cap_words2.add_req(lambda x, ctx: ctx.starts_at(
    x.match.start).contains_type('caps'))


rules = A.Ruleset('sent')

rules.add_instance('cw', 'cap_word')
rules.add_instance('w', 'word')
rules.add_instance('ws', 'whitespace')
rules.add_instance('end', 'sent_end')
rules.add_instance('p', 'punct')

rules.add_relation('cw', 'ws')
rules.add_relation('cw', 'end')
rules.add_relation('w', 'ws')
rules.add_relation('ws', 'w')
rules.add_relation('w', 'end')
rules.add_relation('w', 'p')
rules.add_relation('p', 'ws')
rules.draw()

paras = A.Ruleset('para')

paras.add_instance('ws', 'whitespace')
paras.add_instance('sent', 'sent')
paras.add_instance('nl', 'newline')
paras.add_instance('nl2', 'newline')


paras.add_relation('nl', 'sent')
paras.add_relation('sent', 'ws')
paras.add_relation('ws', 'sent')
paras.add_relation('sent', 'nl2')
# paras.add_relation('nl', 'nl2')
paras.draw()


# text_path = './sherlock.txt'
# text = open(text_path).read()

# reg_pats = {
#     'word': re.compile(r'\b\w+\b'),
#     'punct': re.compile(r'[.,\/#!$%\^&\*;:{}=\-_`~()]'),
#     'caps': re.compile(r'[A-Z]'),
#     'sent_end': re.compile(r'[.!?]'),
#     'whitespace': re.compile(r'\s+'),
#     'newline': re.compile(r'\n')
# }

# tokens = first_pass_process(reg_pats, text)
# print('# punct fount:', len(tokens.filter(lambda x: x.type == 'punct')))


# x = process({
#     'cap_word': cap_words2.match,
#     'sent': lambda x: rules.find(x, 100, 'cw'),
#     'para': lambda x: paras.find(x, 2, 'nl')
# }, tokens)

# # pprint(len(x))

# pprint(x.filter(lambda x: x.type == 'para'))
