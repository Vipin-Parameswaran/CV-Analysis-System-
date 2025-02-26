# Project Name: LLM Text Analysis Application

## Objective

This project aims to provide a web-based solution for extracting and analyzing text from various document formats (PDF, DOCX, and images). By leveraging OpenAI's LLM models, the application allows users to upload documents and images for text extraction, which is then analyzed to provide meaningful insights.

The application offers the following features:

File Upload: Users can upload files (PDF, DOCX, or image formats) for text extraction.
Text Extraction: The uploaded files are processed using specialized extraction methods for each file type (PDF, DOCX, or OCR for images).
LLM Analysis: The extracted text is sent to OpenAI’s LLM models for analysis and response generation.
Key benefits include seamless integration with multiple document formats, real-time text extraction, and detailed analysis powered by OpenAI. The tool can be used for various purposes such as document analysis, content extraction, and data processing.

## Overview

This project is a web-based application built using Flask that integrates with OpenAI's GPT-3.5 models to perform advanced text analysis on various document formats (e.g., PDF, DOCX, and images). It utilizes OCR techniques for information extraction and analysis through an API endpoint. Users can upload documents (PDF/DOCX), and the system processes the content, extracting key information and providing meaningful insights.

---

## Prerequisites

Before running the application, ensure that you have the following installed on your local machine:

- Python 3.6 or later
- pip (Python package installer)

You will also need the following libraries and tools:

- Flask: For building the web application
- OpenAI: To interact with OpenAI's API
- pdfplumber: For extracting text from PDFs
- python-docx: To handle DOCX file extraction
- pytesseract: For OCR (Optical Character Recognition) from images
- PyMuPDF: For handling images within PDF files
- spacy: Natural Language Processing (NLP) tasks
- pdfminer.six: Another PDF text extraction tool

---

## Installation

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/yourusername/LLM-Text-Analysis.git
   cd LLM-Text-Analysis

2. Install the required dependencies using requirements.txt.

   ```bash
   pip install -r requirements.txt

3. Set up environment variables for OpenAI API key by creating a .env file in the root of your project directory.

   ```bash
   OPENAI_API_KEY=your_openai_api_key  

## Workflow

#### 1. User Upload:
The user uploads a PDF, DOCX, or image file via a Flask endpoint.

#### 2. Text Extraction:
Depending on the file type, the application uses different libraries for text extraction:
pdfplumber and pdfminer.six are used for PDFs.
python-docx is used for DOCX files.
pytesseract is used for extracting text from images (using OCR).

#### 3. Text Preprocessing:
The extracted text is cleaned and preprocessed (removing unwanted characters, handling formatting issues, etc.).
Key Information Extraction:
Key pieces of information are extracted using natural language processing (NLP) techniques with the help of spacy.

#### 4.LLM Analysis:
The preprocessed text and extracted information are sent to OpenAI's GPT model for further analysis using the openai.ChatCompletion API.

#### 5.Response:
The application processes the results from OpenAI and sends back meaningful insights to the user, such as summarized content, key findings, or specific data extractions.

## app.py Explanation
#### 1. Imports:
The required libraries are imported, such as Flask, openai, spacy, and others for text extraction and NLP.

#### 2. Flask Application:
A Flask web application is set up with routes to handle HTTP requests.
   
   ```python
   app = Flask(__name__)
   ```


#### 3. File Upload Route:
A route is created to accept file uploads. This route processes the uploaded file and extracts the text.

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    # File extraction logic
```

#### 4. Text Extraction Functions:
Different functions (e.g., extract_text_from_pdf, extract_text_from_docx) handle specific formats and extract text.

```python
def extract_text_from_pdf(file_path):
    # PDF text extraction logic
```

#### 5. LLM Prompt Creation:
A function (create_llm_prompt) is responsible for creating a structured prompt to send to OpenAI's GPT model.

```python
def create_llm_prompt(text):
    # Creating prompt for LLM analysis
```

#### 6. LLM Analysis:
The analyze_with_llm function interacts with OpenAI's API to process the text and retrieve analysis.

```python
def analyze_with_llm(text):
    # LLM analysis logic
```

#### 7. Flask Route for Text Analysis:
A route (/analyze) processes the extracted text, calls the LLM function, and returns the results to the user.

```python
@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Handling analysis logic
```

#### 8. Running the Application:
The app.run() method starts the Flask development server.

```python
if __name__ == '__main__':
    app.run(debug=True)
```

## How to Run the Application

#### Set up your environment:

Make sure that your virtual environment is activated and that all dependencies are installed.
Run the Flask Application:

Open a PowerShell or terminal window, navigate to your project directory, and run the following command:


```console
python app.py

```

This will start the Flask development server.
Access the Application:

Open your browser and go to http://127.0.0.1:5000.
You can now interact with the application through the endpoints.

## PowerShell Command for Running the App

To run the Flask application in PowerShell:

Open PowerShell in your project directory.

Run the following command to activate your virtual environment (if not already activated):


```console
.\venv\Scripts\Activate
```

Then, run the Flask app:

```console
python app.py

```
The Flask server should now be running, and you can interact with it via the specified routes.

## API Endpoints
#### /upload (POST): Upload a PDF, DOCX, or image file for text extraction.
#### /analyze (POST): Analyze the extracted text using the LLM model.

## Error Handling
If there are any issues during the execution (e.g., invalid file format, API errors), appropriate error messages will be returned to the user. For example, if OpenAI's API rate limit is exceeded, the user will be notified.

## Notes
Make sure to have the necessary .env file with the correct OpenAI API key.
The application works with various document formats, and the OCR functionality can handle image files with text.