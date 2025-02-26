import openai
import json
import sqlite3
import os
import spacy
from flask import Flask, request, jsonify
from extract_key_information import extract_key_info
from extract_text import extract_text_from_pdf, extract_text_from_docx
from llm_prompt import create_llm_prompt, analyze_with_llm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hardcoded OpenAI API Key
OPENAI_API_KEY = "sk-proj-***************" # replace it with your api key

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('cv_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      email TEXT,
                      phone TEXT,
                      education TEXT,
                      experience TEXT,
                      skills TEXT,
                      projects TEXT,
                      certifications TEXT
                    )''')
    conn.commit()
    conn.close()

init_db()


# Store CV data in DB
def store_cv_data(data):
    conn = sqlite3.connect('cv_data.db')
    cursor = conn.cursor()

    # Ensure all values are stored as strings
    cursor.execute("""
        INSERT INTO candidates (name, email, phone, education, experience, skills, projects, certifications) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(data.get("Name", "Not Found")),
        str(data.get("Email", "Not Found")),
        str(data.get("Phone", "Not Found")),
        str(data.get("Education", "Not Found")),
        str(data.get("Work Experience", "Not Found")),
        str(", ".join(data["Skills"]) if isinstance(data.get("Skills"), list) else str(data.get("Skills", "Not Found"))),
        str(", ".join(data["Projects"]) if isinstance(data.get("Projects"), list) else str(data.get("Projects", "Not Found"))),
        str(", ".join(data["Certifications"]) if isinstance(data.get("Certifications"), list) else str(data.get("Certifications", "Not Found")))
    ))

    conn.commit()
    conn.close()


# Upload and process file endpoint
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    file_path = os.path.join("uploads", filename)
    file.save(file_path)

    # Extract text based on file type
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    # Extract key information
    extracted_info = extract_key_info(text)
    
    # Create LLM prompt and analyze
    prompt = create_llm_prompt(extracted_info)
    analysis = analyze_with_llm(prompt)
    extracted_info["Analysis"] = analysis
    
    # Store data in DB
    store_cv_data(extracted_info)
    
    return jsonify(extracted_info)

# Query System
@app.route("/query", methods=["POST"])
def query_cv_db():
    data = request.json
    conn = sqlite3.connect('cv_data.db')
    cursor = conn.cursor()
    
    if "skills" in data:
        cursor.execute("SELECT name, email FROM candidates WHERE skills LIKE ?", (f"%{data['skills']}%",))
    elif "education" in data:
        cursor.execute("SELECT name, email, education FROM candidates ORDER BY education DESC")
    elif "experience" in data:
        cursor.execute("SELECT name, email, experience FROM candidates WHERE experience LIKE ?", (f"%{data['experience']}%",))
    elif "certifications" in data:
        cursor.execute("SELECT name, email, certifications FROM candidates WHERE certifications LIKE ?", (f"%{data['certifications']}%",))
    else:
        return jsonify({"message": "Invalid query."})
    
    results = cursor.fetchall()
    conn.close()
    return jsonify({"candidates": results})

if __name__ == "__main__":
    app.run(debug=True)
