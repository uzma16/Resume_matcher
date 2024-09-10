import PyPDF2
from docx import Document as docx_document

def extract_text_from_documents(resume_path, job_description_path):
    # Initialize empty strings to store the extracted text
    resume_text = ""
    jd_text = ""

    # Extract text from resume (PDF or DOC)
    if resume_path.endswith('.pdf'):
        with open(resume_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                resume_text += page_obj.extract_text()
    elif resume_path.endswith('.docx'):
        docx_document_obj = docx_document(resume_path)
        for paragraph in docx_document_obj.paragraphs:
            resume_text += paragraph.text      

    # Extract text from job description (PDF or DOC)
    if job_description_path.endswith('.pdf'):
        with open(job_description_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                jd_text += page_obj.extract_text()
    elif job_description_path.endswith('.docx'):
        docx_document_obj = docx_document(job_description_path)
        for paragraph in docx_document_obj.paragraphs:
            jd_text += paragraph.text     

    return resume_text, jd_text

