import streamlit as st
import scanner
import ai_engine
import time
from fpdf import FPDF

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="STRYKER-7 | Tactical Suite", 
    page_icon="logo.png", 
    layout="wide"
)

# 2. UPGRADED PROFESSIONAL PDF GENERATION ENGINE
def create_pdf(text):
    class PDF(FPDF):
        def header(self):
            # Header Banner Background
            self.set_fill_color(8, 12, 16) 
            self.rect(0, 0, 210, 35, 'F')
            
            # Neon Green Accent Bar
            self.set_fill_color(0, 255, 65)
            self.rect(0, 34, 210, 1, 'F')
            
            # Title
            self.set_y(12)
            self.set_font('Arial', 'B', 16)
            self.set_text_color(0, 255, 65) # Tactical Neon Green
            self.cell(0, 10, 'STRYKER-7 TACTICAL AUDIT REPORT', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            # Professional security tag & dynamic page numbering
            self.cell(0, 10, f'CONFIDENTIAL // STRYKER-7 AUTOMATED SUITE', 0, 0, 'L')
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.ln(15) 
    
    lines = text.split('\n')
    in_table = False
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        # 1. Process Section Headers
        if line.startswith('[HEADER]'):
            pdf.ln(6)
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(11, 26, 18) 
            clean_header = line.replace('[HEADER]', '').strip()
            pdf.cell(0, 10, txt=clean_header, ln=1)
            # Section Divider Underline
            pdf.set_draw_color(0, 255, 65)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(4)
            continue
            
        # 2. Table Parsing & Row Generation
        if '[TABLE]' in line:
            in_table = True
            continue
        if '[ENDTABLE]' in line:
            in_table = False
            pdf.ln(5)
            continue
            
        if in_table:
            col_widths = [30, 90, 35, 35] 
            columns = line.split(',')
            
            # Header Row Styling vs Normal Row Styling
            if 'Tool' in line and 'Finding' in line:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_fill_color(20, 30, 40) 
                pdf.set_text_color(255, 255, 255)
            else:
                pdf.set_font("Courier", size=9) 
                pdf.set_fill_color(245, 245, 245) 
                pdf.set_text_color(0, 0, 0)
                
            # Render Individual Cells
            for idx, col_text in enumerate(columns):
                if idx < len(col_widths):
                    # Smart Severity Highlight Colors
                    if 'Critical' in col_text:
                        pdf.set_text_color(200, 0, 0) 
                    elif 'High' in col_text:
                        pdf.set_text_color(230, 100, 0) 
                        
                    pdf.cell(col_widths[idx], 8, txt=col_text.strip(), border=1, ln=0, fill=True)
                    pdf.set_text_color(0, 0, 0) # Color reset back to black
            pdf.ln(8)
            continue

        # 3. Text & Inline Bold Parsing
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(40, 40, 40)
        
        if '[BOLD]' in line:
            parts = line.split('[BOLD]')
            for part in parts:
                if '[ENDBOLD]' in part:
                    bold_subparts = part.split('[ENDBOLD]')
                    # Bold block
                    pdf.set_font("Arial", 'B', 10)
                    pdf.write(6, bold_subparts[0])
                    # Reset back to regular font
                    pdf.set_font("Arial", size=10)
                    pdf.write(6, bold_subparts[1])
                else:
                    pdf.write(6, part)
            pdf.ln(6)
        else:
            pdf.multi_cell(0, 6, txt=line)
            
    return pdf.output(dest='S').encode('latin-1', 'replace')

# 3. ADVANCED CYBER-READY UI (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Source+Code+Pro&display=swap');
    
    .stApp {
        background: #050a0e;
        background-image: radial-gradient(circle at 50% 50%, #0d1a12 0%, #050a0e 100%);
        color: #e0e0e0;
    }
    
    .main-title {
        color: #00ff41;
        text-align: center;
        font-size: 50px;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.6);
        margin-bottom: 5px;
    }

    section[data-testid="stSidebar"] {
        background-color: #080c10 !important;
        border-right: 1px solid rgba(0, 255, 65, 0.3);
        min-width: 320px !important;
    }

    .stTextInput input {
        background-color: #0d1117 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 4px !important;
    }

    .stButton>button {
        width: 100%;
        background: rgba(0, 255, 65, 0.1) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        font-family: 'Orbitron', sans-serif;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00ff41 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00ff41;
    }

    .report-box {
        padding: 25px;
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid rgba(0, 255, 65, 0.4);
        border-radius: 10px;
        font-family: 'Source Code Pro', monospace;
        color: #a3f7bf;
        backdrop-filter: blur(8px);
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(5, 10, 14, 0.95);
        color: #8b949e;
        text-align: center;
        padding: 12px;
        border-top: 1px solid rgba(0, 255, 65, 0.2);
    }
    .footer a {
        color: #00ff41;
        text-decoration: none;
        margin: 0 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR: CENTERED LOGO & STATUS
with st.sidebar:
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 20px 0;">
            <div style="text-align: center;">
    """, unsafe_allow_html=True)
    
    try:
        st.image("logo.png", width=260)
    except:
        st.markdown("<h1 style='color:#00ff41;'></h1>", unsafe_allow_html=True)
    
    st.markdown("""
            </div>
            <h2 style='color:#00ff41; text-align:center; font-family:Orbitron; font-size:24px; margin-top:15px; letter-spacing:2px;'>STRYKER-7</h2>
            <p style='color:#8b949e; text-align:center; font-size:11px; margin-top:-10px;'>AUTONOMOUS TACTICAL SUITE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown('<div style="border: 1px solid #00ff41; color: #00ff41; padding: 10px; text-align: center; border-radius: 4px; font-weight: bold; background: rgba(0, 255, 65, 0.05);">STATION: ONLINE</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div style="border: 1px solid #58a6ff; color: #58a6ff; padding: 10px; text-align: center; border-radius: 4px; font-weight: bold; background: rgba(88, 166, 255, 0.05);">AI ENGINE: READY</div>', unsafe_allow_html=True)

# 5. MAIN DASHBOARD
st.markdown('<h1 class="main-title">STRYKER-7 TACTICAL SUITE</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; margin-bottom: 40px;'>Autonomous Security Assessment & Neural Reporting Engine</p>", unsafe_allow_html=True)

left_spacer, input_container, right_spacer = st.columns([1, 2, 1])
with input_container:
    target_url = st.text_input("INITIALIZE SCAN PROTOCOL:", placeholder="Enter Target URL/IP")
    execute_btn = st.button("INITIATE DEPLOYMENT")

if execute_btn:
    if target_url:
        col_cmd, col_report = st.columns([1, 1.3])
        with col_cmd:
            st.markdown("### COMMAND CENTER")
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = {}
            tools = ["Nmap", "Nuclei", "Nikto", "Gobuster", "SQLMap", "WP-Scan", "OWASP ZAP"]
            for i, tool in enumerate(tools):
                status_text.markdown(f"**Executing:** `{tool}`...")
                results[tool] = scanner.run_specific_tool(tool, target_url)
                progress_bar.progress((i + 1) / len(tools))
                time.sleep(0.4)
            st.success("DEPLOYMENT COMPLETE")

        with col_report:
            st.markdown("### NEURAL ANALYSIS")
            with st.spinner("AI analyzing tactical data..."):
                final_report = ai_engine.generate_report(results)
                st.markdown(f'<div class="report-box">{final_report}</div>', unsafe_allow_html=True)
                st.write("")
                pdf_bytes = create_pdf(final_report)
                st.download_button("DOWNLOAD PDF REPORT", data=pdf_bytes, file_name="Stryker7_Audit_Report.pdf", mime="application/pdf")

# 6. FOOTER
st.markdown(f"""
    <div class="footer">
        <span>Muhammad Ashraf | Cybersecurity Student</span> | 
        <a href="https://www.linkedin.com/in/muhammad-ashraf-09873733a" target="_blank">LinkedIn</a> | 
        <a href="https://muhammad-ashraf-portfolio-ten.vercel.app" target="_blank">Portfolio</a> |
    </div>
""", unsafe_allow_html=True)
