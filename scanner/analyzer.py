def analyze_results(scan_results: dict) -> list:
    """
    Analyzes normalized scan results and returns a list of security observations.
    Each observation contains: severity, finding, recommendation.
    """
    observations = []
    
    if "error" in scan_results or "ports" not in scan_results:
        return observations
        
    for port_info in scan_results["ports"]:
        port = port_info.get("port")
        state = port_info.get("state", "").lower()
        
        if state != "open":
            continue
            
        # Port 21: FTP
        if port == 21:
            observations.append({
                "severity": "MEDIUM",
                "finding": "FTP service is exposed on port 21.",
                "recommendation": "Consider replacing unencrypted FTP with SFTP or FTPS where appropriate. Restrict access to trusted networks where possible."
            })
            
        # Port 22: SSH
        elif port == 22:
            observations.append({
                "severity": "INFO",
                "finding": "SSH remote administration is exposed on port 22.",
                "recommendation": "Restrict SSH access where possible, use key-based authentication, and disable root login."
            })
            
        # Port 23: Telnet
        elif port == 23:
            observations.append({
                "severity": "HIGH",
                "finding": "Telnet is exposed on port 23.",
                "recommendation": "Avoid Telnet because it transmits credentials in plaintext. Use SSH instead."
            })
            
        # Port 80: HTTP
        elif port == 80:
            observations.append({
                "severity": "LOW",
                "finding": "HTTP service is exposed on port 80.",
                "recommendation": "If sensitive information is transmitted, ensure traffic is redirected to HTTPS/TLS."
            })
            
        # Port 445: SMB
        elif port == 445:
            observations.append({
                "severity": "MEDIUM",
                "finding": "SMB is exposed on port 445.",
                "recommendation": "Restrict SMB access to trusted networks. Ensure the service is properly secured and patched against known vulnerabilities."
            })
            
        # Port 3306: MySQL
        elif port == 3306:
            observations.append({
                "severity": "MEDIUM",
                "finding": "MySQL database service is exposed on port 3306.",
                "recommendation": "Restrict database access to trusted application hosts or networks. Do not expose databases directly to the internet."
            })
            
        # Port 3389: RDP
        elif port == 3389:
            observations.append({
                "severity": "MEDIUM",
                "finding": "Remote Desktop Protocol is exposed on port 3389.",
                "recommendation": "Restrict RDP access and avoid unnecessary internet exposure. Use a VPN or RD Gateway for secure access."
            })
            
    return observations
