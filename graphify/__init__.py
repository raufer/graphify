import logging
import sys
import os


sys.setrecursionlimit(100000)

logger = logging.getLogger(__name__)

logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# class Graphify(object):
#     """
#     Graphify ...
#     """
#     def __init__(self, descriptor, markup='text'):
#         self.descriptor = descriptor
#         self.markup = markup
#
#         if markup == 'xml':
#             self.builder = GraphBuilderXML(self.descriptor)
#         else:
#             self.builder = GraphBuilder(self.descriptor)
#
#     def parse_iterable(self, iterable):
#         """
#         Given an iterable structure, parse them into a 'networkx' graph and return a 'Doc' object
#         """
#         graph = self.builder.parse(iterable)
#         return graph
#
#     def parse_file(self, filepath, encoding='utf-8'):
#         with open(filepath, "r", encoding=encoding) as f:
#             lines = f.readlines()
#             return self.parse_iterable(lines)
#
#     def parse_url(self, url):
#         pass
#
#     def set_description(self, description):
#         """reset the description to a different one from the one provided in the initialization"""
#         self.descriptor = description
#         self.builder = GraphBuilder(self.descriptor)
#

