function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            //Save the token to next use
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/home';
        } else {
            alert(data.error || "Registration failed");
        }
    })
    .catch(error => console.error('Error:', error));
}
