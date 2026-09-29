import os
import datetime
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

def get_template_env():
    """Sets up the Jinja2 environment for report templates."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'templates')
    return Environment(loader=FileSystemLoader(template_dir))

def generate_report_html_string(scan_data: dict) -> str:
    """Generates the HTML content for the report."""
    env = get_template_env()
    template = env.get_template('report.html')
    
    # Add a formatted generation date
    generation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = template.render(
        scan=scan_data,
        generation_date=generation_date
    )
    return html_content

def generate_html_report(scan_data: dict, export_dir: str) -> str:
    """Saves the HTML report to a file and returns the path."""
    html_content = generate_report_html_string(scan_data)
    
    # Sanitize filename
    target_clean = "".join([c if c.isalnum() else "_" for c in scan_data.get('target', 'unknown')])
    filename = f"scan_{scan_data['id']}_{target_clean}.html"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return filepath

def generate_pdf_report(scan_data: dict, export_dir: str) -> tuple[str, str]:
    """Generates a PDF report using xhtml2pdf. Returns (filepath, error_message)."""
    html_content = generate_report_html_string(scan_data)
    
    target_clean = "".join([c if c.isalnum() else "_" for c in scan_data.get('target', 'unknown')])
    filename = f"scan_{scan_data['id']}_{target_clean}.pdf"
    filepath = os.path.join(export_dir, filename)
    
    try:
        with open(filepath, "w+b") as result_file:
            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(
                html_content,                
                dest=result_file
            )
            
        if pisa_status.err:
            return None, "Error generating PDF with xhtml2pdf"
            
        return filepath, None
    except Exception as e:
        return None, str(e)
