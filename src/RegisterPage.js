// RegisterPage.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const [username, setUsername] = useState('');
    const [hashed_password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
  
    const handleRegister = async (e) => {
        e.preventDefault();

        if (hashed_password !== confirmPassword) {
            setError('An error occurred: Passwords do not match')
        }
        else {
            try {
                const response = await axios.post('http://localhost:5000/registration', {
                    username,
                    hashed_password
                });
        
                const data = response.data;
                if (data.message) {
                    console.log(data.message); // Handle success message
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
        }
    };
  
    return (
        <div>
            <h2>Register</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleRegister}>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={hashed_password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default RegisterPage;
