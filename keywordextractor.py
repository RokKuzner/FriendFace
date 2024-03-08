import yake

def extract_keywords(text:str):
    #Get the number of keywords to extract
    keywords_to_extract = int(len(text.split())*0.15)
    keywords_to_extract = 3 if keywords_to_extract < 3 else keywords_to_extract
    keywords_to_extract = 10 if keywords_to_extract > 10 else keywords_to_extract
    
    #Extract the keywords
    extractor = yake.KeywordExtractor(top=keywords_to_extract, stopwords=None)
    keywords = extractor.extract_keywords(text)

    #Return the keywords in an array
    out = []
    for keyword, score in keywords:
        out.append(keyword)
    return out