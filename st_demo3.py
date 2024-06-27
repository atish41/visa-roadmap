import streamlit as st
import PyPDF2
import pdfkit
import markdown2
from rd_endpoint import multiturn_generate_content

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

def text_extractor_for_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    first_page = reader.pages[0]
    return first_page.extract_text()

def convert_to_latin1_compatible(text):
    return text.encode('latin1', 'ignore').decode('latin1')

def create_pdf_from_html(html_content, output_path, wkhtmltopdf_path):
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_content, output_path, configuration=config)

st.header('Upload your questionnaire (PDF)')
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
if uploaded_file is not None:
    input_text = text_extractor_for_pdf(uploaded_file)
    generate_roadmap = st.button("Generate Roadmap")

    if generate_roadmap:
        if input_text:
            output = multiturn_generate_content(input_text)
            complete_output = ""
            for chunk in text_generator(output):
                st.write(chunk)
                complete_output += chunk

            # Convert complete output to HTML
            html_content = markdown2.markdown(complete_output)

            # Path to wkhtmltopdf executable
            wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update this path if necessary
            output_pdf_path = "visa_roadmap.pdf"

            # Create PDF from HTML content
            create_pdf_from_html(html_content, output_pdf_path, wkhtmltopdf_path)

            with open(output_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Visa Roadmap as PDF",
                    data=pdf_file,
                    file_name="visa_roadmap.pdf",
                    mime="application/pdf"
                )
