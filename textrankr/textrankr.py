# -*- coding: utf-8 -*-

from re import split
from networkx import Graph
from networkx import pagerank
from itertools import combinations
from .sentence import Sentence


class TextRank(object):

    def __init__(self, text_with_frame_inds):
        self.sentences = [Sentence(text, i, frame_inds) for i, (text, frame_inds) in enumerate(text_with_frame_inds)]
        self.build()

    def build(self):
        #self._build_sentences()
        self._build_graph()
        self.pageranks = pagerank(self.graph, weight='weight')
        self.reordered = sorted(self.pageranks, key=self.pageranks.get, reverse=True)

    def _build_sentences(self):
        dup = {}
        candidates = split(r'(?:(?<=[^0-9])\.|\n)', self.text)
        self.sentences = []
        index = 0
        for candidate in candidates:
            while len(candidate) and (candidate[-1] == '.' or candidate[-1] == ' '):
                candidate = candidate.strip(' ').strip('.')
            if len(candidate) and candidate not in dup:
                dup[candidate] = True
                self.sentences.append(Sentence(candidate + '.', index))
                index += 1
        del dup
        del candidates

    def _build_graph(self):
        self.graph = Graph()
        self.graph.add_nodes_from(self.sentences)
        for sent1, sent2 in combinations(self.sentences, 2):
            weight = self._jaccard(sent1, sent2)
            if weight:
                self.graph.add_edge(sent1, sent2, weight=weight)

    def _jaccard(self, sent1, sent2):
        p = sum((sent1.bow & sent2.bow).values())
        q = sum((sent1.bow | sent2.bow).values())
        return p / q if q else 0

    def summarize(self, count=3):
        results = sorted(self.reordered[:count], key=lambda sentence: sentence.index)
        results = [result.text for result in results]
        return [(result.text, result.frame_inds) for result in results]
