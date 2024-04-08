// ChatWindow.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function ChatWindow({ senderUsername }) {
    const { recipientUsername } = useParams();
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get(`https://chin-ec530-project2-2.onrender.com/get_messages?sender_username=${senderUsername}&recipient_username=${recipientUsername}`);
                setMessages(response.data.messages);
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        fetchMessages();
    }, [senderUsername, recipientUsername]);

    const fetchMessages = async () => {
        try {
            const response = await axios.get(`https://chin-ec530-project2-2.onrender.com/get_messages?sender_username=${senderUsername}&recipient_username=${recipientUsername}`);
            setMessages(response.data.messages);
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    };

    const handleMessageSend = async () => {
        try {
            console.log(senderUsername);
            console.log(recipientUsername);
            await axios.post('https://chin-ec530-project2-2.onrender.com/send_message', {
                sender_username: senderUsername,
                recipient_username: recipientUsername,
                message_text: newMessage
            });
            // Fetch messages again after sending a new message
            setNewMessage('');
            fetchMessages();
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div className="chat-window">
            <h2>Chat with User {recipientUsername}</h2>
            <div className="messages">
                {messages.map((message, index) => (
                    <div key={index} className="message">
                        <p>{message.sender_username === senderUsername ? 'You' : `User ${recipientUsername}`}: {message.message_text}</p>
                    </div>
                ))}
            </div>
            <div className="message-input">
                <input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} />
                <button onClick={handleMessageSend}>Send</button>
            </div>
        </div>
    );
}

export default ChatWindow;
