import logging
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head><title>Admin Portal - Authorized Personnel Only</title></head>
<body style="background-color:#f0f2f5; font-family:Arial; display:flex; justify-content:center; align-items:center; height:100vh;">
    <div style="background:white; padding:40px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <h2 style="color:#1a73e8;">Corporate Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" style="width:100%; padding:10px; margin-bottom:10px;"><br>
            <input type="password" name="password" placeholder="Password" style="width:100%; padding:10px; margin-bottom:20px;"><br>
            <button type="submit" style="width:100%; padding:10px; background:#1a73e8; color:white; border:none; border-radius:4px; cursor:pointer;">Login</button>
        </form>
    </div>
</body>
</html>
"""
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template_string(LOGIN_HTML)
    if request.method == 'POST':
        attacker_ip = request.remote_addr
        username = request.form.get('username','')
        password = request.form.get('password', '')
        log_message= f"ALERTA: intento de login desde {attacker_ip} | user: {username} | password: {password}"
        app.logger.warning(log_message)
        webhook_url = "http://n8n:5678/webhook-test/analisis-ataque"

        payload = {
        "source_ip": attacker_ip,
            "user_attempt": username,
            "pass_attempt": password,
            "user_agent": request.headers.get('User-Agent')
        }
    try: 
        requests.post(webhook_url, json=payload, timeout=1)
    except Exception as e:
        app.logger.error(f"No se pudo conectar a n8n: {e}")   
    return "Critical Error: Database Connection Failed. Please contact IT Support", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)