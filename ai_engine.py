import google.generativeai as genai

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
        1. DO NOT use any markdown characters like hashtags (#), asterisks (*), or underscores (_) anywhere in the report.
        2. Format Main Headers in ALL CAPS with a blank line before and after them.
        3. Format Subheadings in Title Case (Capitalize Each Word) with a blank line before them.
        4. Present data in a clean, standard text-based table structure without markdown pipes. Use dashes (-) for dividers.
        5. Provide specific remediation commands or configuration fixes clearly on new lines.

        ### REQUIRED REPORT STRUCTURE:
        STRYKER-7 TACTICAL AUDIT REPORT

        1. EXECUTIVE SUMMARY
        [Provide text here]

        2. AGGREGATED FINDINGS TABLE
        Tool ---------------- Finding ---------------- Severity ---------------- CVSS ---- Status
        [Populate data rows here]

        3. DEEP DIVE ANALYSIS
        Information Disclosure (phpinfo)
        [Provide text here]

        Administrative Interfaces and Configuration Issues
        [Provide text here]

        4. STRATEGIC REMEDIATION PLAN
        Immediate Hardening Actions
        [Provide step-by-step technical fixes and commands]

        Tone: Concise, tactical, and highly professional.
        """

        response = model.generate_content(prompt)
        return response.text if response.text else "Error: STRYKER-7 could not generate report content."

    except Exception as e:
        return f"STRYKER AI Engine Error: {str(e)}"
