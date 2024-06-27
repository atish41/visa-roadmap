import streamlit as st
import markdown2
import pdfkit
import os

# Streamlit app
st.header('Upload your Markdown file')
uploaded_file = st.file_uploader("Upload Markdown", type="md")

def convert_md_to_pdf(md_content, output_path):
    # Convert the markdown content to HTML
    html_content = markdown2.markdown(md_content)

    # Define the path to wkhtmltopdf executable
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update this path if necessary
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Convert the HTML content to PDF
    pdfkit.from_string(html_content, output_path, configuration=config)

if uploaded_file is not None:
    # Read the markdown content from the uploaded file
    md_content = uploaded_file.read().decode('utf-8')
    
    generate_roadmap = st.button("Generate PDF")

    if generate_roadmap:
        output_path = "client_info.pdf"
        convert_md_to_pdf(md_content, output_path)
        
        with open(output_path, "rb") as pdf_file:
            st.download_button(
                label="Download Generated PDF",
                data=pdf_file,
                file_name="client_info.pdf",
                mime="application/pdf"
            )
