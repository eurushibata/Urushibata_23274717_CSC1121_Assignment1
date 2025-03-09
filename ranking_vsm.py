# implement ranking vector space model using cosine similarity
from collection_indexer import CollectionIndexer
from datetime import datetime

class RankingVSM:
  def __init__(self, collection):
    self.collection = collection
    self.document_term_matrix = None

    start_time = datetime.now()
    print('STARTED: creating DOCUMENT-TERM matrix')
    self.document_term_matrix = collection.generate_document_term_matrix()
    print(f'FINISHED ({(datetime.now() - start_time).total_seconds()} seconds)')
    # print(self.document_term_matrix)

  # Create Vector Space Model
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866813
  # use the self.document_term_matrix to create the VSM
  def calculate_similarity(self, query):
    clean_query_tokens = self.collection.clean_tokens(query.split())
    # get the document-terms matrix
    terms_index =  self.document_term_matrix

    # to use the dot product, the query needs to follow same structure as the document_term_matrix
    # clone the document_term_matrix structure and reset the terms values to 0
    query_vector = {}
    for term in terms_index[1]:
      query_vector[term] = 0
    # print(query_vector)
  
    # now, update the query_document_term_matrix_instance with the query terms frequency
    # the tokens that are not known will be ignored
    for term in clean_query_tokens:
      if term in query_vector:
        query_vector[term] += 1
    # print(query_vector)

    # calculate the cosine similarity
    similarity_all_documents = {}
    for docno, document_term_matrix in terms_index.items():
      similarity_all_documents[docno] = self.cosine_similarity_per_document(query_vector, document_term_matrix)
    return similarity_all_documents
  
  def cosine_similarity_per_document(self, query_vector, document_term_matrix):
    dot_product = 0
    for term in document_term_matrix:
      dot_product += document_term_matrix[term] * query_vector[term]
    
    # Calculate the Euclidian norm of the document and query vectors
    magnitude_query = sum([value**2 for value in query_vector.values()])
    magnitude_document = sum([value**2 for value in document_term_matrix.values()])

    # calculate the cosine similarity
    if (magnitude_query * magnitude_document) == 0:
      similarity = 0
    else:
      similarity = dot_product / ((magnitude_query * magnitude_document) ** 0.5)
    return similarity
  
  def query(self, query):
    similarity = self.calculate_similarity(query)
    return similarity

  # Relevant Judgement
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866826
  def generate_relevance_judgement(self, similarity_object):
    # delete the similarity scores = 0
    relevance_judgement_rank = []
    for docno, score in similarity_object.items():
      if score > 0:
        relevance_judgement_rank.append({ docno: score })
    # sort the similarity scores (descending)
    relevance_judgement_rank.sort(key=lambda x: list(x.values())[0], reverse=True)
    # print(relevance_judgement_rank)
    return relevance_judgement_rank

if __name__ == "__main__":
  # for testing purpose, define the collection size
  # limit = 2 # any number or None
  limit = None
  collection = CollectionIndexer('./cranfield-trec-dataset/cran.all.1400.xml', limit)
  ranking_vsb = RankingVSM(collection)

  similarity = ranking_vsb.query('what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .')
  relevance_judgement = ranking_vsb.generate_relevance_judgement(similarity)
  print(relevance_judgement)