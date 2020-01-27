"""Text Block Class"""
from itertools import chain
from lark import Tree, Token
import networkx as nx

class TextBlock:
    """A class for representing and navigating textblocks in a tree structure."""
    def __init__(self, content, children=[]):
        self.content = content
        self.children = children

    @staticmethod
    def from_tree(block_tree):
        """Initialize a Block from a parsed AST"""
        content = block_tree.children[0].children
        children = block_tree.children[1].children
        children = [TextBlock.from_tree(x) for x in children]
        return TextBlock(content, children)

    def to_tree(self):
        """Returns self as a tree; useful for display in Jupyter"""
        children_node = Tree(data='children', children=[x.to_tree() for x in self.children])
        content_node = Tree(data='content', children=self.content)
        return Tree(data='block', children=[content_node, children_node])

    def to_graph(self):
        """
            Returns self as a NetworkX DiGraph
            nodes = references,
            edges = co-occurences
        """
        graph = nx.DiGraph()
        for ref in self.get_refs(depth=100):
            graph.add_node(ref)
            block = self.resolve_ref_block(ref)
            for child_ref in block.get_refs(depth=1):
                if ref != child_ref:
                    graph.add_edge(ref, child_ref)
        return graph

    def to_dict(self, path=''):
        """Returns self as a dictionary"""
        children = [x.to_dict(path + '/' + str(i)) for i, x in enumerate(self.children)]
        content = []
        for token in self.content:
            content.append({
                'type': token.type,
                'value': str(token)
            })
        return {
            'type': 'block',
            'children': children,
            'content': content,
            'path': path
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
        return self.resolve_ref_block(head).get_by_path(tail)

    def resolve_ref_block(self, ref_text):
        """Find a block by reference"""
        occurences = self.get_by_ref(ref_text, recursive=True)
        result_block = None
        if ref_text[0] == '/': # get block by path
            return self.get_by_path(ref_text)
        aggregate_children = []
        name = None
        for occurence in occurences:
            block_text = occurence.content
            if len(block_text) == 1 and block_text[0] == ref_text: # references a title block
                aggregate_children += occurence.children
                name = occurence.content
        if name is not None:
            result_block = TextBlock(name, aggregate_children)
        if result_block is None and len(occurences) > 0: # construct an empty block
            result_block = TextBlock(content=[Token('REF', value=ref_text)])
        return result_block

    def __iter__(self):
        "implement the iterator protocol"
        for child in chain(*map(iter, self.children)):
            yield child
        yield self

    def __repr__(self):
        return '- [{0}]'.format(' '.join(self.content))
