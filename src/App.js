
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
                            <Link to="/chin-ec530-project2/">Home</Link>
                        </li>
                        <li>
                            <Link to="/chin-ec530-project2/register">Register</Link>
                        </li>
                        <li>
                            <Link to="/chin-ec530-project2/login">Login</Link>
                        </li>
                    </ul>
                </nav>

                <Routes>
                    <Route path="/chin-ec530-project2/register" element={<RegisterPage />} />
                    <Route path="/chin-ec530-project2/login" element={<LoginPage setLoggedIn={setLoggedIn} />} />
                    <Route path="/chin-ec530-project2/welcome" element={loggedIn ? <AppPage /> : <LoginPage setLoggedIn={setLoggedIn} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
