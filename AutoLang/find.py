'''Scripts for finding substrings'''
import re
from pprint import pprint
from typing import List, NamedTuple, Tuple, Text, FrozenSet
# from termcolor import cprint, colored
import colored


class Span(NamedTuple):
    '''Represents a range of numbers spanning from <start> to <end>'''
    start: int
    end: int

    def __repr__(self):
        return '(%s, %s)' % (self.start, self.end)

    def __contains__(self, other: object):
        if isinstance(other, Span):
            return self.start <= other.start and self.end >= other.end
        else:
            raise TypeError('Spans can only contain other spans!')

    def intersect(self, other: 'Span') -> 'Span':
        if isinstance(other, Span):
            return Span(max(self.start, other.start), min(self.end, other.end))
        else:
            raise TypeError('Spans can only intersect with other spans!')

    def translate_right(self, amount: int) -> 'Span':
        return Span(self.start + amount, self.end + amount)

    def translate_left(self, amount: int) -> 'Span':
        return Span(self.start - amount, self.end - amount)

    def skew_right(self, amount: int) -> 'Span':
        return Span(self.start, self.end + amount)

    def skew_left(self, amount: int) -> 'Span':
        return Span(self.start + amount, self.end)

class MatchSet(NamedTuple):
    members: FrozenSet[Span]

    def __contains__(self, s: Span) -> bool:
        return s in self.members

    def union(self, other: 'MatchSet') -> 'MatchSet':
        return MatchSet(self.members.union(other.members))

    def intersect(self, other: 'MatchSet') -> 'MatchSet':
        return MatchSet(self.members.intersection(other.members))

    def map(self, func) -> 'MatchSet':
        return MatchSet(frozenset([func(x) for x in self.members]))

    def filter(self, func, ctx: Text) -> 'MatchSet':
        return MatchSet(frozenset([x for x in self.members if func(x, ctx)]))


class Info(NamedTuple):
    context: Text
    matches: MatchSet

    def union(self, other: 'Info') -> 'Info':
        if self.context != other.context:
            raise Exception('Mismatching contexts!')
        return Info(self.context, self.matches.union(other.matches))

    def intersect(self, other: 'Info') -> 'Info':
        if self.context != other.context:
            raise Exception('Mismatching contexts!')
        return Info(self.context, self.matches.intersect(other.matches))


    def map(self, func) -> 'Info':
        return Info(self.context, self.matches.map(func))

    def filter(self, func) -> 'Info':
        return Info(self.context, self.matches.filter(func, self.context))

    def highlight(self) -> Text:
        text = list(self.context)
        for match in self.matches.members:
            for idx, i in enumerate(range(match.start, match.end)):
                if i < len(text):
                    if text[i] == '\n':
                        text[i] = colored.stylize('↩️' + text[i], colored.bg('blue'))
                    else:
                        text[i] = colored.stylize(text[i], colored.bg('blue'))
        return ''.join(text) + colored.attr('reset')



def read(filename: str) -> Text:
    return open(filename, 'r').read()


def write(filename: str, text: Text) -> None:
    open(filename, 'w').write(text)
    return None


def find(context: Text, pat: str, type_name: str) -> Info:
    matches = []
    for m in re.finditer(pat, context):
        matches.append(Span(*m.span(0)))
    return Info(context, MatchSet(frozenset(matches)))



def highlight_multi(infos: List[Info]) -> Text:
    colors = [
        colored.bg('blue'),
        colored.bg('dark_green'),
        colored.bg('sky_blue_1')
    ]
    text = list(infos[0].context)
    for info_idx, info in enumerate(infos):
        for match in info.matches.members:
            for idx, i in enumerate(range(match.start, match.end)):
                text[i] = colored.stylize(text[i], colors[info_idx])

    return ''.join(text) + colored.attr('reset')


t = read('./sherlock.txt')
words = find(t, r'\b\w+\b', 'word')

caps = find(t, r'[A-Z]', 'caps') 

punct = find(t, r'[.,\/#!$%\^&\*\;:{}=\-_`~()]', 'punct')
ws = find(t, r'\s+|', 'whitespace')
nl = find(t, r'\n', 'newline')


word_starts = words.map(lambda x: x.skew_right(-1* (x.end - x.start - 1)))
cap_word_starts = caps.intersect(word_starts)
# print(cap_word_starts.highlight())
w = words.filter(lambda x, _: x.skew_right(-1* (x.end - x.start - 1)) in cap_word_starts.matches)
# print(w.highlight())

print(highlight_multi([w, punct]))
# print(cap_word_starts.matches)
# View Words in Frame "just first symbol"
# 
# 

