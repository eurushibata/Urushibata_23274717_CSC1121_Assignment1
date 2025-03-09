# implement BM25 algorithm
from corpus_indexer import CorpusIndexer
import numpy as np
import math

class RankingBM25:
  def __init__(self, collection):
    self.collection = collection

    sum_of_length_of_clean_tokens = 0
    for doc in self.collection.documents:
      sum_of_length_of_clean_tokens += len(doc['clean_tokens'])

    # average document length (after tokens cleaning)
    self.avgdl = sum_of_length_of_clean_tokens / len(self.collection.documents)

  def query(self, query):
    clean_query_tokens = self.collection.clean_tokens(query.split())
       
    bm25_array = {}
    for doc in self.collection.documents:
      total_score = sum(self.calculate_bm25(doc['clean_tokens'], query_token) for query_token in clean_query_tokens)
      bm25_array[doc['docno']] = total_score
    return bm25_array
  
  #  Calculate Probability Estimation
  # https://www.futurelearn.com/courses/mechanics-of-search-text-and-web-retrieval/4/steps/1866845
  def calculate_bm25(self, document_term_vector, word, k=1.25, b=0.75):
    N = len(self.collection.documents)
    n = sum(doc['clean_tokens'].count(word) for doc in self.collection.documents)
    avgdl = self.avgdl
    tf = document_term_vector.count(word)

    idf = math.log(((N - n + 0.5) / (n + 0.5)) + 1)
    
    return round(tf/(tf + k*(1-b)+b*(N/avgdl)) * idf, 4)

if __name__ == "__main__":
  # for testing purpose, define the collection size
  # limit = 1000 # any number or None
  limit = None
  collection = CorpusIndexer('./cranfield-trec-dataset/cran.all.1400.xml', limit)
  ranking_bm25 = RankingBM25(collection)


  res = ranking_bm25.query('can a criterion be developed to show empirically the validity of flow solutions for chemically reacting gas mixtures based on the simplifying assumption of instantaneous local chemical equilibrium .')
  print(res)
  # relevance_judgement = ranking_vsb.generate_relevance_judgement(similarity)
  # print(relevance_judgement)


# https://www.youtube.com/watch?v=ziiF1eFM3_4&t=1s
  # 1.2 < k1 < 2   => 1.25
  # 0.5 < b < 0.8 => 0.75

