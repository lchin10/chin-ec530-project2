import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function FileDetailsPage({ username }) {
    const { filename } = useParams();
    const [fileInfo, setFileInfo] = useState(null);
    const [translationChecked, setTranslationChecked] = useState(false);
    const [taggingChecked, setTaggingChecked] = useState(false);

    useEffect(() => {
        document.title = `${filename} - Smart Document Analyzer`;
    }, [filename]);

    useEffect(() => {
        const getFileInfo = async () => {
            try {
                const response = await axios.post('https://chin-ec530-project2-2.onrender.com/get_file_info', { username, filename });
                setFileInfo(response.data.file_info);
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (translationChecked) {
            await handleTranslate();
        }
        if (taggingChecked) {
            await handleTag();
        }
        window.location.reload();
    };

    if (!fileInfo) {
        return <p>Loading file information...</p>;
    }

    return (
        <div style={{ margin: "3%", }}>
            <h1>Current Information:</h1>
            {Object.keys(fileInfo).length > 0 ? (
                Object.entries(fileInfo).map(([key, value]) => (
                    <p key={key}>{key}: {value}</p>
                ))
            ) : (
                <p>No information available for this file.</p>
            )}
            <h2>What would you like to do with this file?</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Translate doc to text:
                    <input
                        type="checkbox"
                        checked={translationChecked}
                        onChange={() => setTranslationChecked(!translationChecked)}
                    />
                </label>
                <br />
                <label>
                    Tag doc with keywords/topics:
                    <input
                        type="checkbox"
                        checked={taggingChecked}
                        onChange={() => setTaggingChecked(!taggingChecked)}
                    />
                </label>
                <br />
                <button type="submit">Confirm</button>
            </form>
        </div>
    );
}

export default FileDetailsPage;
