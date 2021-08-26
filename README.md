# Application Tracking system using Neural Networks

![Pipeline](PIPELINE.png)

 ## Introduction
Any talent acquisition team faces the problem of dealing with an avalanche of applications whenever a new job opening arises. Only matching keywords and phrases automates some portions of the present application tracking system. As a result, resumes are ranked in a skewed manner, and the most worthy individual is not hired. This ATS applications ensures the most decerving candidates are shortlisted for the given position by using state-of-the-art neural network systems.

## Pipeline
The general flow of the pipeline is depicted in the flowchart above and is explained below : 
* A simple HTML form which takes as input the job description (JD) and Resumes (CVs). You can provide as many CVs for a particular position. (Accepted input : docx, pdf, img/jpg)
* The inputs from the user is then passed to an OCR(optical character recognition) system that captures the text from images. A resume parser is used to convert the text to structues Json data that captures the necessary fields from both JD and CV.
* The JSON record is then stored using MongoDB and then later accessed to create sentence pairs based on skills, experience etc.
* The sentence pairs are then cleaned using text processing and are passed to the transformers based models which encode the sentence pairs. The user interface allows the user to select from the available models.
* The sentence pairs are then evaluated using cosine similarity that captures how close or similar the two sentence are.
* Simultaneously, the knowledge graph captures the hierarchy of skills between the two sentences and gives it a score.
* The scores from the knowledge graph and the models are then aggregated and evaluated to get the best candidate for the given job description.
* The results are then displayed to the user for selection.

## Getting Started
#### Prerequisites
* Install MongoDB client and start the service locally. Go to MongoDB install directory -> bin -> Run mongo and mongod in two differnt terminals. 
* Install all the python dependencies from requirements.txt pip install -r requirements.txt

### Replicate the application in your local system
* Clone the repository to a directory in your local file system.
* Perform the prerequiste steps above. Install mongodb compass to get insights on the application data push to mongoDB.
* Run app.py. This will open a simple html form to input the JD and CVs. The application will take time to compute and display the scores.

# Thesis Created by
**Rajath Suresh Babu**
##### Email : rajathsuresh9@gmail.com

# Thesis Supervisors
**Prof. Dr. Ajinkya Prabhune** and
**Mr. Ashish Chouhan**

