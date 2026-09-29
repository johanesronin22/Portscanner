import pytest
from scanner.validator import is_valid_target, validate_target

def test_valid_ipv4():
    assert is_valid_target("192.168.1.1") == True
    assert is_valid_target("8.8.8.8") == True

def test_valid_ipv6():
    assert is_valid_target("2001:4860:4860::8888") == True
    assert is_valid_target("::1") == True

def test_valid_domain():
    assert is_valid_target("scanme.nmap.org") == True
    assert is_valid_target("google.com") == True
    assert is_valid_target("localhost") == True

def test_invalid_ip():
    assert is_valid_target("256.256.256.256") == False
    assert is_valid_target("1.2.3.4.5") == False

def test_invalid_domain():
    assert is_valid_target("invalid..domain") == False
    assert is_valid_target("-invalid.com") == False

def test_empty_input():
    assert is_valid_target("") == False
    assert is_valid_target("   ") == False
    assert is_valid_target(None) == False

def test_malicious_input():
    assert is_valid_target("127.0.0.1; rm -rf /") == False
    assert is_valid_target("google.com | ls") == False
    assert is_valid_target("scanme.nmap.org & echo 'hacked'") == False
    
def test_validate_target_message():
    valid, msg = validate_target("invalid!!")
    assert valid == False
    assert "Invalid target" in msg
    
    valid, msg = validate_target("192.168.1.1")
    assert valid == True
    assert msg == ""
