from graphene import ObjectType, String, Schema, Field, List
from graphene.test import Client
from pprint import pprint
import re

import functional_parser as parser

class LinkOut(ObjectType):

    children = List(lambda: Block)
    references = List(lambda: Block)

    def resolve_children(block, info):
        l = parser.get_links_out(block, parser.BLOCKS, {'children': parser.ALL_LINKS['children']})
        print(l)
        return [x for x in l['children']]

    def resolve_references(block, info):
        l = parser.get_links_out(block, parser.BLOCKS, {'references': parser.ALL_LINKS['references']})
        return [x for x in l['references']]

class LinkIn(ObjectType):

    children = List(lambda: Block)
    references = List(lambda: Block)

    def resolve_children(block, info):
        l = parser.get_links_in(block, parser.BLOCKS, {'children': parser.ALL_LINKS['children']})
        return [x for x in l['children']]

    def resolve_references(block, info):
        l = parser.get_links_in(block, parser.BLOCKS, {'references': parser.ALL_LINKS['references']})
        return [x for x in l['references']] 


class Token(ObjectType):
    type = String()
    value = String()
    target = String()

    def resolve_target(token, info):
        return parser.resolve_reference(token.value, parser.BLOCKS).id


class Block(ObjectType):
    id = String()
    content = List(Token)
    linkIn = Field(LinkIn)
    linkOut = Field(LinkOut)

    def resolve_id(block, info):
        return block.id

    def resolve_content(block, info):
        return block.content

    def resolve_linkIn(block, info):
        return block

    def resolve_linkOut(block, info):
        return block

class Query(ObjectType):
    block = Field(Block, id=String(default_value='~'))
    blocks = Field(List(Block), ids=List(String))

    def resolve_block(parent, info, id):
        return parser.block_by_id(id)

    def resolve_blocks(parent, info, ids):
        return [parser.block_by_id(i) for i in ids]


schema = Schema(query=Query)
