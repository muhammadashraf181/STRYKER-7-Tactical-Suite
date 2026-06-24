import subprocess

def run_specific_tool(tool_name, target):
    commands = {
        "Nmap": f"nmap -Pn -sV -O -A {target}",
        "Nuclei": f"nuclei -u {target} -silent -rate-limit 10 -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)'",
        "Nikto": f"nikto -h {target} -Tuning 123",
        "Gobuster": f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -t 5 --delay 800ms -a 'Mozilla/5.0'",
        "SQLMap": f"sqlmap -u {target} --batch --level=1 --crawl=2 --random-agent --tamper=space2comment,charencode",
        "WP-Scan": f"wpscan --url {target} --batch --enumerate vp --stealth --random-user-agent",
        "OWASP ZAP": f"zap-baseline.py -t {target}"
    }
    
    cmd = commands.get(tool_name)
    try:
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=900)
        return process.stdout if process.stdout else process.stderr
    except Exception as e:
        return f"Tool Execution Failed: {str(e)}"
