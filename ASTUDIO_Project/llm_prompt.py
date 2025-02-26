import os
import openai

# can use the below code instead to hide your api key for security purposes
# openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = "sk**********************" # Replace your API Key here
openai.api_key = OPENAI_API_KEY 

# Function to call OpenAI API
def analyze_with_llm(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI that analyzes resumes."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "Error while analyzing with LLM."

# Function to create structured prompt
def create_llm_prompt(extracted_info):
    prompt = f"""
    You are an AI expert specializing in Resume/CV analysis. Below is a candidate's CV information:

    Name: {extracted_info.get("Name", "Not Found")}
    Email: {extracted_info.get("Email", "Not Found")}
    Phone: {extracted_info.get("Phone", "Not Found")}
    Organizations: {extracted_info.get("Organizations", "Not Found")}
    Education: {extracted_info.get("Education", "Not Found")}
    Work Experience: {extracted_info.get("Work Experience", "Not Found")}
    Skills: {extracted_info.get("Skills", "Not Found")}
    Projects: {extracted_info.get("Projects", "Not Found")}
    Certifications: {extracted_info.get("Certifications", "Not Found")}

    Please analyze the CV information and provide feedback on the following:
    1. Strengths in skills and qualifications.
    2. Opportunities for improvement in the resume.
    3. Overall assessment of the candidate's profile.

    Provide the response in a clear and structured format, with detailed recommendations.
    """
    return prompt
