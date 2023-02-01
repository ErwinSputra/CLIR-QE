from nltk.tokenize import word_tokenize
import re
import nltk


class Prapengolahan:
    def __init__(self):
        self.tokenizer = word_tokenize
        self.stopwords = set(nltk.corpus.stopwords.words("english"))
        self.lemma = nltk.wordnet.WordNetLemmatizer()

    def tokenize_and_extract(self, doc):
        doc = doc.lower()
        tokenize = [token for token in self.tokenizer(doc)]

        terms = []
        self.stopwords.add('self')
        for token in tokenize:
            if token not in self.stopwords:
                # jika token bukan angka dan bukan selain huruf A-Z sama dengan
                # jika token hanya mengandung huruf A-Z, selain itu not accept
                if not re.search(r'\d', token) and not re.search(r'[^A-Za-z-]', token):
                    lem = self.lemma.lemmatize(token)
                    terms.append(lem)
        return terms
