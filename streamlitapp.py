from rd_endpoint import multiturn_generate_content
import streamlit as st
import PyPDF2
from pdfconverter import convert_to_latin1_compatible, create_pdf

def collect_response(response_generator):
  """
  Collects all text chunks from a response generator and returns the complete response.
  """
  complete_response = ""
  for chunk in response_generator:
    complete_response += chunk.text
  return complete_response

def text_generator(response_generator):
    for chunk in response_generator:
        yield chunk.text

def text_extrater_for_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    first_page = reader.pages[0]
    return first_page.extract_text()
st.header('Upload your questionnaire (PDF)')
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
if uploaded_file is not None:

    input_text  = text_extrater_for_pdf(uploaded_file)
    generate_roadmap=st.button("Generate Roadmap")

    if generate_roadmap:
        if input_text:
            output = multiturn_generate_content(input_text) 
            
            # text_stream = text_generator(output)
            complete_output =""
            for chunk in text_generator(output):
                st.write(chunk)
                complete_output+=chunk
            
            
            
            

            pdf_text = convert_to_latin1_compatible(complete_output)
            print("Following is the  complete response", complete_output)
            output_pdf_path = "visa_roadmap.pdf"
            create_pdf(pdf_text, output_pdf_path)
            with open(output_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Visa Roadmap as PDF",
                    data=pdf_file,
                    file_name="visa_roadmap.pdf",
                    mime="application/pdf"
                )


