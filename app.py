from flask import Flask, render_template, redirect, url_for, request, session
from flask_cors import CORS
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# URLs of the microservices
AUTHENTICATION_SERVICE_URL = "http://localhost:5000"
CONTENT_MANAGEMENT_SERVICE_URL = "http://localhost:5001"

CORS(app)

# Homepage
@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('index.html')

# Home page after login
@app.route('/home')
def home():
    """
    Render the home page with a list of contents fetched from the content management service.
    Requires a valid token passed in the query string.
    """
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content", headers=headers)
    if response.status_code == 200:
        contents = response.json()
        return render_template('home.html', contents=contents, token=token)
    else:
        return "Unable to fetch content", response.status_code

#Start AUTH service
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Render the login page and handle the login process.
    Send a request to the authentication service to log in the user.
    If successful, redirects to the home page with the token as query parameter.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/login", json={'email': email, 'password': password})
        if response.status_code == 200:
            token = response.json().get('access_token')
            return redirect(url_for('home', token=token))
        else:
            return "Login Failed", 401

    return render_template('login.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Render the registration page and handle user registration.
    Send a request to the authentication service to register the user.
    If successful, redirects to the home page with the token as query parameter.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/register", json={'email': email, 'password': password})
        if response.status_code == 201:
            token = response.json().get('access_token')
            return redirect(url_for('home', token=token))
        else:
            return response.json().get('error', 'Registration failed'), response.status_code

    return render_template('register.html')

# Reset password Page
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """
    Render the reset password page and handle the password reset process.
    Send a request to the authentication service to initiate a password reset for the user.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            return "Please provide a valid email.", 400
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/reset-password", json={'email': email})
        if response.status_code == 200:
            return "Password reset email sent. Please check your inbox.", 200
        elif response.status_code == 404:
            return "User not found.", 404
        else:
            return "An error occurred.", response.status_code
        
    return render_template('reset_password.html')


# Logout user
@app.route('/logout', methods=['GET'])
def logout():
    """
    Handle the logout process by removing the token from the session.
    Send a request to the authentication service to log out the user.
    """
    token = session.get('access_token')
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/logout", headers=headers)
        if response.status_code == 200:
            session.pop('access_token', None)  #Remove token
            return redirect(url_for('index'))
        else:
            return "Logout failed", response.status_code
    return redirect(url_for('index'))


#Start CONTENT_MANAGMENT service
# Page to view content details
@app.route('/content/<int:content_id>', methods=['GET'])
def content_detail(content_id):
    """
    Render the page to show details of a specific content.
    Send a request to the content management service to fetch the content details by ID.
    """
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}", headers=headers)
    if response.status_code == 200:
        content = response.json()
        return render_template('content_detail.html', content=content, token=token)
    else:
        return "Content not found", response.status_code
        

# # Page to view all contents
@app.route('/content', methods=['GET'])
def content():
    """
    Render the page to view all available content.
    Send a request to the content management service to fetch all content.
    """
    token = request.args.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    # Chiamata al servizio di gestione dei contenuti per ottenere la home
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content", headers=headers)
    if response.status_code == 200:
        contents = response.json()
        return render_template('all_content.html', contents=contents, token=token)

# Stream content page
@app.route('/content/<int:content_id>/stream', methods=['GET'])
def stream_content(content_id):
    """
    Render the page to stream a specific content.
    Send a request to the content management service to get streaming information for the content by ID.
    """
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}/stream")
    if response.status_code == 200:
        content = response.json().get('content')
        return render_template('stream.html', content=content)
    else:
        return "Unable to stream content", response.status_code

# Download content page
@app.route('/content/<int:content_id>/download', methods=['GET'])
def download_content(content_id):
    """
    Render the page to download a specific content.
    Send a request to the content management service to get download information for the content by ID.
    """
    response = requests.get(f"{CONTENT_MANAGEMENT_SERVICE_URL}/content/{content_id}/stream")
    if response.status_code == 200:
        content = response.json().get('content')
        return render_template('download.html', content=content)
    else:
        return "Unable to stream content", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
