from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests

app = Flask(__name__)

# URL dei microservizi
AUTHENTICATION_SERVICE_URL = "http://localhost:5000"
CONTENT_MANAGEMENT_SERVICE_URL = "http://localhost:5001"

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Pagina di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Invio della richiesta POST all'auth service per il login
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/login", json={'email': email, 'password': password})
        if response.status_code == 200:
            token = response.json().get('access_token')
            return redirect(url_for('home', token=token))
        else:
            return "Login Failed", 401

    return render_template('login.html')

# Pagina di registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Invio della richiesta POST all'auth service per la registrazione
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/register", json={'email': email, 'password': password})
        if response.status_code == 201:
            token = response.json().get('access_token')
            return redirect(url_for('home', token=token))
        else:
            return response.json().get('error', 'Registration failed'), response.status_code

    return render_template('register.html')

# Pagina principale
@app.route('/home')
def home():
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # Chiamata al servizio di gestione dei contenuti per ottenere la home
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content", headers=headers)
    if response.status_code == 200:
        contents = response.json()
        return render_template('home.html', contents=contents, token=token)
    else:
        return "Unable to fetch content", response.status_code

# Pagina per visualizzare dettagli di un contenuto specifico
@app.route('/content/<int:content_id>', methods=['GET'])
def content_detail(content_id):
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # Chiamata al servizio di gestione dei contenuti per ottenere i dettagli
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}", headers=headers)
    if response.status_code == 200:
        content = response.json()
        return render_template('content_detail.html', content=content, token=token)
    else:
        return "Content not found", response.status_code

# Pagina per lo streaming del contenuto
@app.route('/content/<int:content_id>/stream', methods=['GET'])
def stream_content(content_id):
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # Chiamata al servizio di gestione per lo streaming del contenuto
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}/stream", headers=headers)
    if response.status_code == 200:
        content = response.json()
        return render_template('stream.html', content=content)
    else:
        return "Unable to stream content", response.status_code

# Pagina per il download del contenuto
@app.route('/content/<int:content_id>/download', methods=['POST'])
def download_content(content_id):
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # Chiamata al servizio di gestione per il download del contenuto
    response = requests.post(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}/download", headers=headers)
    if response.status_code == 200:
        content = response.json()
        return render_template('download.html', content=content)
    else:
        return "Unable to download content", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
