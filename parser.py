""" Max Sun 2020 """
import os
from itertools import chain

from lark import Lark, Tree, Token, Transformer
from lark.indenter import Indenter

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


NOTES_FOLDER = './note_files/'
NOTE_PATHS = [x for x in os.listdir(NOTES_FOLDER) if x.endswith('.md')]


class TreeIndenter(Indenter):
    """A lexical processor for indentation"""
    NL_type = '_NL'
    OPEN_PAREN_types = ["OPEN_REF"]
    CLOSE_PAREN_types = ["CLOSE_REF"]
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


class BTransformer(Transformer):
    """Pos-processing to modify the lark generated tree"""
    def text(self, items):
        """Join words under text nodes in the AST"""
        return Token('TXT', ' '.join(items))

    def reference(self, items):
        """Join words under reference nodes in the AST"""
        return Token('REF', ' '.join(items))


class Block:
    """A class for representing and navigating textblocks in a tree structure."""
    def __init__(self, content, children=[]):
        self.content = content
        self.children = children

    @staticmethod
    def from_tree(block_tree):
        """Initialize a Block from a parsed AST"""
        content = block_tree.children[0].children
        children = block_tree.children[1].children
        children = [Block.from_tree(x) for x in children]
        return Block(content, children)

    def to_tree(self):
        """Returns self as a tree; useful for display in Jupyter"""
        children_node = Tree(data='children', children=[x.toTree() for x in self.children])
        content_node = Tree(data='content', children=self.content)
        return Tree(data='block', children=[content_node, children_node])

    def to_dict(self):
        """Returns self as a dictionary"""
        children = [x.to_dict() for x in self.children]
        content = []
        for token in self.content:
            content.append({
                'type': token.type,
                'value': str(token)
            })
        return {
            'type': 'block',
            'children': children,
            'content': content
        }

    def flatten(self, path=''):
        """
            Flatten self into a dictionary
            - keys are unique indicies to each child block
        """
        results = {}
        block_children = self.children
        results[path] = self
        for i, child in enumerate(block_children):
            results.update(child.flatten(path + '/' + str(i)))
        return results

    def get_refs(self, depth=100):
        """Return all refs in the textblock, search recursively up to <depth>"""
        all_refs = set()
        for token in self.content:
            if token.type == 'REF':
                all_refs.add(str(token))
        if depth > 0:
            for child in self.children:
                all_refs.update(child.get_refs(depth - 1))
        return all_refs

    def get_by_ref(self, ref, recursive=False):
        """Return all child textblocks containing <ref>"""
        results = []
        for token in self.content:
            if token.type == 'REF' and token == ref:
                results.append(self)
        if recursive:
            for child in self.children:
                results += child.get_by_ref(ref, recursive)
        return results

    def get_by_path(self, path):
        """
            Get child textblock relative to <path>
            - Example: "/0/1"
            refers to the second child of this blocks first child
        """
        head = path.split('/')[0]
        tail = '/'.join(path.split('/')[1:])
        if head == '' and len(tail) == 0:
            return self
        if head == '' and len(path.split('/')) > 1:
            return self.get_by_path(tail)
        if head.isnumeric():
            return self.children[int(head)].get_by_path(tail)

    def __iter__(self):
        "implement the iterator protocol"
        for child in chain(*map(iter, self.children)):
            yield child
        yield self

    def __repr__(self):
        return ' '.join(self.content)


GRAMMAR = r"""
    ?start: (_NL* block)* -> start
    block: "- " content _NL children
    children: [_INDENT block* _DEDENT]
    
    content: (text|reference)+
    text: (WORD)+
    reference: "[[" (WORD)+ "]]"
    
    WORD: /([^(\[|\]|\s)])/+
    
    %import common.LETTER
    %import common.DIGIT
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE
    _NL: /(\r?\n(\s)*)+/
"""

PARSER = Lark(
    GRAMMAR,
    parser='lalr',
    postlex=TreeIndenter(),
    transformer=BTransformer())


def parse_blocks(text):
    """Parse text into an array of block ASTs"""
    return PARSER.parse(text).children


def parse_notefile(note_path):
    """Parse a notefile into an AST, using the filename as the root"""
    text = open(note_path).read() + '\n'
    note_title = os.path.basename(note_path).replace('.md', '')
    blocks = [Block.from_tree(x) for x in parse_blocks(text)]
    root_text = [Token('REF', note_title)]
    return Block(content=root_text, children=blocks)


def parse_notefiles(folder_path):
    """Parse a folder of notefiles into an AST"""
    paths = [x for x in os.listdir(folder_path) if x.endswith('.md')]
    note_blocks = []
    for path in paths:
        note_tree = parse_notefile(NOTES_FOLDER + path)
        note_blocks.append(note_tree)
    return Block(content=[Token('REF', value='~')], children=note_blocks)


NOTES_FOLDER = './note_files/'
NOTES_DATA = parse_notefiles(NOTES_FOLDER)


def resolve_ref_block(ref_text, root_block):
    """Find a block by reference"""
    occurences = root_block.get_by_ref(ref_text, recursive=True)
    result_block = None
    if ref_text[0] == '/': # get block by path
        return root_block.get_by_path(ref_text)
    aggregate_children = []
    name = None
    for occurence in occurences:
        block_text = occurence.content
        if len(block_text) == 1 and block_text[0] == ref_text: # references a title block
            aggregate_children += occurence.children
            name = occurence.content
    if name is not None:
        result_block = Block(name, aggregate_children)
    if result_block is None and len(occurences) > 0: # construct an empty block
        result_block = Block(content=[Token('REF', value=ref_text)])
    return result_block


G = nx.DiGraph()

for x in NOTES_DATA.get_refs(depth=100):
    G.add_node(x)
    block = resolve_ref_block(x, NOTES_DATA)
    for ref in block.get_refs(depth=1):
        if x != ref:
            G.add_edge(x, ref)

print(to_agraph(G))
