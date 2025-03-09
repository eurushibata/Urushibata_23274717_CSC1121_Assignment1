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


if __name__ == "__main__":
  collection = CollectionIndexer('./cranfield-trec-dataset/cran.all.1400.xml')
  ranking_vsb = RankingVSM(collection)

  # print(ranking_vsb.create_vsm())
  
  # print(collection.generate_term_document_matrix())