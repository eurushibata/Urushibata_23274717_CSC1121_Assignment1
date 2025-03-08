#!/usr/bin/python
from bs4 import BeautifulSoup
from search.stopwords import get_stop_words
import xmltodict
import json

class Indexation:
  def __init__(self, data):
    self.documents = data

  def tokenize(self, docno):
    for document in self.documents:
      if int(document['docno']) == int(docno):
        text = document['text']
        # Tokenize the text
        tokens = text.lower().split()
        return tokens

  def remove_stopwords(self, tokens):
    stop_words = get_stop_words()
    return [token for token in tokens if token not in stop_words]

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
  # json_data = json.dumps(xml_dict, indent=2)

  # Bs_data = BeautifulSoup(data, "xml")
  # titles = Bs_data.find_all('title')
  # texts = Bs_data.find_all('text')

  # print(Bs_data)
  # print(xml_dict['root'])




  inverted_index = Indexation(xml_dict['root']['doc'])
  tokens = inverted_index.tokenize(1)
  tokensWOStopWords = inverted_index.remove_stopwords(tokens)
  print(f'Tokens({len(tokens)}): ({tokens})')
  print(f'Tokens after stopwords({len(tokensWOStopWords)}): ({tokensWOStopWords})')
  





  # Using find() to extract attributes 
  # of the first instance of the tag
  # b_name = Bs_data.find('child', {'name':'Frank'})

  # print(b_name)

  # Extracting the data stored in a
  # specific attribute of the 
  # `child` tag
  # value = b_name.get('test')

  # print(value)


  # Steps:
  # 1. Text PRocessing - Tokenization, Stopword Removal, Stemming
  # 2. Vectorization - Count Vectorization, TF-IDF
  # 3. Model Building - KMeans, LDA, LSA
  # 4. Evaluation - Silhouette Score, Coherence Score
  # 5. Visualization - Word Cloud, LDAvis


  # for ranking VSM - Cosine Similarity