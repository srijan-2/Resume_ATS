from dotenv import load_dotenv

load_dotenv()
import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #convert the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='jpeg')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No files Uploaded")
    
## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Application Tracking System")
input_text = st.text_area("Job Description:", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("Resume uploaded Successfully")    

submit1 = st.button("Tell Me About the resume")

# submit2 = st.button("How can I improve")

submit2 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced HR with tech experience in the field of any one job role from  Data Science  Software Engineer, Full Stack Web development, Data Analyst,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Software Engineer, Full Stack Web development, Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")