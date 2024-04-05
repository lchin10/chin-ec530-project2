
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import AppPage from './AppPage';
import WelcomePage from './WelcomePage';
import FileDetailsPage from './FileDetailsPage';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true');
    const [username, setGlobalUsername] = useState(localStorage.getItem('username') || '');

    const handleLogout = () => {
        setLoggedIn(false);
        setGlobalUsername('');
        // Remove logged-in state and username from localStorage
        localStorage.removeItem('loggedIn');
        localStorage.removeItem('username');
        window.location.href = '/chin-ec530-project2/';
    };

    useEffect(() => {
        // Store login state and username in localStorage
        localStorage.setItem('loggedIn', loggedIn);
        localStorage.setItem('username', username);
    }, [loggedIn, username]);

    return (
        <Router>
            <div>
                <nav>
                    <ul>
                        <li>
                            <Link to="/chin-ec530-project2/">Home</Link>
                        </li>
                        {loggedIn ? (
                            <>
                                <li>
                                    <Link to="/chin-ec530-project2/welcome">Welcome, {username}!</Link>
                                </li>
                                <li>
                                    <button onClick={handleLogout}>Logout</button>
                                </li>
                            </>
                        ) : (
                            <>
                                <li>
                                    <Link to="/chin-ec530-project2/register">Register</Link>
                                </li>
                                <li>
                                    <Link to="/chin-ec530-project2/login">Login</Link>
                                </li>
                            </>
                        )}
                    </ul>
                </nav>

                <Routes>
                    <Route path="/chin-ec530-project2/register" element={<RegisterPage setLoggedIn={setLoggedIn} setGlobalUsername={setGlobalUsername} />} />
                    <Route path="/chin-ec530-project2/login" element={<LoginPage setLoggedIn={setLoggedIn} setGlobalUsername={setGlobalUsername} />} />
                    <Route path="/chin-ec530-project2/welcome" element={loggedIn ? <WelcomePage username={username} /> : <LoginPage setLoggedIn={setLoggedIn} />} />
                    <Route path="/chin-ec530-project2/welcome/:filename" element={<FileDetailsPage />} />
                    <Route path="/chin-ec530-project2/" element={<AppPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
