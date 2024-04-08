
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import AppPage from './AppPage';
import WelcomePage from './WelcomePage';
import FileDetailsPage from './FileDetailsPage';
import ChatWindow from './ChatWindow';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true');
    const [username, setGlobalUsername] = useState(localStorage.getItem('username') || '');
    const [onlineUsers, setOnlineUsers] = useState([]);

    const handleLogout = async () => {
        try {
            const response = await axios.post('https://chin-ec530-project2-2.onrender.com/logout', {
                username
            });

            const data = response.data;
            if (data.message) {
                console.log(data.message);
                setLoggedIn(false);
                setGlobalUsername('');
                // Remove logged-in state and username from localStorage
                localStorage.removeItem('loggedIn');
                localStorage.removeItem('username');
                window.location.href = '/chin-ec530-project2/';
            } else if (data.error) {
                console.log(data.error);
            }
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    useEffect(() => {
        // Store login state and username in localStorage
        localStorage.setItem('loggedIn', loggedIn);
        localStorage.setItem('username', username);
    }, [loggedIn, username]);

    useEffect(() => {
        const fetchOnlineUsers = async () => {
            try {
                const response = await axios.post('https://chin-ec530-project2-2.onrender.com/list_online_users');
                setOnlineUsers(response.data.online_users);
            } catch (error) {
                console.error('Error fetching online users:', error);
            }
        };

        fetchOnlineUsers();
        const intervalId = setInterval(fetchOnlineUsers, 5000); // Fetch every 5 seconds
        return () => clearInterval(intervalId);
    }, []);

    const handleChatOpen = (recipientUsername) => {
        window.location.href = `/chin-ec530-project2/chat/${recipientUsername}`;
    };

    return (
        <Router>
            <div style={{ display: 'flex' }}>
                <div style={{ flexGrow: 1 }}>
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
                        <Route path="/chin-ec530-project2/register" element={loggedIn ? <WelcomePage username={username} /> : <RegisterPage setLoggedIn={setLoggedIn} setGlobalUsername={setGlobalUsername} />} />
                        <Route path="/chin-ec530-project2/login" element={loggedIn ? <WelcomePage username={username} /> : <LoginPage setLoggedIn={setLoggedIn} setGlobalUsername={setGlobalUsername} />} />
                        <Route path="/chin-ec530-project2/welcome" element={loggedIn ? <WelcomePage username={username} /> : <AppPage />} />
                        <Route path="/chin-ec530-project2/welcome/:filename" element={<FileDetailsPage username={username} />} />
                        <Route path="/chin-ec530-project2/chat/:recipientUsername" element={<ChatWindow senderUsername={username} />} />
                        <Route path="/chin-ec530-project2/" element={<AppPage />} />
                    </Routes>
                </div>

                <div className="online-users" style={{ border: '2px solid #ccc', borderRadius: '5px', padding: '10px', marginLeft: '20px', margin: "5%",}} >
                    <h3>Online Users</h3>
                    <ul>
                        {onlineUsers.map((user, index) => (
                            <li key={index} onClick={() => handleChatOpen(user)}>
                                {user}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </Router>
    );
}

export default App;
