""" Max Sun 2020 """
import os

from lark import Lark, Token, Transformer
from lark.indenter import Indenter

from networkx.drawing.nx_agraph import to_agraph

from text_block import TextBlock

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


class TreeTransformer(Transformer):
    """Pos-processing to modify the lark generated tree"""
    @staticmethod
    def text(items):
        """Join words under text nodes in the AST"""
        return Token('TXT', ' '.join(items))

    @staticmethod
    def reference(items):
        """Join words under reference nodes in the AST"""
        return Token('REF', ' '.join(items))

GRAMMAR = open('./grammar.lark').read()

PARSER = Lark(
    GRAMMAR,
    parser='lalr',
    postlex=TreeIndenter(),
    transformer=TreeTransformer)


def parse_text(text):
    """Parse text into an array of block ASTs"""
    return PARSER.parse(text).children


def parse_notefile(note_path):
    """Parse a notefile into an AST, using the filename as the root"""
    text = open(note_path).read() + '\n'
    note_title = os.path.basename(note_path).replace('.md', '')
    blocks = [TextBlock.from_tree(x) for x in parse_text(text)]
    root_text = [Token('REF', note_title)]
    return TextBlock(content=root_text, children=blocks)


def parse_notefiles(folder_path):
    """Parse a folder of notefiles into an AST"""
    paths = [x for x in os.listdir(folder_path) if x.endswith('.md')]
    note_blocks = []
    for path in paths:
        note_tree = parse_notefile(NOTES_FOLDER + path)
        note_blocks.append(note_tree)
    return TextBlock(content=[Token('REF', value='~')], children=note_blocks)


if __name__ == '__main__':
    NOTES_FOLDER = './note_files/'
    NOTES_DATA = parse_notefiles(NOTES_FOLDER)
    G = NOTES_DATA.to_graph()
    print(to_agraph(G))
