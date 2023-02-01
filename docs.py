from preprocessing import Prapengolahan
from collections import defaultdict


class Dokumen:
    def __init__(self):
        self.Development_Docs = "dataset/demofile.dataset"  # devdocs.dataset demofile.dataset
        self.Output_Docs = "dataset/doc_retr.dataset"
        self.pra = Prapengolahan()
        self.documents_dict = {}

    def documents_dictionary(self):
        file = open(self.Development_Docs, encoding="UTF-8")  # ISO-8859-1
        for line in file:
            doc = line.split("\t")
            terms = self.pra.tokenize_and_extract(doc[1])
            self.documents_dict[doc[0]] = terms
        file.close()

        return self.documents_dict

    def inverted_index(self):
        self.documents_dictionary()
        inverted_index = defaultdict(set)

        for docid, terms in self.documents_dict.items():
            for term in terms:
                inverted_index[term].add(docid)
        return inverted_index

    def document_retr(self):
        documents = {}
        file = open(self.Output_Docs, encoding="UTF-8")

        for line in file:
            doc = line.split("\t")
            text = [doc[1], doc[2]]
            documents[doc[0]] = text
        file.close()

        return documents
