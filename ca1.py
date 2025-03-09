#!/usr/bin/python
from bs4 import BeautifulSoup
from search.stopwords import get_stop_words, escape_sequence
import xmltodict
import json

class Indexation:

  # The documents structures are:
  # {
  #   'docno': '1',
  #   'title': 'experimental investigation of the aerodynamics of a wing in a slipstream .',
  #   'author': 'brenckman,m.',
  #   'bibliography': 'j. ae. scs. 25, 1958, 324.',
  #   'text': 'experimental investigation of the aerodynamics of a wing in a slipstream .'
  # }
  def __init__(self, data):
    self.documents = data
    # print(self.documents[0])
    print(f'Number of documents entered: {len(self.documents)}')

    #  tokenize the text of a document given its docno
    for document in self.documents:
      tokens = self.tokenizeOneDocByDocno(document['docno'])
      tokensWOStopWords = self.remove_stopwords(tokens)
      # print(f'Docno: {document["docno"]}')
      # print(f'Tokens({len(tokens)}): ({tokens})')
      # print(f'Tokens after stopwords({len(tokensWOStopWords)}): ({tokensWOStopWords})')
      document['tokens'] = tokens
      document['tokensWOStopWords'] = tokensWOStopWords

  def tokenizeOneDocByDocno(self, docno):
    for document in self.documents:
      if int(document['docno']) == int(docno):
        #  TODO: shoudl we use the title also? it seems that titles are included on the text.
        text = document['text']
        # Remove escape sequences
        if (text is None):
          return []
        for escape in escape_sequence():
          text = text.replace(escape, " ")

        # Tokenize the text by splitting by spaces
        tokens = text.lower().split()
        return tokens

  def remove_stopwords(self, tokens):
    stop_words = get_stop_words()
    return [token for token in tokens if token not in stop_words]

  def create_inverted_index(self):
    inverted_index = {}
    for document in self.documents:
      tokens = document['tokensWOStopWords']
      for i, token in enumerate(tokens):
        if token in inverted_index:
          inverted_index[token].append(document['docno'])
        else:
          inverted_index[token] = [document['docno']]
    return inverted_index
  
  def create_term_frequency(self):
    term_frequency = {}
    inverted_index = self.create_inverted_index()
    for token, docnos in inverted_index.items():
      term_frequency[token] = len(docnos)
    return term_frequency


    

if __name__ == "__main__":
  file_path = './cranfield-trec-dataset/cran.all.1400.xml'
  with open(file_path, 'r') as f:
    data = f.read()

  # Wrap the data in a root tag since it isn't a XML data structure without a root element
  data = f"<root>{data}</root>"

  # Parse the XML data
  xml_dict = xmltodict.parse(data)
  json_data = json.dumps(xml_dict, indent=2)
  parsed_json = json.loads(json_data)



  docs = Indexation(xml_dict['root']['doc'])
  tokens = docs.tokenizeOneDocByDocno(1)
  tokensWOStopWords = docs.remove_stopwords(tokens)
  # print(f'Tokens({len(tokens)}): ({tokens})')
  # print(f'Tokens after stopwords({len(tokensWOStopWords)}): ({tokensWOStopWords})')

  index = docs.create_inverted_index()
  print(f'Inverted Index: {index}')
  
  print(f'Term Frequency: {docs.create_term_frequency()}')


  # Steps:
  # 1. Text Processing - Tokenization, Stopword Removal, Stemming
  # 2. Vectorization - Count Vectorization, TF-IDF
  # 3. Model Building - KMeans, LDA, LSA
  # 4. Evaluation - Silhouette Score, Coherence Score
  # 5. Visualization - Word Cloud, LDAvis


  # for ranking VSM - Cosine Similarity

# FROM https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866817
# The Inverted Index

# The idea behind an inverted index is very similar to the index at the end of a book:
# it provides a list of words or phrases with pointers to the pages in the book where those can be found.

# An inverted index is a data structure consisting of two parts:

# 1. The dictionary (or vocabulary), or list of index terms, contains the list of features, like terms, n-grams,
# phrases, named entities, etc., extracted from the text and which are used to represent the documents.
# 2. Associated with each inverted term, there is an inverted (or posting) list, that contains the information to be
# stored with the index term. Each cell in the inverted list is called a posting. The posting list contains
# information about the position of the index term in the collection, such as the reference to the
# document (equivalent to the page for a book). The document is normally identified by a unique serial number (docID).