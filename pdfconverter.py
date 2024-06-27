import unicodedata
from fpdf import FPDF
from mistletoe import markdown

def convert_to_latin1_compatible(text):
    # Replace the en-dash with a hyphen
    text = text.replace('\u2013', '-')
    
    # Normalize and encode to latin-1, ignoring unsupported characters
    text = unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')
    
    return text
# Function to create a PDF from text with UTF-8 encoding
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

  # Add the plain text to the PDF
    pdf.chapter_body(plain_text)
    pdf.chapter_body(text)
    pdf.output(output_path)


