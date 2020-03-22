'''Data types for SpEx'''
from typing import List, NamedTuple


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


Data = List[Token]
