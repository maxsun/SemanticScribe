'''module for building state machines to search through TokenSets'''
import re
from functools import reduce
from typing import List

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

import spex_types as T
import random


class Spec:

    def __init__(self, name: str):
        self.name = name
        self.requirements = set()

    def add_req(self, req):
        self.requirements.add(req)

    def match(self, tokens: T.TokenSetFast) -> T.TokenSetFast:
        return reduce(T.TokenSetFast.intersect, [tokens.filter(lambda x: f(x, tokens)) for f in self.requirements]).map(lambda x: x.update_type(self.name))


class Ruleset:

    def __init__(self, name):
        self.graph = nx.MultiDiGraph()
        self.name = name

    def add_instance(self, _id, _type) -> int:
        # _id = len(self.graph.nodes)
        self.graph.add_node(_id, type=_type)
        return _id

    def instance_by_id(self, id: str):
        return self.graph.nodes[id]

    def add_relation(self, tail: int, head: int):
        self.graph.add_edge(tail, head)

    def draw(self, filename='rules.png', label_key='type') -> None:
        G = self.graph.copy()
        labels = {}
        for node in G.nodes:
            labels[node] = {'label': G.nodes[node][label_key]}
        nx.set_node_attributes(G, labels)
        A = to_agraph(G)
        A.layout('dot')
        A.draw(filename)

    def start_types(self) -> List[str]:
        results = []
        for n in self.graph.nodes:
            if self.graph.in_degree(n) == 0:
                results.append(n)
        return results

    def match(self, tokens: T.TokenSetFast, instance_id: int = None) -> T.TokenSetFast:
        '''Returns the first subset of a Tokenset satisifies the ruleset.'''
        if instance_id is None:
            instance_id = self.start_types()[0]
        start_index = tokens.min_index
        first_tokens = tokens.starts_at(start_index)
        target_type = self.instance_by_id(instance_id)['type']

        accepted_tokens = first_tokens.filter(lambda x: x.type == target_type)
        if len(accepted_tokens) == 0:
            return T.TokenSetFast([])

        next_node_ids = list(self.graph.neighbors(instance_id))
        if len(next_node_ids) == 0:
            return tokens.subset(T.Range(start_index, accepted_tokens.max_index))

        # results: List[T.TokenSet] = []
        for node_id in next_node_ids:
            for accepted_tkn in accepted_tokens.content:
                next_range = T.Range(accepted_tkn.match.end, tokens.max_index)
                match = self.match(tokens.subset(next_range), node_id)
                if len(match) > 0:
                    return tokens.subset(T.Range(start_index, match.max_index))

        # if len(results) > 0:
        #     min_result_index = min([x.max_index for x in results])
        #     return tokens.subset(T.Range(start_index, min_result_index))
        return T.TokenSetFast([])

    def find(self, tokens: T.TokenSetFast, count: int = 100, start: str='cw') -> List[T.TokenSetFast]:
        start_types = self.start_types()

        window_size = 300  # in number of characters
        i = 2768
        num_found = 0
        results = set()
        while num_found < count and i < tokens.max_index:
            x = tokens.subset(T.Range(i, i + window_size))
            m = self.match(x, start)
            if len(m) == 0:
                i = tokens.next_at(i + 1).min_index
            else:
                results.add(T.Token(self.name, m.compile_to_str(),
                                    T.Range(m.min_index, m.max_index)))
                num_found += 1
                i = tokens.next_at(m.max_index).min_index
        return T.TokenSetFast(results)
