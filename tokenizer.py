from hazm import Normalizer, word_tokenize, Stemmer, Lemmatizer


class Tokenizer:
    @classmethod
    def normalize(cls, data):
        normalize_data = Normalizer().normalize(data)
        normalize_data = Normalizer().affix_spacing(normalize_data)
        normalize_data = Normalizer().character_refinement(normalize_data)
        normalize_data = Normalizer().punctuation_spacing(normalize_data)
        return normalize_data

    @classmethod
    def tokenize(cls, date):
        return word_tokenize(date)

    @classmethod
    def is_punc(cls, term):
        punctuations = """!()-[]{};:'",<>.،/?@#$%^&*_~\\"""
        return term if term not in punctuations else None

    @classmethod
    def find_tf(cls, data):
        results = []
        for term in list(set(data)):
            results.append({'term': term, 'tf': data.count(term)})
        return results

    def execute(self, data):
        results = []
        terms = self.tokenize(data)
        for term in terms:
            if self.is_punc(term):
                results.append(self.normalize(term))
        results = self.find_tf(results)
        return results


tokenize = Tokenizer()
