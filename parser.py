"""This contains code for parsing notes into a knowledge graph"""
import os
from pprint import pprint
from lark import Lark
from lark.indenter import Indenter


class TreeIndenter(Indenter):
    """Post-processor to detect nesting of text blocks"""
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2


def parse_blocks(blocks):
    """Turn a list of text block trees into a nested dictionary"""
    results = []
    for block in blocks:
        blocktext = block.children[0].children
        children = block.children[1].children
        children = parse_blocks(children)
        results.append({
            'text': blocktext,
            'children': children
        })
    return results


def parse_note_tree(note_path):
    """Parse the note at <note_path>"""
    text = open(note_path).read() + '\n'
    tree = PARSER.parse(text)
    return tree


GRAMMAR = open('grammar.lark').read()

PARSER = Lark(
    GRAMMAR,
    parser='lalr',
    postlex=TreeIndenter())


if __name__ == '__main__':
    NOTES_FOLDER = './note_files/'
    NOTE_PATHS = [x for x in os.listdir(NOTES_FOLDER) if x.endswith('.md')]

    for path in NOTE_PATHS:
        note_title = path.replace('.md', '')
        note_tree = parse_note_tree(NOTES_FOLDER + path)
        note_data = parse_blocks(note_tree.children)
        print(note_title)
        pprint(note_data)
