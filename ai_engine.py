import google.generativeai as genai
import os

API_KEY = "Your Gemini AI API KEY" 
genai.configure(api_key=API_KEY)

def generate_report(scan_results):
   
    try:
        model = genai.GenerativeModel('models/gemini-3.1-flash-lite')
    
        prompt = f"""
        You are the STRYKER-7 AI Security Orchestrator.
        Your task is to analyze raw output from a 7-tool VAPT suite and provide a unified tactical audit.

        ### INPUT DATA FROM TOOLS:
        {scan_results}

        ### CRITICAL OUTPUT INSTRUCTIONS:
        1. DO NOT use raw Markdown headers like '##' or '###'. Instead, prefix headers with '[HEADER]' or '[SUBHEADER]'.
           Example: [HEADER] 1. EXECUTIVE SUMMARY
        2. DO NOT use asterisks '**' or '__' for bolding. Use '[BOLD] text [ENDBOLD]' for important terms.
        3. Do not use markdown pipe tables. Format tabular data clearly as comma-separated values under a '[TABLE]' tag, like this:
           [TABLE]
           Tool, Finding, Severity, Status
           Nmap, Open Port 80, Medium, Confirmed
           [ENDTABLE]
        4. Provide specific remediation commands or configuration fixes.

        ### REQUIRED REPORT STRUCTURE:
        [HEADER] 1. EXECUTIVE SUMMARY
        (Brief overview of the target's security posture)
        
        [HEADER] 2. AGGREGATED FINDINGS TABLE
        [TABLE]
        Tool, Finding, Severity, Status
        (Populate dynamically based on scan results)
        [ENDTABLE]

        [HEADER] 3. DEEP DIVE ANALYSIS
        (Detailed explanation of Critical/High risks)

        [HEADER] 4. STRATEGIC REMEDIATION PLAN
        (Step-by-step technical fixes for the sysadmin/developer)

        Tone: Concise, tactical, and highly professional.
        """

        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return "Error: STRYKER-7 could not generate report content."

    except Exception as e:
        return f"STRYKER-7 AI Engine Error: {str(e)}"
