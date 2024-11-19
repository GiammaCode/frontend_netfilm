from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_cors import CORS
import requests

app = Flask(__name__)

# URL dei microservizi
AUTHENTICATION_SERVICE_URL = "http://localhost:5000"
CONTENT_MANAGEMENT_SERVICE_URL = "http://localhost:5001"

CORS(app)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

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

###########################  AUTH #############################

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

# Pagina di registrazione ok
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

#pagina di reset
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            return "Please provide a valid email.", 400

        # Invio della richiesta POST all'auth service per il reset della password
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/reset-password", json={'email': email})
        
        if response.status_code == 200:
            return "Password reset email sent. Please check your inbox.", 200
        elif response.status_code == 404:
            return "User not found.", 404
        else:
            return "An error occurred.", response.status_code

    return render_template('reset_password.html')


# Logout dell'utente
@app.route('/logout', methods=['GET'])
def logout():
    token = session.get('access_token')
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        # Invio della richiesta di logout al servizio di autenticazione
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/logout", headers=headers)
        if response.status_code == 200:
            session.pop('access_token', None)  # Rimuovi il token dalla sessione
            return redirect(url_for('index'))
        else:
            return "Logout failed", response.status_code
    return redirect(url_for('index'))


##############################  CONTENT MANAGMENT #############################

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
