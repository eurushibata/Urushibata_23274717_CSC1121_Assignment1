#!/usr/bin/python
import xmltodict
import json

class ReadTopics:
  # limit_topic is used to limit the number of topics to be read
  def __init__(self, file_path, limit_topics=None):
    self.topics = []
    with open(file_path, 'r') as f:
      data = f.read()

    # Parse the XML data
    xml_dict = xmltodict.parse(data)
    json_data = json.dumps(xml_dict, indent=2)
    # Parse the JSON data
    self.topics = json.loads(json_data)['xml']['top']

    if (limit_topics is not None):
      self.topics = self.topics[:limit_topics]

    print(f'Total topics loaded: {len(self.topics)}')
  
  def get_topics(self):
    return self.topics

if __name__ == "__main__":
  a = ReadTopics('./cranfield-trec-dataset/cran.qry.xml')
  print(a.get_topics())