import nmap
import time

def scan_target(target: str) -> dict:
    """
    Scans a target using python-nmap and normalizes the results.
    Prioritizes open ports, service detection, and version detection.
    Handles errors gracefully.
    """
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        return {
            "error": "Nmap is not installed or could not be located. Please install Nmap and ensure it is available on your system PATH."
        }
    except Exception as e:
        return {
            "error": f"Failed to initialize Nmap: {str(e)}"
        }

    start_time = time.time()
    
    try:
        # -sV: Probe open ports to determine service/version info
        # -F: Fast mode - Scan fewer ports than the default scan
        # -Pn: Treat all hosts as online -- skip host discovery
        nm.scan(hosts=target, arguments='-sV -F -Pn')
    except Exception as e:
        return {
            "error": f"The scan could not be completed: {str(e)}"
        }
        
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    if target not in nm.all_hosts():
        # Sometimes Nmap resolves the domain to an IP and uses that IP as the host key
        # Let's check if there are any hosts returned at all
        hosts = nm.all_hosts()
        if not hosts:
            return {
                "error": "The scan completed, but no hosts were found. The target might be down or unreachable."
            }
        # Use the first host found if the target name was resolved to an IP
        host_key = hosts[0]
    else:
        host_key = target
        
    scan_data = nm[host_key]
    host_status = scan_data.state() if scan_data.state() else "unknown"
    
    normalized_results = {
        "target": target,
        "resolved_ip": host_key if host_key != target else None,
        "status": host_status,
        "scan_duration": duration,
        "ports": []
    }
    
    if 'tcp' in scan_data:
        for port in sorted(scan_data['tcp'].keys()):
            port_info = scan_data['tcp'][port]
            
            normalized_results['ports'].append({
                "port": port,
                "protocol": "tcp",
                "state": port_info.get('state', 'unknown'),
                "service": port_info.get('name', 'unknown'),
                "product": port_info.get('product', ''),
                "version": port_info.get('version', ''),
                "extra_info": port_info.get('extrainfo', '')
            })
            
    return normalized_results
