from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import logging
from config import Config
from scanner.validator import validate_target
from scanner.nmap_scanner import scan_target
from scanner.analyzer import analyze_results
from database.database import init_db, save_scan, get_scan, get_all_scans
from reports.report_generator import generate_html_report, generate_pdf_report

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize DB on startup
with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target', '').strip()
    
    # 1. Validate Target
    is_valid, error_msg = validate_target(target)
    if not is_valid:
        flash(error_msg, "error")
        logger.warning(f"Invalid scan attempt: {target}")
        return redirect(url_for('index'))
        
    logger.info(f"Scan requested for target: {target}")
    return render_template('scanning.html', target=target)

@app.route('/perform_scan', methods=['POST'])
def perform_scan():
    # This route is hit by the javascript on scanning.html to actually perform the long-running scan
    target = request.form.get('target', '').strip()
    
    is_valid, error_msg = validate_target(target)
    if not is_valid:
        return {"error": error_msg}, 400
        
    logger.info(f"Scan started for target: {target}")
    
    # 2. Run Scan
    scan_results = scan_target(target)
    
    if "error" in scan_results:
        logger.error(f"Scan failed for {target}: {scan_results['error']}")
        return {"error": scan_results["error"]}, 500
        
    # 3. Analyze Results
    findings = analyze_results(scan_results)
    
    # 4. Save to Database
    scan_id = save_scan(
        target=scan_results['target'],
        status="completed",
        scan_duration=scan_results['scan_duration'],
        host_status=scan_results['status'],
        ports=scan_results['ports'],
        findings=findings
    )
    
    logger.info(f"Scan completed and saved for target: {target} (Scan ID: {scan_id})")
    
    return {"scan_id": scan_id, "redirect_url": url_for('results', scan_id=scan_id)}, 200

@app.route('/results/<int:scan_id>')
def results(scan_id):
    scan_data = get_scan(scan_id)
    if not scan_data:
        flash("Scan not found.", "error")
        return redirect(url_for('history'))
        
    return render_template('results.html', scan=scan_data)

@app.route('/history')
def history():
    scans = get_all_scans()
    return render_template('history.html', scans=scans)

@app.route('/report/<int:scan_id>/html')
def download_html(scan_id):
    scan_data = get_scan(scan_id)
    if not scan_data:
        flash("Scan not found.", "error")
        return redirect(url_for('history'))
        
    html_path = generate_html_report(scan_data, app.config['HTML_EXPORT_DIR'])
    
    logger.info(f"HTML report downloaded for scan ID: {scan_id}")
    return send_file(html_path, as_attachment=True)

@app.route('/report/<int:scan_id>/pdf')
def download_pdf(scan_id):
    scan_data = get_scan(scan_id)
    if not scan_data:
        flash("Scan not found.", "error")
        return redirect(url_for('history'))
        
    pdf_path, error = generate_pdf_report(scan_data, app.config['PDF_EXPORT_DIR'])
    
    if error:
        flash(f"The scan completed successfully, but the PDF could not be generated: {error}", "warning")
        return redirect(url_for('results', scan_id=scan_id))
        
    logger.info(f"PDF report downloaded for scan ID: {scan_id}")
    return send_file(pdf_path, as_attachment=True, download_name=f"scan_report_{scan_id}.pdf")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message="Page not found."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="An internal server error occurred."), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
