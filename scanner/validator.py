import ipaddress
import re

def is_valid_target(target: str) -> bool:
    """
    Validates if a given string is a valid IPv4, IPv6, or domain name.
    Rejects empty, malformed, or potentially dangerous inputs.
    """
    if not target or not isinstance(target, str):
        return False
        
    target = target.strip()
    
    if not target:
        return False
        
    # Prevent obvious command injection characters
    if any(char in target for char in [';', '|', '&', '$', '>', '<', '`', '\\', '\n', '\r']):
        return False
        
    # Check if it's a valid IP address
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
        
    # Check if it's a valid domain name
    # Domain name regex based on RFC 1035/1123
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9]' # First character of the domain
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+' # Sub domain + hostname
        r'[a-zA-Z]{2,6}$' # Top level domain
    )
    
    # Also allow 'localhost' for testing
    if target.lower() == 'localhost':
        return True
        
    if domain_regex.match(target):
        return True
        
    return False

def validate_target(target: str) -> tuple[bool, str]:
    """
    Validates target and returns a tuple (is_valid, error_message).
    """
    if is_valid_target(target):
        return True, ""
    else:
        return False, "Invalid target. Please enter a valid IP address or domain name."
