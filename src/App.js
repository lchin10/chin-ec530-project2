
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import AppPage from './AppPage';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    return (
        <Router>
            <div>
                <nav>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to="/register">Register</Link>
                        </li>
                        <li>
                            <Link to="/login">Login</Link>
                        </li>
                    </ul>
                </nav>

                <Routes>
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/login" element={<LoginPage setLoggedIn={setLoggedIn} />} />
                    <Route path="/" element={loggedIn ? <AppPage /> : <LoginPage setLoggedIn={setLoggedIn} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
