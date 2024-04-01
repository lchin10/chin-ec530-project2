// LoginPage.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginPage({ setLoggedIn, setGlobalUsername }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('https://0.0.0.0:5000/login', {
                username,
                password
            });

            const data = response.data;
            if (data.token) {
                console.log(data.token); // Handle success message
                // localStorage.setItem('token', data.token);
                setLoggedIn(true);
                setGlobalUsername(username);
                // Redirect the user to the welcome page
                navigate('/chin-ec530-project2/welcome');
            } else {
                console.log(data.error);
                setError(data.error); // Set error message
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data.error) {
                const error_message = 'An error occurred:'.concat(' ', error.response.data.error)
                console.log(error.response.data.error);
                setError(error_message); // Set error message from API response
            } else {
                console.error('An error occurred:', error);
                setError('An error occurred. Please try again later.');
            }
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LoginPage;