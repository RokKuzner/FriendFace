import yake

extractor = yake.KeywordExtractor(top=10, stopwords=None)

def extract_keywords(text:str):
    keywords = extractor.extract_keywords(text)

    out = []
    for keyword, score in keywords:
        out.append(keyword)
    return out