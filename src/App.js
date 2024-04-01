
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import AppPage from './AppPage';
import WelcomePage from './WelcomePage';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setGlobalUsername] = useState('');
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
                                    <button onClick={() => setLoggedIn(false)}>Logout</button>
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
                    <Route path="/chin-ec530-project2/" element={<AppPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
