# implement BM25 algorithm
from corpus_indexer import CorpusIndexer
import math

class RankingBM25:
  def __init__(self, collection):
    self.collection = collection

    sum_of_length_of_clean_tokens = 0
    for doc in self.collection.documents:
      sum_of_length_of_clean_tokens += len(doc['clean_tokens'])

    # average document length (after tokens cleaning)
    self.avgdl = sum_of_length_of_clean_tokens / len(self.collection.documents)

    # start_time = datetime.now()
    # print('STARTED: creating DOCUMENT-TERM matrix')
    # self.document_term_matrix = collection.generate_document_term_matrix()
    # print(f'FINISHED ({(datetime.now() - start_time).total_seconds()} seconds)')
    # print(self.document_term_matrix)

  # implement the BM25 algorithm
  def calculate_similarity(self):
    # calculate the BM25
    similarity_all_documents = {}
    for docno, document_term_vector in self.document_term_matrix.items():
      similarity_all_documents[docno] = self.bm25_per_document(document_term_vector)
    return similarity_all_documents
  
  def probability_estimation (self, query):
    # Approximating the non relevant documents R = r = 0 => Total of documents in collection
    N = len(self.collection.documents)

    weights = {}
    for term in query:
      # if query term doesn't exist in the collection, skip
      if (term not in self.collection.generate_terms_index()):
        continue

      # calculate the weight for each term in the query
      n = self.collection.generate_terms_index()[term]
      n = len(list(set(n))) # make frequency unique = number of documents containing the term
      # https://www.futurelearn.com/courses/mechanics-of-search-text-and-web-retrieval/4/steps/1866845
      # Robertson and Sparck Jones weighting
      weights[term] = math.log((0.5*(N - n + 0.5))/((n + 0.5)*0.5))
    return weights
  
  def query(self, query):
    clean_query_tokens = self.collection.clean_tokens(query.split())
    weights = self.probability_estimation(clean_query_tokens)

    # w_rsj ranking
    similarity_all_documents = {}
    for docno, document_term_vector in self.collection.generate_document_term_matrix().items():
      similarity_all_documents[docno] = 0
      for term, value in weights.items():
        if document_term_vector[term] != 0:
          similarity_all_documents[docno] += value
      
    # sort the similarity descending
    similarity_all_documents = dict(sorted(similarity_all_documents.items(), key=lambda item: item[1], reverse=True))
    return similarity_all_documents
  

  def bm25_per_document(self, query, document, k=1.2, b=0.75):
    
    # how to calculate frequencey of query in the document?


      # def bm25_per_document(self, document_term_matrix):
    # w_bm25 = tf/(K1*((1-b) + b*dl/av dl) +t*f)*w_rsj()

    pass



if __name__ == "__main__":
  # for testing purpose, define the collection size
  limit = 1000 # any number or None
  # limit = None
  collection = CorpusIndexer('./cranfield-trec-dataset/cran.all.1400.xml', limit)
  ranking_bm25 = RankingBM25(collection)

  # similarity = ranking_bm25.query('can a criterion be developed to show empirically the validity of flow solutions for chemically reacting gas mixtures based on the simplifying assumption of instantaneous local chemical equilibrium .')
  # print(similarity)
  # relevance_judgement = ranking_vsb.generate_relevance_judgement(similarity)
  # print(relevance_judgement)


# https://www.youtube.com/watch?v=ziiF1eFM3_4&t=1s
  # 1.2 < k1 < 2   => 1.25
  # 0.5 < b < 0.8 => 0.75

