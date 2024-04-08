// ChatWindow.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function ChatWindow({ senderUsername }) {
    const { recipientUsername } = useParams();
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const fetchMessages = async () => {
        try {
            const response = await axios.get(`https://chin-ec530-project2-2.onrender.com/get_messages?sender_username=${senderUsername}&recipient_username=${recipientUsername}`);
            setMessages(response.data.messages);
            console.log(response.data.messages);
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    };

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get(`https://chin-ec530-project2-2.onrender.com/get_messages?sender_username=${senderUsername}&recipient_username=${recipientUsername}`);
                setMessages(response.data.messages);
                console.log(response.data.messages);
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        fetchMessages();
        // Poll for new messages every 5 seconds
        const intervalId = setInterval(fetchMessages, 5000);
        return () => clearInterval(intervalId);
    }, [senderUsername, recipientUsername]);

    const handleMessageSend = async () => {
        try {
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
        <div className="chat-window" style={{ margin: "3%",}} >
            <h2>Chat with User {recipientUsername}</h2>
            <div className="messages">
                {messages.map((message, index) => (
                    <div key={index} className="message">
                        <p>{message.Timestamp}: <b>{message.SenderUsername === senderUsername ? 'You' : `${recipientUsername}`}</b>: {message.MessageText}</p>
                    </div>
                ))}
            </div>
            <form onSubmit={handleMessageSend}>
                <div className="message-input">
                    <input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} />
                    <button type="submit">Send</button>
                </div>
            </form>
        </div>
    );
}

export default ChatWindow;
