#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RIZERxPROFILE - Web Dashboard (Final)
Stylish all-in-one Flask application with top menu, dynamic forms, and social credits.
Compatible with Vercel serverless & local dev (0.0.0.0:8080)
Author: RIZERxPROFILE
Version: 2.4
"""

import sys
import requests
from flask import Flask, request, jsonify, render_template_string
from colorama import init

init(autoreset=True)

# ========================== CONSTANTS ==========================
ITEM_ID = "203000000/204000000/205000000/211000000/211000000/211000000/203000000/203000000/203000000/204000000/204000000/204000000/205000000/205000000/203000000/203000000"

# Existing URLs
GUEST_ADD_URL = "https://rizerxprofileitemadder.vercel.app/add-profile-guest"
JWT_ADD_URL   = "https://rizerxprofileitemadder.vercel.app/add-profile"
ACCESS_ADD_URL = "https://rizerxprofileitemadder.vercel.app/add-profile-access-v2"
ACCESS_TO_JWT_URL = "https://rizerxaccessjwt.vercel.app/rizer"
GUEST_TO_CREDS_URL = "https://rizerxguestaccountacceee.vercel.app//rizer"

# Long Bio URLs
LONG_BIO_GUEST_URL = "https://cleint-bio-changer.vercel.app/bio_upload"
LONG_BIO_JWT_URL = "https://cleint-bio-changer.vercel.app/bio_upload"

# ========================== UTILITY FUNCTIONS ==========================
def format_api_response(response_data):
    """Convert JSON response to clean plain text."""
    if isinstance(response_data, dict):
        lines = []
        for key, value in response_data.items():
            clean_key = str(key).replace('"', '').replace("'", "").replace("{", "").replace("}", "").replace("\\", "")
            if isinstance(value, (dict, list)):
                clean_val = format_api_response(value).replace("\n", "\n    ")
            else:
                clean_val = str(value).replace('"', '').replace("'", "").replace("{", "").replace("}", "").replace("\\", "")
            lines.append(f"  {clean_key}: {clean_val}")
        return "\n".join(lines)
    elif isinstance(response_data, list):
        lines = []
        for idx, item in enumerate(response_data):
            clean_item = format_api_response(item).replace("\n", "\n  ")
            lines.append(f"  • Item {idx+1}:\n    {clean_item}")
        return "\n".join(lines)
    else:
        return str(response_data).replace('"', '').replace("'", "").replace("{", "").replace("}", "").replace("\\", "")

def send_request(url, params=None, method="GET"):
    """Send HTTP request and return formatted response."""
    try:
        if method.upper() == "GET":
            resp = requests.get(url, params=params, timeout=15)
        else:
            resp = requests.post(url, data=params, timeout=15)

        if resp.status_code != 200:
            error_detail = ""
            try:
                error_data = resp.json()
                error_detail = format_api_response(error_data)
            except:
                error_detail = resp.text[:500]
            return f"HTTP Error {resp.status_code}: {resp.reason}\nDetails: {error_detail}"

        try:
            data = resp.json()
            return format_api_response(data)
        except ValueError:
            return resp.text.replace('"', '').replace("'", "").replace("{", "").replace("}", "").replace("\\", "")
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def guest_login(uid, password):
    return send_request(GUEST_ADD_URL, {"uid": uid, "password": password, "itemid": ITEM_ID})

def jwt_login(token):
    return send_request(JWT_ADD_URL, {"token": token, "itemid": ITEM_ID})

def access_token_login(access_token):
    return send_request(ACCESS_ADD_URL, {"accesstoken": access_token, "itemid": ITEM_ID})

def access_to_jwt(access_token):
    return send_request(ACCESS_TO_JWT_URL, {"access_token": access_token})

def guest_to_creds(uid, password):
    return send_request(GUEST_TO_CREDS_URL, {"uid": uid, "password": password})

def long_bio_guest(bio, uid, password):
    return send_request(LONG_BIO_GUEST_URL, {"bio": bio, "uid": uid, "pass": password}, method="GET")

def long_bio_jwt(bio, jwt_token):
    return send_request(LONG_BIO_JWT_URL, {"bio": bio, "jwt": jwt_token}, method="GET")

# ========================== FLASK APP ==========================
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RIZERxPROFILE | Ultimate Item Manager</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600;14..32,700;14..32,800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 10% 20%, rgba(0, 0, 0, 0.95), rgba(10, 5, 20, 0.98));
            color: #eef5ff;
            min-height: 100vh;
            padding: 2rem 1.5rem;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 30% 50%, rgba(255, 60, 172, 0.08), transparent 70%);
            pointer-events: none;
            z-index: 0;
            animation: pulseGlow 8s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { opacity: 0.3; }
            100% { opacity: 0.8; }
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .hero {
            text-align: center;
            margin-bottom: 2rem;
            animation: fadeInDown 0.8s ease;
        }
        .hero h1 {
            font-size: 3.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FF3CAC, #784BA0, #2B86C5);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 12px rgba(255,60,172,0.4);
            letter-spacing: -0.5px;
        }
        .hero .tag {
            font-size: 1rem;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(5px);
            display: inline-block;
            padding: 0.5rem 1.5rem;
            border-radius: 40px;
            margin-top: 0.8rem;
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .top-menu {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.8rem;
            margin-bottom: 2rem;
            background: rgba(10, 8, 25, 0.85);
            backdrop-filter: blur(12px);
            border-radius: 60px;
            padding: 0.8rem 1.2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .menu-btn {
            background: transparent;
            border: none;
            color: #ddd;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            border-radius: 40px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .menu-btn i {
            font-size: 1rem;
        }
        .menu-btn.active {
            background: linear-gradient(95deg, #FF3CAC, #784BA0);
            color: white;
            box-shadow: 0 0 8px rgba(255,60,172,0.6);
        }
        .menu-btn:hover:not(.active) {
            background: rgba(255, 60, 172, 0.2);
            color: white;
            transform: translateY(-2px);
        }

        .card {
            background: rgba(15, 10, 30, 0.7);
            backdrop-filter: blur(12px);
            border-radius: 32px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            overflow: hidden;
            transition: all 0.3s;
            margin-bottom: 2rem;
        }
        .card-header {
            padding: 1.4rem 1.8rem;
            background: rgba(0,0,0,0.4);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .card-header i {
            font-size: 1.9rem;
        }
        .card-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
        }
        .card-body {
            padding: 1.8rem;
        }
        .input-group {
            margin-bottom: 1.3rem;
        }
        .input-group label {
            display: block;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #cdc9ff;
        }
        .input-group input, .input-group textarea, .input-group select {
            width: 100%;
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 12px 18px;
            border-radius: 24px;
            font-size: 0.9rem;
            color: white;
            font-family: 'Inter', monospace;
            transition: all 0.2s;
        }
        .input-group textarea {
            min-height: 80px;
            resize: vertical;
        }
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #FF3CAC;
            box-shadow: 0 0 0 3px rgba(255,60,172,0.3);
        }
        .method-toggle {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            justify-content: center;
        }
        .method-btn {
            flex: 1;
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 0.8rem;
            border-radius: 40px;
            cursor: pointer;
            text-align: center;
            font-weight: bold;
            transition: all 0.2s;
            color: #ccc;
        }
        .method-btn.active {
            background: linear-gradient(95deg, #FF3CAC, #784BA0);
            color: white;
            border-color: transparent;
            box-shadow: 0 0 12px rgba(255,60,172,0.5);
        }
        .method-btn i {
            margin-right: 8px;
        }
        button.submit-btn {
            width: 100%;
            background: linear-gradient(95deg, #FF3CAC, #784BA0);
            border: none;
            padding: 12px;
            border-radius: 40px;
            font-weight: bold;
            font-size: 1rem;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.25s;
            margin-top: 12px;
        }
        button.submit-btn:hover {
            transform: scale(0.98);
            background: linear-gradient(95deg, #ff57b9, #8f63c7);
        }
        .result-area {
            margin-top: 1.5rem;
            background: #0a0518cc;
            border-radius: 24px;
            padding: 1rem;
            border: 1px solid rgba(255,255,255,0.15);
            font-family: monospace;
            font-size: 0.8rem;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 280px;
            overflow-y: auto;
        }
        .loading {
            color: #ffbf69;
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .error-text {
            color: #ff8383;
            border-left: 3px solid #ff3c3c;
            padding-left: 10px;
        }
        .credits {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(0,0,0,0.4);
            border-radius: 30px;
            backdrop-filter: blur(5px);
        }
        .credits p {
            margin-bottom: 0.8rem;
            font-size: 0.9rem;
            color: #ccc;
        }
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        .social-icons a {
            color: #fff;
            font-size: 1.8rem;
            transition: transform 0.2s, color 0.2s;
            display: inline-block;
        }
        .social-icons a:hover {
            transform: scale(1.1);
            color: #FF3CAC;
        }
        footer {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.7rem;
            opacity: 0.5;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 700px) {
            body { padding: 1rem; }
            .hero h1 { font-size: 2.2rem; }
            .menu-btn { padding: 0.4rem 0.8rem; font-size: 0.75rem; }
            .method-btn { font-size: 0.8rem; padding: 0.6rem; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1><i class="fas fa-crown"></i> RIZERxPROFILE</h1>
        <div class="tag"><i class="fas fa-bolt"></i> ITEM MANAGER & LONG BIO</div>
    </div>

    <!-- Top Menu -->
    <div class="top-menu">
        <button class="menu-btn active" data-feature="guest"><i class="fas fa-user-secret"></i> GUEST ITEM ADD</button>
        <button class="menu-btn" data-feature="jwt"><i class="fas fa-token"></i> JWT ITEM ADD</button>
        <button class="menu-btn" data-feature="access"><i class="fas fa-key"></i> ACCESS TOKEN ITEM ADD</button>
        <button class="menu-btn" data-feature="accessToJwt"><i class="fas fa-exchange-alt"></i> ACCESS → JWT</button>
        <button class="menu-btn" data-feature="guestToCreds"><i class="fas fa-dna"></i> GUEST → TOKENS</button>
        <button class="menu-btn" data-feature="longBio"><i class="fas fa-paragraph"></i> LONG BIO</button>
    </div>

    <!-- Dynamic Form Area -->
    <div id="dynamicForm" class="card">
        <div class="card-header">
            <i id="formIcon" class="fas fa-user-secret"></i>
            <h2 id="formTitle">GUEST ITEM ADD</h2>
        </div>
        <div class="card-body" id="formBody">
            <!-- Forms will be injected here -->
        </div>
    </div>

    <!-- Credits Section -->
    <div class="credits">
        <p><strong>OWNER & DEVELOPER</strong><br>RIZERxPROFILE</p>
        <div class="social-icons">
            <a href="https://t.me/Beotherjk" target="_blank" title="Telegram Profile"><i class="fab fa-telegram"></i></a>
            <a href="https://t.me/beotherjkman" target="_blank" title="Telegram Channel"><i class="fab fa-telegram-plane"></i></a>
            <a href="https://t.me/beotherjkmans" target="_blank" title="Telegram Group"><i class="fab fa-telegram"></i><span style="font-size:0.8rem;"> Group</span></a>
            <a href="https://www.youtube.com/@darkdevil14890" target="_blank" title="YouTube"><i class="fab fa-youtube"></i></a>
            <a href="https://www.tiktok.com/@darkdevil148990" target="_blank" title="TikTok"><i class="fab fa-tiktok"></i></a>
        </div>
        <p style="margin-top: 0.5rem; font-size:0.8rem;">Telegram: @Beotherjk | Channel: @beotherjkman | Group: @beotherjkmans</p>
    </div>
    <footer>
        <i class="fas fa-shield-alt"></i> RIZERxPROFILE • All-in-one • No extra files
    </footer>
</div>

<script>
    let currentFeature = 'guest';

    function loadFeature(feature) {
        currentFeature = feature;
        fetch(`/api/get_form?feature=${feature}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('formIcon').className = data.icon;
                document.getElementById('formTitle').innerText = data.title;
                document.getElementById('formBody').innerHTML = data.html;
                attachFormHandlers(feature);
            })
            .catch(err => console.error('Error loading form:', err));
    }

    function attachFormHandlers(feature) {
        if (feature === 'guest') {
            const btn = document.getElementById('submitGuest');
            if (btn) btn.onclick = () => {
                const uid = document.getElementById('guestUid').value.trim();
                const pwd = document.getElementById('guestPwd').value;
                if (!uid || !pwd) return showResult('guestResult', 'UID and Password required', true);
                callApi('/api/guest_login', { uid, password: pwd }, 'guestResult', 'Authenticating...');
            };
        } else if (feature === 'jwt') {
            const btn = document.getElementById('submitJwt');
            if (btn) btn.onclick = () => {
                const token = document.getElementById('jwtToken').value.trim();
                if (!token) return showResult('jwtResult', 'JWT token required', true);
                callApi('/api/jwt_login', { token }, 'jwtResult', 'Verifying...');
            };
        } else if (feature === 'access') {
            const btn = document.getElementById('submitAccess');
            if (btn) btn.onclick = () => {
                const token = document.getElementById('accessToken').value.trim();
                if (!token) return showResult('accessResult', 'Access token required', true);
                callApi('/api/access_login', { access_token: token }, 'accessResult', 'Processing...');
            };
        } else if (feature === 'accessToJwt') {
            const btn = document.getElementById('submitAccessToJwt');
            if (btn) btn.onclick = () => {
                const token = document.getElementById('accessToJwtInput').value.trim();
                if (!token) return showResult('convertJwtResult', 'Access token required', true);
                callApi('/api/access_to_jwt', { access_token: token }, 'convertJwtResult', 'Converting...');
            };
        } else if (feature === 'guestToCreds') {
            const btn = document.getElementById('submitGuestToCreds');
            if (btn) btn.onclick = () => {
                const uid = document.getElementById('guestCredsUid').value.trim();
                const pwd = document.getElementById('guestCredsPwd').value;
                if (!uid || !pwd) return showResult('guestCredsResult', 'UID and Password required', true);
                callApi('/api/guest_to_creds', { uid, password: pwd }, 'guestCredsResult', 'Generating...');
            };
        } else if (feature === 'longBio') {
            // Attach method toggle buttons
            const guestBtn = document.getElementById('methodGuest');
            const jwtBtn = document.getElementById('methodJwt');
            const guestFields = document.getElementById('guestFields');
            const jwtFields = document.getElementById('jwtFields');
            const submitBtn = document.getElementById('submitLongBio');
            let currentMethod = 'guest'; // default

            function updateMethod(method) {
                currentMethod = method;
                if (method === 'guest') {
                    guestBtn.classList.add('active');
                    jwtBtn.classList.remove('active');
                    guestFields.style.display = 'block';
                    jwtFields.style.display = 'none';
                } else {
                    jwtBtn.classList.add('active');
                    guestBtn.classList.remove('active');
                    guestFields.style.display = 'none';
                    jwtFields.style.display = 'block';
                }
            }

            if (guestBtn && jwtBtn) {
                guestBtn.onclick = () => updateMethod('guest');
                jwtBtn.onclick = () => updateMethod('jwt');
                // initial
                updateMethod('guest');
            }

            if (submitBtn) {
                submitBtn.onclick = () => {
                    const bio = document.getElementById('bioText').value.trim();
                    if (!bio) return showResult('longBioResult', 'Bio text required', true);
                    if (currentMethod === 'guest') {
                        const uid = document.getElementById('bioUid').value.trim();
                        const pwd = document.getElementById('bioPwd').value;
                        if (!uid || !pwd) return showResult('longBioResult', 'Guest UID and Password required', true);
                        callApi('/api/long_bio_guest', { bio, uid, password: pwd }, 'longBioResult', 'Uploading bio (guest)...');
                    } else {
                        const jwt = document.getElementById('bioJwt').value.trim();
                        if (!jwt) return showResult('longBioResult', 'JWT token required', true);
                        callApi('/api/long_bio_jwt', { bio, jwt }, 'longBioResult', 'Uploading bio (JWT)...');
                    }
                };
            }
        }
    }

    function showResult(elementId, message, isError = false) {
        const el = document.getElementById(elementId);
        if (el) {
            if (isError) el.innerHTML = `<div class="error-text">${escapeHtml(message)}</div>`;
            else el.innerHTML = `<div>${escapeHtml(message)}</div>`;
        }
    }

    async function callApi(endpoint, payload, resultElementId, loadingMsg) {
        const resultEl = document.getElementById(resultElementId);
        if (!resultEl) return;
        resultEl.innerHTML = `<div class="loading"><i class="fas fa-spinner fa-pulse"></i> ${loadingMsg}</div>`;
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (data.error) {
                resultEl.innerHTML = `<div class="error-text">Error: ${escapeHtml(data.error)}</div>`;
            } else {
                resultEl.innerHTML = `<pre style="margin:0; white-space:pre-wrap;">${escapeHtml(data.result)}</pre>`;
            }
        } catch (err) {
            resultEl.innerHTML = `<div class="error-text">Request failed: ${err.message}</div>`;
        }
    }

    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }

    document.querySelectorAll('.menu-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const feature = btn.getAttribute('data-feature');
            if (feature === currentFeature) return;
            document.querySelectorAll('.menu-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadFeature(feature);
        });
    });

    loadFeature('guest');
</script>
</body>
</html>
"""

# ---------- API ROUTES ----------
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get_form', methods=['GET'])
def get_form():
    """Return HTML and metadata for the selected feature."""
    feature = request.args.get('feature', 'guest')
    forms = {
        'guest': {
            'icon': 'fas fa-user-secret',
            'title': 'GUEST ITEM ADD',
            'html': '''
                <div class="input-group">
                    <label><i class="fas fa-id-card"></i> UID</label>
                    <input type="text" id="guestUid" placeholder="Enter Guest UID">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-key"></i> Password</label>
                    <input type="password" id="guestPwd" placeholder="Guest Password">
                </div>
                <button class="submit-btn" id="submitGuest"><i class="fas fa-paper-plane"></i> ADD PROFILE</button>
                <div class="result-area" id="guestResult">⚡ waiting for action...</div>
            '''
        },
        'jwt': {
            'icon': 'fas fa-token',
            'title': 'JWT ITEM ADD',
            'html': '''
                <div class="input-group">
                    <label>JWT Token</label>
                    <input type="text" id="jwtToken" placeholder="eyJhbGciOiJIUzI1NiIs...">
                </div>
                <button class="submit-btn" id="submitJwt"><i class="fas fa-rocket"></i> ADD PROFILE</button>
                <div class="result-area" id="jwtResult">✨ enter token and submit</div>
            '''
        },
        'access': {
            'icon': 'fas fa-key',
            'title': 'ACCESS TOKEN ITEM ADD',
            'html': '''
                <div class="input-group">
                    <label>Access Token</label>
                    <input type="text" id="accessToken" placeholder="Access Token">
                </div>
                <button class="submit-btn" id="submitAccess"><i class="fas fa-arrow-right-to-bracket"></i> ADD PROFILE</button>
                <div class="result-area" id="accessResult">🔑 paste access token</div>
            '''
        },
        'accessToJwt': {
            'icon': 'fas fa-exchange-alt',
            'title': 'ACCESS → JWT',
            'html': '''
                <div class="input-group">
                    <label>Access Token</label>
                    <input type="text" id="accessToJwtInput" placeholder="access_token here">
                </div>
                <button class="submit-btn" id="submitAccessToJwt"><i class="fas fa-sync-alt"></i> CONVERT TO JWT</button>
                <div class="result-area" id="convertJwtResult">⚙️ get JWT from access token</div>
            '''
        },
        'guestToCreds': {
            'icon': 'fas fa-dna',
            'title': 'GUEST → TOKENS',
            'html': '''
                <div class="input-group">
                    <label>Guest UID</label>
                    <input type="text" id="guestCredsUid" placeholder="UID">
                </div>
                <div class="input-group">
                    <label>Guest Password</label>
                    <input type="password" id="guestCredsPwd" placeholder="Password">
                </div>
                <button class="submit-btn" id="submitGuestToCreds"><i class="fas fa-magic"></i> GET JWT & ACCESS</button>
                <div class="result-area" id="guestCredsResult">🧪 generate JWT + access token</div>
            '''
        },
        'longBio': {
            'icon': 'fas fa-paragraph',
            'title': 'LONG BIO',
            'html': '''
                <div class="method-toggle">
                    <div id="methodGuest" class="method-btn active"><i class="fas fa-user"></i> Guest Credentials</div>
                    <div id="methodJwt" class="method-btn"><i class="fas fa-token"></i> JWT Token</div>
                </div>
                <div class="input-group">
                    <label>Bio Text</label>
                    <textarea id="bioText" placeholder="Write your long bio here..."></textarea>
                </div>
                <div id="guestFields">
                    <div class="input-group">
                        <label>Guest UID</label>
                        <input type="text" id="bioUid" placeholder="UID">
                    </div>
                    <div class="input-group">
                        <label>Guest Password</label>
                        <input type="password" id="bioPwd" placeholder="Password">
                    </div>
                </div>
                <div id="jwtFields" style="display:none;">
                    <div class="input-group">
                        <label>JWT Token</label>
                        <input type="text" id="bioJwt" placeholder="JWT token">
                    </div>
                </div>
                <button class="submit-btn" id="submitLongBio"><i class="fas fa-cloud-upload-alt"></i> UPLOAD BIO</button>
                <div class="result-area" id="longBioResult">📄 ready</div>
            '''
        }
    }
    return jsonify(forms.get(feature, forms['guest']))

# All API endpoints (unchanged)
@app.route('/api/guest_login', methods=['POST'])
def api_guest_login():
    data = request.get_json()
    uid = data.get('uid', '').strip()
    password = data.get('password', '').strip()
    if not uid or not password:
        return jsonify({'error': 'UID and password are required'}), 400
    result = guest_login(uid, password)
    return jsonify({'result': result})

@app.route('/api/jwt_login', methods=['POST'])
def api_jwt_login():
    data = request.get_json()
    token = data.get('token', '').strip()
    if not token:
        return jsonify({'error': 'JWT token is required'}), 400
    result = jwt_login(token)
    return jsonify({'result': result})

@app.route('/api/access_login', methods=['POST'])
def api_access_login():
    data = request.get_json()
    access_token = data.get('access_token', '').strip()
    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400
    result = access_token_login(access_token)
    return jsonify({'result': result})

@app.route('/api/access_to_jwt', methods=['POST'])
def api_access_to_jwt():
    data = request.get_json()
    access_token = data.get('access_token', '').strip()
    if not access_token:
        return jsonify({'error': 'Access token required'}), 400
    result = access_to_jwt(access_token)
    return jsonify({'result': result})

@app.route('/api/guest_to_creds', methods=['POST'])
def api_guest_to_creds():
    data = request.get_json()
    uid = data.get('uid', '').strip()
    password = data.get('password', '').strip()
    if not uid or not password:
        return jsonify({'error': 'UID and password required'}), 400
    result = guest_to_creds(uid, password)
    return jsonify({'result': result})

@app.route('/api/long_bio_guest', methods=['POST'])
def api_long_bio_guest():
    data = request.get_json()
    bio = data.get('bio', '').strip()
    uid = data.get('uid', '').strip()
    password = data.get('password', '').strip()
    if not bio or not uid or not password:
        return jsonify({'error': 'Bio, UID, and password are required'}), 400
    result = long_bio_guest(bio, uid, password)
    return jsonify({'result': result})

@app.route('/api/long_bio_jwt', methods=['POST'])
def api_long_bio_jwt():
    data = request.get_json()
    bio = data.get('bio', '').strip()
    jwt = data.get('jwt', '').strip()
    if not bio or not jwt:
        return jsonify({'error': 'Bio and JWT token are required'}), 400
    result = long_bio_jwt(bio, jwt)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
