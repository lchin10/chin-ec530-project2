import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FileDetailsPage({ username, filename }) {
    const [fileInfo, setFileInfo] = useState(null);

    useEffect(() => {
        const getFileInfo = async () => {
            try {
                const response = await axios.post('https://chin-ec530-project2-2.onrender.com/get_file_info', { username, filename });
                setFileInfo(response.data.fileInfo);
            } catch (error) {
                console.error('Error fetching file info:', error);
            }
        };
    
        getFileInfo();
    }, [username, filename]);

    const handleTranslate = async () => {
        // Make API call to translate doc to text
    };

    const handleTag = async () => {
        // Make API call to tag doc with keywords/topics
    };

    if (!fileInfo) {
        return <p>Loading file information...</p>;
    }

    return (
        <div>
            <h1>Current Information:</h1>
            <p>{fileInfo}</p>
            <h2>What would you like to do with this file?</h2>
            <button onClick={handleTranslate}>Translate doc to text</button>
            <button onClick={handleTag}>Tag doc with keywords/topics</button>
        </div>
    );
}

export default FileDetailsPage;
