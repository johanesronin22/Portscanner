# Port Scanner Report Generator

A complete, beginner-friendly cybersecurity internship project built with Python and Flask. This application automates network service discovery using Nmap, analyzes the results for basic security configurations, and generates professional HTML and PDF reports.

## Features

- **Automated Scanning**: Wraps Nmap to perform service and version detection.
- **Input Validation**: Ensures targets are valid IP addresses or domains.
- **Security Analyzer**: Rule-based analysis for common exposed services (FTP, SSH, HTTP, SMB, etc.).
- **Report Generation**: Exports findings to HTML and PDF formats.
- **Scan History**: Stores previous scans and findings using SQLite.
- **Responsive Dashboard**: Dark-themed, professional cybersecurity UI.

## Screenshots

*Note: Add actual screenshots of your running application here.*

### Homepage
![Homepage](static/img/screenshot_home.png)

### Scan Results & Security Recommendations
![Scan Results](static/img/screenshot_results.png)

### Scan History
![Scan History](static/img/screenshot_history.png)

### Generated Report
![HTML/PDF Report](static/img/screenshot_report.png)

## Architecture

The application is structured into the following components:
- **Web Layer**: Flask application (`app.py`) providing the HTTP interface.
- **Scanner Layer**:
  - `validator.py`: Sanitizes and validates user input.
  - `nmap_scanner.py`: Wraps `python-nmap` to perform the actual network scan.
  - `analyzer.py`: Generates security observations based on detected services.
- **Database Layer**: SQLite (`database.py` & `schema.sql`) for persistent storage.
- **Reporting Layer**: Jinja2 and xhtml2pdf (`report_generator.py`) to render and save reports.

## Requirements

- Python 3.8+
- Nmap (must be installed on the system)


## Installation

### 1. Install Nmap
**Windows:**
1. Download the Nmap installer from [nmap.org/download.html](https://nmap.org/download.html).
2. Run the installer and ensure Npcap is installed during the process.
3. Verify Nmap is in your system PATH by opening a terminal and running `nmap --version`.

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install nmap
```

**macOS:**
```bash
brew install nmap
```

### 2. Set Up the Python Environment
Clone this repository and create a virtual environment:

```bash
git clone <repository-url>
cd port-scanner

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note on PDF Generation:**
> This project uses `xhtml2pdf` to generate PDFs directly from HTML templates without requiring external system dependencies like GTK or wkhtmltopdf.

### 4. Configuration
Rename `.env.example` to `.env` and set a secure `FLASK_SECRET_KEY`.

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`.

## Usage

1. **Enter Target**: On the homepage, enter an authorized target (e.g., `scanme.nmap.org`).
2. **Scan**: Click "Start Scan" and wait for the results. The application will use Nmap to discover open ports.
3. **View Results**: The dashboard will display the host status, scan duration, open ports, and any security observations.
4. **Download Report**: Use the buttons on the results page to download the report in HTML or PDF format.
5. **View History**: Access the "History" tab to review previous scans.

## Security Considerations

- **Authorization**: Only scan systems you own or have explicit, documented authorization to assess.
- **Command Safety**: The application uses the `python-nmap` API instead of raw shell commands to prevent command injection.
- **Database Safety**: Parameterized SQL queries are used to prevent SQL injection.
- **Input Validation**: Targets are strictly validated against IP and domain regular expressions before scanning.

## Limitations

- **Not a Vulnerability Scanner**: This tool performs port scanning and service enumeration. It does not actively exploit systems or replace professional tools like Nessus or OpenVAS.
- **Single Target**: The current version accepts one IP or domain at a time.
- **Rule-Based Analysis**: Security observations are based on simple rules (e.g., "Telnet is exposed") rather than dynamic vulnerability checks.

## Project Structure

```
port-scanner/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── scanner/                # Scanning logic
│   ├── validator.py        # Input validation
│   ├── nmap_scanner.py     # Nmap wrapper
│   └── analyzer.py         # Security recommendations
├── database/               # Storage layer
│   ├── database.py         # SQLite connection & queries
│   └── schema.sql          # Table definitions
├── reports/                # Export generation
│   └── report_generator.py # HTML/PDF logic
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, JS, Images
├── exports/                # Generated reports
│   ├── html/
│   └── pdf/
└── tests/                  # Unit tests
```

---
*Created as a cybersecurity internship project demonstrating Python, Flask, Nmap automation, and security reporting.*
