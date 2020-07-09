# -*- coding: utf-8 -*-

from collections import Counter
from konlpy.tag import Okt


class Sentence(object):

    okt = Okt()

    def __init__(self, text, index=0, frame_inds=None):
        self.index = index
        self.text = text.strip()
        self.tokens = self.okt.phrases(self.text)
        self.bow = Counter(self.tokens)
        self.frame_inds = frame_inds

    def __str__(self):
        return self.text

    def __hash__(self):
        return self.index
