#!/usr/bin/env python3
import argparse
from simple_term_menu import TerminalMenu
from corpus_indexer import CorpusIndexer
from topic_reader import ReadTopics
from ranking_vsm import RankingVSM
from ranking_bm25 import RankingBM25
# def main():
#     options = [
#        "Vector Space Model",
#        "entry 2",
#        "entry 3"]
#     terminal_menu = TerminalMenu(options)
#     menu_entry_index = terminal_menu.show()
#     print(f"You have selected {options[menu_entry_index]}!")

#     if (menu_entry_index == 0):
        # print("Vector Space Model")

def execute(ranking_algorithm, query_filepath, output_filename):
  collection = CorpusIndexer('./cranfield-trec-dataset/cran.all.1400.xml')
  algo = None
  if (ranking_algorithm == "vsm"):
    print("Vector Space Model")
    algo = RankingVSM(collection)
  if (ranking_algorithm == "vsm_q"):
    print("Vector Space Model")
    algo = RankingVSM(collection)
  elif (ranking_algorithm == "bm25"):
    print("BM25")
    algo = RankingBM25(collection)

  topics = ReadTopics(query_filepath)

  results = []
  for topic in topics.get_topics():
    print(topic["num"])
    print(topic["title"])
    
    # get the top 100 documents for each topic
    ranking_algo_result = algo.query(topic["title"])[:100]

    for rank, result in enumerate(ranking_algo_result, start=1):
      docid = list(result.keys())[0]
      score = list(result.values())[0]
      results.append(format_output(topic["num"], "Q0", docid, rank, score, "myrun"))
  
  # res = algo.query('experimental investigation of the aerodynamics of a wing in a slipstream .')
  # print(res)

  # write to file
  f = open(output_filename, "w")
  for result in results:
    f.write(result)
    f.write("\n")
  f.close()

def format_output(num, q0, docid, rank, score, system):
  return f"{num} {q0} {docid} {rank} {score} {system}"

if __name__ == "__main__":
  parser=argparse.ArgumentParser(description="sample argument parser")
  parser.add_argument("ranking_algorithm", help="Ranking algorithm", nargs="?", choices=["vsm", "vsm_q", "bm25"])
  parser.add_argument("query_filepath", help="Query (topics) filepath", nargs="?")
  parser.add_argument("output_filename", help="Output file (e.g. myrun.res)", nargs="?")

  args=parser.parse_args()

  print(args.ranking_algorithm)
  print(args.query_filepath)
  print(args.output_filename)

  print("===================================================")
  print("Information Retrieval")
  print("===================================================")
  print("Author: Emerson Takeshi Urushibata")

  execute(args.ranking_algorithm, args.query_filepath, args.output_filename)
  # print("Select the Information Retrieval ranking algorithm:")
  
  # if (args.ranking_algorithm == None):
  #   main()


  # output
#   predictions (dict): a single retrieval run.
# query (int): Query ID.
# q0 (str): Literal "q0".
# docid (str): Document ID.
# rank (int): Rank of document.
# score (float): Score of document.
# system (str): Tag for current run.