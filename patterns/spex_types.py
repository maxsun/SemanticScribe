'''Types for building SpEx'''
from pprint import pformat
from typing import Callable, FrozenSet, Iterable, List, NamedTuple
from collections import defaultdict

class Range(NamedTuple):
    '''Represents a range of numbers from <start> to <end>'''
    start: int
    end: int

    def __repr__(self):
        return '(%s, %s)' % (self.start, self.end)

    def __contains__(self, other: 'Range'):
        return self.start <= other.start and self.end >= other.end

    def intersect(self, other: 'Range') -> 'Range':
        return Range(max(self.start, other.start), min(self.end, other.end))



class Token(NamedTuple):
    '''Represents a typed value, with a corresponding range'''
    type: str
    text: str
    match: Range

    def update_type(self, new_type: str) -> 'Token':
        '''Returns a copy of this Token with <new_type>'''
        return Token(new_type, self.text, self.match)

    def __repr__(self):
        return '<%s @ %s: "%s">' % (self.type, self.match, self.text)

class TokenSetFast:
    '''
    Provides FASTER utilities for working with lists of Tokens
    Uses a 2d list mapping index to the id of tokens, which include that position.
    '''
    def __init__(self, tokens: Iterable[Token]):
        self.content: FrozenSet[Token] = frozenset(tokens)

        self.max_index = 0
        self.min_index = 0
        if len(tokens) > 0:
            self.max_index = max([tkn.match.end for tkn in self.content])
            self.min_index = min([tkn.match.start for tkn in self.content])

        self.index_to_tokens = defaultdict(set)
        self.id_to_token = {}
        for i, tkn in enumerate(self.content):
            self.id_to_token[i] = tkn

            for j in range(tkn.match.start, tkn.match.end):
                self.index_to_tokens[j].add(i)

        # self.index_to_tokens = [set() for _ in range(self.max_index - self.min_index)]
        # for tkn in self.content:


    def __eq__(self, other: 'TokenSetFast') -> bool:
        '''returns whether two token sets are equivalent'''
        if isinstance(other, TokenSetFast):
            return self.content == other.content
        raise TypeError('Only TokenSetFast can be added together!')

    def __add__(self, other: 'TokenSetFast') -> 'TokenSetFast':
        '''returns a TokenSet with the union of <self> & <other>'s contents'''
        if isinstance(other, TokenSetFast):
            return TokenSetFast(self.content.union(other.content))
        raise TypeError('Only TokenSetFast can be added together!')

    def intersect(self, other: 'TokenSetFast') -> 'TokenSetFast':
        '''returns a TokenSet with the intersection of <self> & <other>'s contents'''
        if isinstance(other, TokenSetFast):
            return TokenSetFast(self.content.intersection(other.content))
        raise TypeError('Only TokenSetFast can be intersected together!')

    def __repr__(self) -> str:
        return pformat(sorted(list(self.content), key=lambda x: x.match.start))

    def __len__(self) -> int:
        return len(self.content)

    def contains_type(self, type: str) -> bool:
        for token in self.content:
            if token.type == type:
                return True
        return

    def filter(self, func: Callable[[Token], bool]) -> 'TokenSetFast':
        '''returns a TokenSet containing anything which <func> maps to True'''
        return TokenSetFast([tkn for tkn in self.content if func(tkn)])

    def map(self, func: Callable[[Token], Token]) -> 'TokenSetFast':
        '''returns a TokenSet after <func> applying to each element'''
        return TokenSetFast([func(tkn) for tkn in self.content])

    def compile_to_str(self) -> str:
        '''returns the plaintext of the content tokens'''
        template = ['❓'] * (self.max_index - self.min_index)
        for token in self.content:
            for i in range(token.match.end - token.match.start):
                delta = token.match.start - self.min_index
                template[i + delta] = token.text[i]
        return ''.join(template)


    def subset(self, rng: Range) -> 'TokenSetFast':
        '''returns the subset of <self> in <rng>'''
        results = set()
        for i in range(rng.start, rng.end):
            results = results.union(self.index_to_tokens[i])
        in_range = set()
        for _id in results:
            in_range.add(self.id_to_token[_id])
        return TokenSetFast(in_range)

    def starts_at(self, idx: int) -> 'TokenSetFast':
        '''returns the subset of <self> starting at <idx>'''
        tokens_at_idx = self.subset(Range(idx, idx + 1))
        return tokens_at_idx.filter(lambda x: x.match.start == idx)

    def next_at(self, idx: int) -> 'TokenSetFast':
        '''returns the subset of <self> first starting after <idx>'''
        for i in range(idx, self.max_index):
            if len(self.index_to_tokens[i]) == 0:
                continue
            results = self.starts_at(i)
            if len(results.content) > 0:
                return results
        return TokenSetFast([])
