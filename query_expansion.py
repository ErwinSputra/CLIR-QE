from nltk.corpus import wordnet as wn
from preprocessing import Prapengolahan
import numpy as np


class QE:
    def __init__(self):
        self.pra = Prapengolahan()

    def expanding_query(self, query):
        query = self.pra.tokenize_and_extract(query)
        rule = -1
        idx = 1
        if len(query) == 1:
            idx = 3
            rule = 1
        elif len(query) == 2:
            rule = 2
        elif len(query) == 3:
            rule = 5

        dict = {}
        synonyms = []
        for term in query:
            i = 0
            dict[term] = False
            synonyms.append(term)
            if len(wn.synsets(term)) != 0:
                for syn in wn.synsets(term):
                    for lem in syn.lemmas():
                        if lem.name().lower() not in synonyms and i != idx:  # lem.name().lower()
                            synonyms.append(lem.name())
                            dict[term] = True
                            i += 1

        theterm = ''
        testterm = []
        i = 0
        if len(dict) > 1:
            for item in dict:
                if not dict[item]:
                    if rule == 2:
                        theterm = item
                    if rule == 5:
                        testterm.append(item)
                    i += 1

        if rule == 5:
            if i == 3:
                rule = 12
            elif len(testterm) == 2:
                main_term = np.setdiff1d(query, testterm)
                index = query.index(main_term)
                if index == 0:
                    rule = 6
                if index == 1:
                    rule = 7
                if index == 2:
                    rule = 8
            elif len(testterm) == 1:
                index = query.index(testterm[0])
                if index == 0:
                    rule = 9
                if index == 1:
                    rule = 10
                if index == 2:
                    rule = 11

        if rule == 2:
            if theterm != '':
                index = query.index(theterm)
                if index == 0:
                    rule = 3
                if index == 1:
                    rule = 4
            elif i == 2:
                rule = 0

        return synonyms, rule

    @staticmethod
    def list_to_string(s):
        str1 = ""
        i = 1
        for ele in s:
            if i == len(s):
                str1 += ele
            else:
                str1 += ele + " "
            i += 1

        return str1
