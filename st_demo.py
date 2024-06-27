import streamlit as st
import PyPDF2
from fpdf import FPDF
from bs4 import BeautifulSoup
from rd_endpoint import multiturn_generate_content

# Define helper functions
def collect_response(response_generator):
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

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def convert_to_latin1_compatible(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PR Roadmap', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(text, filename):
    pdf = PDF()
    pdf.add_page()
    parsed_text = BeautifulSoup(text, 'html.parser')
    for element in parsed_text:
        if element.name in ['h2', 'h3']:
            pdf.chapter_title(element.get_text())
        else:
            pdf.chapter_body(element.get_text())
    pdf.output(filename)

# Streamlit application
st.header('Upload your questionnaire (PDF)')
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    input_text = text_extrater_for_pdf(uploaded_file)
    generate_roadmap = st.button("Generate Roadmap")

    if generate_roadmap:
        if input_text:
            parsed_html = parse_html(input_text)
            parsed_text = parsed_html.get_text(separator='\n', strip=True)
            output = multiturn_generate_content(parsed_text)
            
            complete_output = ""
            for chunk in text_generator(output):
                st.write(chunk)
                complete_output += chunk
            
            pdf_text = convert_to_latin1_compatible(complete_output)
            st.write("Following is the complete response:", complete_output)  # Debug print statement for complete output
            output_pdf_path = "visa_roadmap.pdf"
            create_pdf(pdf_text, output_pdf_path)
            
            with open(output_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Visa Roadmap as PDF",
                    data=pdf_file,
                    file_name="visa_roadmap.pdf",
                    mime="application/pdf"
                )
