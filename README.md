# Frontend Application for Authentication and Content Management

This repository contains a Flask-based frontend application that interacts with two separate microservices: an **Authentication Service** and a **Content Management Service**. The frontend application allows users to register, log in, view available content, stream or download specific content, and manage their sessions.

## Overview

- **Programming Language**: Python 3
- **Framework**: Flask
- **Dependencies**: Flask-CORS, Requests
- **Services Used**: Authentication Service (running on `localhost:5000`), Content Management Service (running on `localhost:5001`)

## Features

1. **Authentication**:
   - Register new users.
   - Log in existing users.
   - Log out and manage user sessions.
   - Reset password functionality.

2. **Content Management**:
   - View all available content.
   - Get details about specific content.
   - Stream specific content.
   - Download specific content.

## Project Structure

```
frontend_netfilm/
|-- app.py                 # Main Flask application
|-- templates/             # HTML templates for various pages
    |-- index.html         # Index page
    |-- login.html         # Login page
    |-- register.html      # User registration page
    |-- reset_password.html # Password reset page
    |-- home.html          # Home page displaying available content
    |-- content_detail.html # Page showing details of specific content
    |-- stream.html        # Page for streaming specific content
    |-- download.html      # Page for downloading content
    |-- all_content.html   # Page displaying all content
|-- static/                # Static files (CSS, JavaScript, images)
```

## Endpoints

### Authentication Endpoints

1. **`/register`**: User Registration
   - Allows new users to register.
   - Sends a POST request to the Authentication Service (`/auth/register`).

2. **`/login`**: User Login
   - Logs in an existing user.
   - Sends a POST request to the Authentication Service (`/auth/login`).
   - Redirects to `/home` upon successful login.

3. **`/reset-password`**: Password Reset
   - Allows users to request a password reset email.
   - Sends a POST request to the Authentication Service (`/auth/reset-password`).

4. **`/logout`**: User Logout
   - Logs out the user.
   - Sends a POST request to the Authentication Service (`/auth/logout`).

### Content Management Endpoints

1. **`/home`**: Home Page
   - Displays a list of all available content fetched from the Content Management Service (`/content`).

2. **`/content`**: View All Content
   - Displays a page listing all available content.
   - Fetches data from the Content Management Service (`/content`).

3. **`/content/<int:content_id>`**: Content Detail Page
   - Displays detailed information about a specific content item.
   - Fetches details from the Content Management Service (`/content/<id>`).

4. **`/content/<int:content_id>/stream`**: Stream Content
   - Displays the streaming page for a specific content item.
   - Fetches streaming details from the Content Management Service (`/content/<id>/stream`).

5. **`/content/<int:content_id>/download`**: Download Content
   - Displays the download page for a specific content item.
   - Fetches download details from the Content Management Service (`/content/<id>/download`).

## How to Run the Project

### Prerequisites
- Python 3.x
- Install dependencies using `pip`:

  ```sh
  pip install Flask flask-cors requests
  ```

### Running the Application

1. **Start the Authentication Service**: Make sure that the Authentication Service is running on `localhost:5000`.
2. **Start the Content Management Service**: Make sure that the Content Management Service is running on `localhost:5001`.
3. **Run the Frontend Application**:

   ```sh
   python app.py
   ```

   The frontend will run on `http://localhost:8000`.

### Accessing the Application
- **Homepage**: Visit `http://localhost:8000/`.
- **Register or Log in** to access content.
- **Home Page** after logging in will show the available content for streaming and download.

## Dependencies
- **Flask**: Web framework used to create the application.
- **Flask-CORS**: Enables Cross-Origin Resource Sharing (CORS) for cross-origin requests.
- **Requests**: Python library used to make HTTP requests to the Authentication and Content Management services.

