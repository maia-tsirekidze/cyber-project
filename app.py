
from flask import Flask, render_template, request,jsonify
import requests
import socket 
from datetime import datetime
from urllib.parse import urlparse
from database import init_db, save_report

app = Flask(__name__)
init_db()
@app.route('/')

def index():
    return render_template('index.html')
@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    if url =="":
       return "No url provided",400
    elif not (url.startswith('http://')or url.startswith('https://')):
        return "invalid URL, must start with http:// or https://",400
    try:
        response = (requests.get(url, timeout=8,allow_redirects=True))
    except requests.exceptions.RequestException as a:
        return "error"
    headers=dict(response.headers)
    required_headers = [
        'Content-Security-Policy',
        'Strict-Transport-Security',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Referrer-Policy'
    ]
    warnings =[]
    for h in required_headers:
        if h not in headers:
            warnings.append(f'Missing header:{h}')
    
    try:
        hostname = urlparse(url).hostname
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "unknown"
# თარიღი
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#  პასუხი JSON
    report = {
        "url": url,
        "ip": ip_address,
        "report_time": report_time,
        "headers": headers,
        "warnings": warnings
    }
    save_report(report)
    return jsonify(report)
if __name__ == '__main__':
   app.run(debug=True)
