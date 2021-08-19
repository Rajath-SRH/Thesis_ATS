from PIL import Image
import json
import pymongo
import json
from json import loads
from bson.objectid import ObjectId
from pymongo import MongoClient
import re
import nltk
nltk.download('punkt')



#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def main():
  pass


def extract_cv_corpus(session_id):
  client = pymongo.MongoClient("localhost", 27017)
  db = client.ATS
  cur = db.cv_struct.find({'session_id': session_id})
  for mainIndex, cv in enumerate(cur):
    for corpus in nltk.sent_tokenize(cv["all_text"]):
      for skill in cv["skills"]:
        if skill in corpus:
          data = {}
          data["skill"] = skill
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["cv_corpus"] = corpus
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          data["session_id"] = cv["session_id"]
          db.cv_corpus.insert_one(data)

      if cv["experience"] is not None:
        for experience in cv["experience"]:
          data = {}
          data["skill"] = None
          data["expericene"] = experience
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["cv_corpus"] = experience
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          data["session_id"] = cv["session_id"]
          db.cv_corpus.insert_one(data)
          
      if cv["degree"] is not None:
        for degree in cv["degree"]:
          data = {}
          data["skill"] = None
          data["expericene"] =  None
          data["degree"] = degree
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["cv_corpus"] = degree
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          data["session_id"] = cv["session_id"]
          db.cv_corpus.insert_one(data)

      if cv["designation"] is not None:
        for designation in cv["designation"]:
          data = {}
          data["skill"] = None
          data["expericene"] =  None
          data["degree"] = None
          data["designation"] = designation
          data["college_name"] = None
          data["company_names"] = None
          data["cv_corpus"] = designation
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          data["session_id"] = cv["session_id"]
          db.cv_corpus.insert_one(data)


      if cv["college_name"] is not None:
        for college_name in cv["college_name"]:
          data = {}
          data["skill"] = None
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = college_name
          data["company_names"] = None
          data["cv_corpus"] = college_name
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          db.cv_corpus.insert_one(data)


      if cv["company_names"] is not None:
        for company_names in cv["company_names"]:
          data = {}
          data["skill"] = None
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = company_names
          data["cv_corpus"] = company_names
          data["cv_mongo_object_id"] = cv['_id']
          data["file_name"] = cv['file_name']
          data["session_id"] = cv["session_id"]
          db.cv_corpus.insert_one(data)



if __name__ == "__main__":
  main()