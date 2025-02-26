import re
import spacy
from pdfminer.high_level import extract_text
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

# Function to extract key details using Regex & NLP
def extract_key_info(text):
    info = {}

    # Extract Name (First detected PERSON entity)
    doc = nlp(text)
    name = ''
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            info["Name"] = name
            break
    # Initialize the spaCy Matcher
    matcher = Matcher(nlp.vocab)

    # Define patterns for extracting skills and certifications
    skill_patterns = [
        [{"lower": "python"}],
        [{"lower": "java"}],
        [{"lower": "c++"}],
        [{"lower": "sql"}],
        [{"lower": "machine learning"}],
        [{"lower": "deep learning"}],
        [{"lower": "data analysis"}],
        [{"lower": "artificial intelligence"}],
        # Add more skills as needed
    ]

    cert_patterns = [
        [{"lower": "certification"}],
        [{"lower": "training"}],
        [{"lower": "license"}],
        [{"lower": "certified"}],
        # Add more certification keywords
    ]

    matcher.add("SKILLS", skill_patterns)
    matcher.add("CERTIFICATIONS", cert_patterns)

    # Apply spaCy NLP processing
    doc = nlp(text)

    # Extract Name
    if not name:
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) > 1:  # Ensuring it's a full name
                info["Name"] = ent.text
                break

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    info["Email"] = email_match.group(0) if email_match else "Not Found"
    if info["Email"] == "Not Found":
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        info["Email"] = email_match.group(0) if email_match else "Not Found"

    # Extract Phone Number
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{1,4}\)?[-.\s]?)?[\d]{2,4}[-.\s]?\d{2,4}[-.\s]?\d{4}", text)
    info["Phone"] = phone_match.group(0) if phone_match else "Not Found"

    # Extract Organizations
    info["Organizations"] = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    info["Organizations"] = ", ".join(info["Organizations"]) if info["Organizations"] else "Not Found"

    # Match for skills and certifications
    skill_matches = matcher(doc)
    skills_found = set()
    certifications_found = set()

    for match_id, start, end in skill_matches:
        span = doc[start:end]
        if matcher.vocab.strings[match_id] == "SKILLS":
            skills_found.add(span.text)
        elif matcher.vocab.strings[match_id] == "CERTIFICATIONS":
            certifications_found.add(span.text)

    info["Skills"] = ", ".join(skills_found) if skills_found else "Not Found"
    info["Certifications"] = ", ".join(certifications_found) if certifications_found else "Not Found"

    # Extract sections using regex for Education, Work Experience, Projects
    sections = {
        "Education": r"(?:EDUCATION|Academic Background|Qualifications)[\s\S]*?(?=\n\n|$)",
        "Work Experience": r"(?:EXPERIENCE|Employment History|Professional Experience)[\s\S]*?(?=\n\n|$)",
        "Projects": r"(?:PERSONAL PROJECTS|Portfolio|Notable Work|Research Projects)[\s\S]*?(?=\n\n|$)"
    }

    for section, pattern in sections.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_section = match.group(0).strip().split("\n")[1:]  # Remove heading
            extracted_section = [line.strip() for line in extracted_section if line.strip()]
            info[section] = "\n".join(extracted_section) if extracted_section else "Not Found"
        else:
            info[section] = "Not Found"

    # Additional Education extraction using keywords
    if info["Education"] == "Not Found":
        education_keywords = ["Bachelors", "Masters", "PhD", "University", "Degree", "College", "EDUCATION", "Academic Background", "Qualifications"]
        education = [line.strip() for line in text.split("\n") if any(kw in line for kw in education_keywords)]
        info["Education"] = education if education else "Not Found"

    # Additional Work Experience extraction using keywords
    if info["Work Experience"] == "Not Found":
        experience_keywords = ["Experience", "Internship", "Worked", "Role", "Responsibilities"]
        work_exp = [line.strip() for line in text.split("\n") if any(kw in line for kw in experience_keywords)]
        info["Work Experience"] = work_exp if work_exp else "Not Found"

    # Additional Projects extraction using keywords
    if info["Projects"] == "Not Found":
        projects_keywords = ["Projects", "Developed", "Created", "Implemented"]
        projects = [line.strip() for line in text.split("\n") if any(kw in line for kw in projects_keywords)]
        info["Projects"] = projects if projects else "Not Found"

    return info