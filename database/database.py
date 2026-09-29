import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'portscanner.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_db_connection():
    """Returns a database connection with row factory configured."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def save_scan(target: str, status: str, scan_duration: float, host_status: str, ports: list, findings: list) -> int:
    """Saves a scan and its related ports and findings. Returns the scan ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert scan
    cursor.execute('''
        INSERT INTO scans (target, status, scan_duration, host_status)
        VALUES (?, ?, ?, ?)
    ''', (target, status, scan_duration, host_status))
    
    scan_id = cursor.lastrowid
    
    # Insert ports
    for port in ports:
        cursor.execute('''
            INSERT INTO ports (scan_id, port, protocol, state, service, product, version, extra_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scan_id, port.get('port'), port.get('protocol'), port.get('state'),
            port.get('service'), port.get('product'), port.get('version'), port.get('extra_info')
        ))
        
    # Insert findings
    for finding in findings:
        cursor.execute('''
            INSERT INTO findings (scan_id, severity, finding, recommendation)
            VALUES (?, ?, ?, ?)
        ''', (scan_id, finding.get('severity'), finding.get('finding'), finding.get('recommendation')))
        
    conn.commit()
    conn.close()
    return scan_id

def get_scan(scan_id: int) -> dict:
    """Retrieves a complete scan record."""
    conn = get_db_connection()
    scan_row = conn.execute('SELECT * FROM scans WHERE id = ?', (scan_id,)).fetchone()
    
    if not scan_row:
        conn.close()
        return None
        
    scan_dict = dict(scan_row)
    
    # Get ports
    ports = conn.execute('SELECT * FROM ports WHERE scan_id = ? ORDER BY port ASC', (scan_id,)).fetchall()
    scan_dict['ports'] = [dict(p) for p in ports]
    
    # Get findings
    findings = conn.execute('SELECT * FROM findings WHERE scan_id = ?', (scan_id,)).fetchall()
    scan_dict['findings'] = [dict(f) for f in findings]
    
    conn.close()
    return scan_dict

def get_all_scans() -> list:
    """Retrieves all scans for history."""
    conn = get_db_connection()
    scans = conn.execute('SELECT * FROM scans ORDER BY scan_date DESC').fetchall()
    conn.close()
    return [dict(s) for s in scans]
