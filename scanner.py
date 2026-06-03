import subprocess

def run_specific_tool(tool_name, target):
    commands = {
        "Nmap": f"nmap -sV -F {target}",
        "Nuclei": f"nuclei -u {target} -silent",
        "Nikto": f"nikto -h {target} -Tuning 123",
        "Gobuster": f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -q",
        "SQLMap": f"sqlmap -u {target} --batch --level=1 --crawl=2",
        "WP-Scan": f"wpscan --url {target} --batch --enumerate vp",
        "OWASP ZAP": f"zap-baseline.py -t {target}"
    }
    
    cmd = commands.get(tool_name)
    try:
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return process.stdout if process.stdout else process.stderr
    except Exception as e:
        return f"Tool Execution Failed: {str(e)}"
