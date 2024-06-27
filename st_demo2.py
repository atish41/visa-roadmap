import streamlit as st
import PyPDF2
from fpdf import FPDF
from mistletoe import markdown
from bs4 import BeautifulSoup
import unicodedata
import pdfkit 
import markdown2

# Helper functions
def text_extrater_for_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    first_page = reader.pages[0]
    return first_page.extract_text()

def convert_to_latin1_compatible(text):
    text = text.replace('\u2013', '-')
    text = unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')
    return text

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Visa Roadmap', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(text, output_path):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Generated Visa Roadmap')
    plain_text = markdown(text)
    pdf.chapter_body(plain_text)
    pdf.output(output_path)


def create_pdf_from_html(html_content, output_path, wkhtmltopdf_path):
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_content, output_path, configuration=config)

# Streamlit app
st.header('Upload your questionnaire (PDF)')
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    input_text = text_extrater_for_pdf(uploaded_file)
    generate_roadmap = st.button("Generate Roadmap")

    if generate_roadmap:
        if input_text:
            output_path = "visa_roadmap.pdf"
            complete_output= ""
            pdf_text = convert_to_latin1_compatible(input_text)
            
            st.write(pdf_text)
                
            create_pdf(pdf_text,output_path)
            #html_content=markdown2.markdown(text_gen)

            #wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' 
            #output_pdf_path = "visa_roadmap.pdf"

            #create_pdf_from_html(html_content,output_pdf_path,wkhtmltopdf_path)
            


            
            with open(output_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Visa Roadmap as PDF",
                    data=pdf_file,
                    file_name="visa_roadmap.pdf",
                    mime="application/pdf"
                )
