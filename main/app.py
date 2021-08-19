import os
import pytesseract as tess
import pymongo
from pymongo import MongoClient
from PIL import Image
from os.path import isfile, join
import json
from pyresparser import ResumeParser
import io
import PyPDF2
import extract_jd_corpus
import extract_cv_corpus
import mpnet
import uuid
import distilrobert
import albert
import tinybert
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



# def main():
#   pass

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'C:/Users/Rajath/Desktop/Thesis/Pipeline/Data/JD'
UPLOAD_FOLDER_jd = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER_jd'] = UPLOAD_FOLDER_jd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'C:/Users/Rajath/Desktop/Thesis/Pipeline/Data/CV'
UPLOAD_FOLDER_cv = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER_cv'] = UPLOAD_FOLDER_cv


@app.route('/', methods=['POST'])
def upload_file():

    uploaded_JD = request.files.getlist('JD')
    for file in uploaded_JD:
      file.save(os.path.join(app.config['UPLOAD_FOLDER_jd'],file.filename))
      
    uploaded_CV = request.files.getlist('CV')
    for file in uploaded_CV:
      file.save(os.path.join(app.config['UPLOAD_FOLDER_cv'],file.filename))

    jd = "C:/Users/Rajath/Desktop/Thesis/Pipeline/Data/JD/"
    cv = "C:/Users/Rajath/Desktop/Thesis/Pipeline/Data/CV/"
    
   
    res = []

      #read cv
    for filename in os.listdir(cv):
        if filename.endswith(".jpeg") or filename.endswith(".jpg"):
          img = Image.open(cv + filename)
          text = tess.image_to_string(img)
          text_lower = text.lower()
          tx = " ".join(text_lower.split('\n'))#split at space?
          # print(tx)
          #local_collection_cv.insert_one({"file_name": filename, "text": tx})
        elif filename.endswith(".pdf") or filename.endswith(".docx"):

            #for structured data for training data model
            pdf_cv = ResumeParser(str(cv) + "/" + str(filename)).get_extracted_data()
            pdff = open(str(cv) + "/" + str(filename), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdff)
            page = pdfReader.getPage(0)
            Content = page.extractText()
            
            session_id = uuid.uuid4().hex[:8]

            pdf_cv["session_id"] = session_id
            pdf_cv["file_name"] = filename
            pdf_cv["all_text"] = Content
            pdf_cv["doc_type"] = "cv"
            client = pymongo.MongoClient("localhost", 27017)
            db = client.ATS
            db.cv_struct.insert_one(pdf_cv)
            extract_cv_corpus.extract_cv_corpus(session_id)

            for filename in os.listdir(jd):
              if filename.endswith(".png"):
                img = Image.open(str(jd) + "/" + str(filename))
                text = tess.image_to_string(img)
                # print(text, "lolwa")
                pdf_data = ResumeParser(str(jd) + "/" + str(filename)).get_extracted_data()
                  
              elif filename.endswith(".pdf") or filename.endswith(".docx"):
                  pdf_data = ResumeParser(str(jd) + "/" + str(filename)).get_extracted_data()
                  pdff = open(str(jd) + "/" + str(filename), 'rb')
                  pdfReader = PyPDF2.PdfFileReader(pdff)
                  page = pdfReader.getPage(0)
                    
                  Content = page.extractText()
                  pdf_data["session_id"] = session_id
                  pdf_data["file_name"] = filename
                  pdf_data["all_text"] = Content
                  pdf_data["doc_type"] = "jd"
                  client = pymongo.MongoClient("localhost", 27017)
                  db = client.ATS
                  db.jd_struct.insert_one(pdf_data)
                  extract_jd_corpus.extract_jd_corpus(session_id)


            #get results for mpnet
            if request.form.get("models") == "mpnet":
              

              result = mpnet.final_result(session_id)
              res.append(result)
              print("MPNET Sentence transformer: ", result) 
              
              print(".\n")
              print(".\n")
              print(".\n")
              


            #get results for distilrobert
            if request.form.get("models") == "distilrobert":
              result = distilrobert.final_result(session_id)
              res.append(result)
              print("DistilBert Sentence transformer: ", result)
              print(".\n")
              print(".\n")
              print(".\n")
              

            if request.form.get("models") == "albert":
              result = albert.final_result(session_id)
              res.append(result)
              print("Albert Sentence transformer: ", result)
              print(".\n")
              print(".\n")
              print(".\n")

            if request.form.get("models") == "tinybert":
              result = tinybert.final_result(session_id)
              res.append(result)
              print("TinyBERT Sentence transformer: ", result)
              print(".\n")
              print(".\n")
              print(".\n")
            
    return render_template('index.html', score = res)

            
if __name__ == '__main__':
   app.run(debug = True)