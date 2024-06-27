import markdown2
from weasyprint import HTML

# Read the markdown content from the file
with open('client_info.md', 'r') as md_file:
    md_content = md_file.read()

# Convert the markdown content to HTML
html_content = markdown2.markdown(md_content)

# Convert the HTML content to PDF
HTML(string=html_content).write_pdf('client_info.pdf')

print("PDF created successfully!")
