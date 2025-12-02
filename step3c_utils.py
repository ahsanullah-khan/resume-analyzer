
from step3a_imports import re
import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_content, filename):
    """Extract text from PDF, DOCX, or TXT files"""
    if filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith('.docx'):
        doc = Document(io.BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    else:
        return file_content.decode('utf-8')

def extract_years_of_experience(text):
    """Extract years of experience from text"""
    years_pattern = r'(\d+)\s*(?:years?|yrs?)'
    matches = re.findall(years_pattern, text.lower())
    return max([int(match) for match in matches]) if matches else 0

def clean_text_for_similarity(text):
    """Clean and prepare text for semantic analysis"""
    return ' '.join(text.split()[:300])

def clean_suggestions(text):
    """Clean and format AI suggestions"""
    suggestions = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        clean_line = re.sub(r'^[\d\-•\.\)\s]+', '', line).strip()
        if clean_line and len(clean_line) > 15 and not clean_line.startswith(('RESUME', 'JOB', 'CURRENT')):
            suggestions.append(clean_line)

    if len(suggestions) < 2:
        suggestions = [
            "Quantify your achievements with specific numbers and metrics",
            "Add relevant industry-specific keywords from the job description",
            "Highlight your most relevant experience at the top of the resume"
        ]

    return suggestions[:4]
