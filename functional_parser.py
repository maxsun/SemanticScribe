"""A .tht parser"""
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import re
from typing import List, Callable, Dict
import hashlib

@dataclass
class Token:
    '''Class representing a token with <type> and <value>

    Attributes:
        type (str): The token type.
        value (str): The token value.
    '''
    type: str
    value: str
    target: str = ''


@dataclass
class Block:
    '''Class representing a block with an <id> and <content>

    Attributes:
        id (str): A unique block id, likely a hash of its content. 
        content (List[Token]): The block's content; a list of tokens.
        indent (int): **this should probably be removed**
    '''
    id: str
    content: List[Token]
    indent: int

    def __repr__(self):
        return self.id + ': ' + ' '.join([x.value for x in self.content])


def block(content: List[Token], indent: int = 0) -> Block:
    '''Returns a block with an id generated based on <content>'''
    return Block(
        id=hex(int(hashlib.md5(str([x.value for x in content]).encode()).hexdigest(), 16)),
        content=content,
        indent=indent,
    )

SUPEROOT_BLOCK = block([Token('REF', '~')], -1)

def tokenize(line_text: str) -> List[Token]:
    '''Convert a string into tokens'''
    words: List[str] = re.split(r'\s+', line_text)
    references = re.findall(r'(\[\[[^\[|\]]+\]\])+', line_text)
    tokens = []
    for word in words:
        if word in references:
            tokens.append(Token('REF', word))
        else:
            tokens.append(Token('TXT', word))
    return tokens


def parse(lines: List[str]) -> List[Block]:
    '''Read a list of strings into a list of blocks'''
    blocks: List[Block] = [SUPEROOT_BLOCK]
    for line in lines:
        line = line.replace('\n', '')
        if line:
            line_text = re.sub(r'(^\s*\-\s*)', '', line)
            if len(line_text.strip()) > 0:
                indent = len(line) - len(line.lstrip())
                blocks.append(block(
                    content=tokenize(line_text),
                    indent=indent
                ))
    return blocks


def filter_blocks(
        blocks: List[Block],
        pred: Callable[[Block], bool]) -> List[Block]:
    '''Returns the subset of <blocks> which satisfy <pred>'''
    results: List[Block] = []
    for blk in blocks:
        if pred(blk):
            results.append(blk)
    return results


def block_contains_value(blk: Block, value: str) -> bool:
    '''Returns whether a token in <block>'s content has <value>'''
    return value in [x.value for x in blk.content]


def resolve_parent(child: Block, blocks: List[Block]) -> Block:
    '''Returns the first block preceding <child> with less indentation'''
    if child not in blocks:
        return SUPEROOT_BLOCK
    child_index = blocks.index(child)
    prev_blocks = blocks[:child_index]
    for blk in prev_blocks[::-1]:
        if blk.indent < child.indent:
            return blk
    return SUPEROOT_BLOCK


def resolve_immediate_children(parent: Block, blocks: List[Block]) -> List[Block]:
    '''Returns all blocks which have <parent> as their parent.'''
    if parent not in blocks:
        return []
    return filter_blocks(
        blocks[blocks.index(parent) + 1:],
        lambda b: resolve_parent(b, blocks) == parent
    )


def resolve_reference(ref_value: str, blocks: List[Block]) -> Block:
    '''Returns a block who's content is [Token('REF', <ref_value>)]'''
    for blk in blocks:
        if len(blk.content) == 1 and len(blk.content[0].type) == 'REF':
            if blk.content[0].value == ref_value:
                return blk
    return block([Token('REF', ref_value)], indent=0)


def resolve_block_references(blk, blocks):
    '''Returns all blocks which are references in <blk>'s content'''
    refs = []
    for token in blk.content:
        if token.type == 'REF':
            refs.append(resolve_reference(token.value, blocks))
    return refs


def get_links_out(
        blk: Block,
        blocks: List[Block],
        links: Dict[str, Callable[[Block, List[Block]], List[Block]]]) -> Dict[str, List[Block]]:
    '''Get links from <blk> to others in <blocks>'''
    links_out = defaultdict(lambda: [])
    for link_type in links:
        links_out[link_type] += links[link_type](blk, blocks)
    return links_out


def get_links_in(
        blk: Block,
        blocks: List[Block],
        links: Dict[str, Callable[[Block, List[Block]], List[Block]]]) -> Dict[str, List[Block]]:
    '''Get links from others in <blocks> to <blk>'''
    links_in = defaultdict(lambda: [])
    for b in blocks:
        b_out = get_links_out(b, blocks, links)
        for link_type in b_out:
            if blk in b_out[link_type]:
                links_in[link_type].append(b)
    return links_in

ALL_LINKS = {
    'references': resolve_block_references,
    'children': resolve_immediate_children
}

BLOCKS = parse(re.split(r'(\s*\-.*\n)', '''
- [[G.W.]]
    - crossed the Delaware
    - was the first [[President]]
    - led the [[American_Revolution]]
- [[President]]
    - the highest ranking American government position
    - **not** a king!
        - America was founded to escape monarchy/tyranny
- The [[American_Revolution]] began in 1765
    - the [[War]] didn't start until 1775 though
    - marks the foundation of [[America]]
        - Led by [[G.W.]]
'''))

all_refs = set()
for b in BLOCKS:
    for token in b.content:
        if not resolve_reference(token.value, BLOCKS) in BLOCKS:
            BLOCKS.append(resolve_reference(token.value, BLOCKS))

id_to_block = {}
for b in BLOCKS:
    id_to_block[b.id] = b

id_to_block['~'] = resolve_reference('~', BLOCKS)

def block_by_id(id: str) -> Block:
    return id_to_block[id]
