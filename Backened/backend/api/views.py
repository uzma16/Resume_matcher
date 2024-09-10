
def chat_with_gpt(prompt):
    import requests
    try:
        url = "https://api.openai.com/v1/chat/completions"

        payload = json.dumps(
            {
                "model": "gpt-4-0613",
                "messages": [{"role": "assistant", "content": prompt}],
                "temperature": 0,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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",
            "OpenAI-Organization": "org-muCWsH0ydeomtslkIwAHVG3Z",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)["choices"][0]["message"]["content"]
        # print(type(data), data)
        return {"data": json.loads(data)}
    except Exception as e:
        print(e)
        return {
            "status_code": 500,
            "message": "recommendations are not available right now!",
            "error_type": "recommendation error"
        }

import json
import requests
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text_from_documents  

class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            documents = serializer.save()  # Save documents to get instance
            # Extract text from documents
            resume_text, jd_text = extract_text_from_documents(documents.resume.path, documents.job_description.path)
            # Save extracted text
            documents.extracted_resume_text = resume_text
            documents.extracted_jd_text = jd_text
            documents.save()
            
            # prompt = f"Identify the top  7 skills required in this job description: {jd_text}. Produce the results in JSON format."
            prompt = f"Identify the only top 7 skills required in this job description: {jd_text}. Produce the results in JSON format, with skills listed directly under the 'skills' key."
            skills_required_for_job = chat_with_gpt(prompt) 
            prompt = f"Identify the top 7 skills required in this resume: {resume_text}. Produce the results in JSON format, with skills listed directly under the 'skills' key."
            skills_in_resume = chat_with_gpt(prompt) 
            prompt = f"In the context of the top technical skills - {skills_required_for_job} in the target job based on attached job description, help me draft a narrative in the form of perfect paragraph in less than 200 words to practice the question [Tell me about yourself] using my resume - {resume_text} .Override the inconsistencies in the script, include my relevant experience in my resume to match the desired skills in the target job, and reference the target job title. Produce the output in JSON format."
            gpt_response = chat_with_gpt(prompt)
            # prompt = f"Tell the skills match in percentage with given resume skills: {skills_in_resume} to the skills required for job: {skills_required_for_job}.Produce the output in JSON format."
            # prompt =  f"Match skills in resume ({skills_in_resume}) with job requirements ({skills_required_for_job}) in percentage. Provide output as JSON."
            # prompt = f"Tell the match in percentages for various parameters such as skills, Experience, and Languages between the {resume_text} and {jd_text}.If any parameter is not available in any document then consider it as 75% match from your side.Then Output the results in JSON format, including percentages for each parameter match"
            # ---------working prompt--------------prompt = f"Tell the match in percentages for Skills, Experience, and Languages between the {resume_text} and {jd_text}. If any parameter is not available in any document, consider it as a 75% match from your side. Output the results in JSON format, including the match percentage for each parameter.For every parameter give single value means for Skills(it should total value of each value in skills), for others also follow the same"
            prompt = f"Tell the match percentages for Skills, Experience, and Languages between the provided resume {gpt_response} and job description {jd_text}. For each parameter, if any specific item (e.g., a skill, a job title) is not mentioned in either the resume or the job description, consider it as a 0% match for that item. Aggregate the match percentages for each parameter and calculate the total match percentage as the average of these percentages. Ensure the total values for each parameter do not exceed 100% and that the total match percentage is a meaningful representation of the overall match. Output the results in JSON format, including the match percentage for each parameter and the overall match percentage"
            percentage_match = chat_with_gpt(prompt)
            response = [skills_required_for_job,gpt_response,percentage_match]
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    