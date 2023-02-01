from query_expansion import QE
from term_weighting import PembobotanKata
from preprocessing import Prapengolahan
import math


class VSM:
    def __init__(self, inv_idx, tfidf_doc):
        self.query_exp = QE()
        self.inv_idx = inv_idx
        self.tf_idf_doc = tfidf_doc
        self.pmbKata = PembobotanKata()
        self.pra = Prapengolahan()

    def cos_sim(self, q_expansion):
        tfidf_query = self.pmbKata.tf_idf_query(q_expansion)
        dot_product = 0
        query_mod = 0
        doc_mod = 0
        print(tfidf_query)
        if len(tfidf_query) == 0:
            return -999
        else:
            cossim = {}
            doks = []
            for term in q_expansion:
                for document in self.inv_idx[term]:
                    if document not in doks:
                        for word in q_expansion:
                            dot_product += tfidf_query.get(word, 0) * self.tf_idf_doc[word].get(document, 0)
                            query_mod += tfidf_query.get(word, 0) ** 2
                            doc_mod += self.tf_idf_doc[word].get(document, 0) ** 2
                        query_mod = math.sqrt(query_mod)
                        doc_mod = math.sqrt(doc_mod)
                        denominator = query_mod * doc_mod
                        if denominator != 0:
                            cossim[document] = dot_product / denominator
                        dot_product = 0
                        query_mod = 0
                        doc_mod = 0
                        doks.append(document)
            return sorted(cossim.items(), key=lambda x: x[1], reverse=True)
