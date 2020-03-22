'''Special Expressions; SpEx'''
import re
import time
from pprint import pprint
from typing import Callable, Dict, List, NamedTuple, Tuple


import automata as A
import auto_types as T


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
