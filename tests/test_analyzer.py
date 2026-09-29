from scanner.analyzer import analyze_results

def test_analyze_empty():
    assert analyze_results({}) == []
    assert analyze_results({"error": "Failed"}) == []
    assert analyze_results({"ports": []}) == []

def test_analyze_ftp():
    res = {"ports": [{"port": 21, "state": "open"}]}
    obs = analyze_results(res)
    assert len(obs) == 1
    assert obs[0]["severity"] == "MEDIUM"
    assert "FTP" in obs[0]["finding"]

def test_analyze_ssh():
    res = {"ports": [{"port": 22, "state": "open"}]}
    obs = analyze_results(res)
    assert len(obs) == 1
    assert obs[0]["severity"] == "INFO"
    assert "SSH" in obs[0]["finding"]

def test_analyze_telnet():
    res = {"ports": [{"port": 23, "state": "open"}]}
    obs = analyze_results(res)
    assert len(obs) == 1
    assert obs[0]["severity"] == "HIGH"
    assert "Telnet" in obs[0]["finding"]

def test_analyze_multiple():
    res = {"ports": [
        {"port": 80, "state": "open"},
        {"port": 445, "state": "open"},
        {"port": 3389, "state": "open"},
        {"port": 3306, "state": "open"},
        {"port": 8080, "state": "open"} # Unknown port
    ]}
    obs = analyze_results(res)
    assert len(obs) == 4
    severities = [o["severity"] for o in obs]
    assert "LOW" in severities
    assert severities.count("MEDIUM") == 3
