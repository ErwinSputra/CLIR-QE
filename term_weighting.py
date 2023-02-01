from docs import Dokumen
import math
from collections import defaultdict


class PembobotanKata:
    def __init__(self):
        self.docs = Dokumen().documents_dictionary()
        self.N = len(self.docs)
        self.avg_len = sum([len(doc) for doc in self.docs.values()])/len(self.docs)
        self.inv_idx = Dokumen().inverted_index()

    def tf_idf_query(self, q_terms):
        fqt = {}
        for term in q_terms:
            fqt[term] = fqt.get(term, 0) + 1
        tf_idf_query = {}
        id = 1
        for term in fqt.keys():
            query_tf = math.log10(fqt[term]) + 1
            print(f'{id}. {term}')
            df = len(self.inv_idx[term])
            print(f'df = {df}')
            if df != 0:
                query_idf = math.log(self.N / df)
                id += 1
                tf_idf_query[term] = query_tf * query_idf
        return tf_idf_query

    def tf_idf_doc(self, term, docID):
        td = self.docs[docID].count(term)
        df = len(self.inv_idx[term])  # df is the number of documents a term occurs in
        tf = math.log10(td) + 1  # the frequency of the word t in document d
        idf = math.log(self.N/df)
        w = tf * idf
        return w

    def create_tf_idf(self):
        tf_idf = defaultdict(dict)
        for term in set(self.inv_idx.keys()):
            for docid in self.inv_idx[term]:
                tf_idf[term][docid] = self.tf_idf_doc(term, docid)
        return tf_idf
