import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
// import { Document, Page, pdfjs } from 'react-pdf';

function FileDetailsPage({ username }) {
    const { filename } = useParams();
    const [fileInfo, setFileInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [translationChecked, setTranslationChecked] = useState(false);
    const [taggingChecked, setTaggingChecked] = useState(false);

    useEffect(() => {
        document.title = `${filename} - Smart Document Analyzer`;
    }, [filename]);

    useEffect(() => {
        const getFileInfo = async () => {
            try {
                const response = await axios.post('https://chin-ec530-project2-2.onrender.com/get_file_info', { username, filename });
                // const response = await axios.post('http://localhost:5000/get_file_info', { username, filename });
                setFileInfo(response.data.file_info);
            } catch (error) {
                console.error('Error fetching file info:', error);
            }
        };
    
        getFileInfo();
    }, [username, filename]);

    const handleTranslate = async () => {
        try {
            const response = await axios.post('https://chin-ec530-project2-2.onrender.com/doc_to_text', { username, filename });
            // const response = await axios.post('http://localhost:5000/doc_to_text', { username, filename });
            const data = response.data;
            if (data.message){
                console.log(data.message);
            } else {
                console.log(data.error);
            }
        } catch (error) {
            console.error('Error fetching file info:', error);
        }
    };

    const handleTag = async () => {
        try {
            const response = await axios.post('https://chin-ec530-project2-2.onrender.com/tag_keywords_topics', { username, filename });
            // const response = await axios.post('http://localhost:5000/tag_keywords_topics', { username, filename });
            const data = response.data;
            if (data.message){
                console.log(data.message);
            } else {
                console.log(data.error);
            }
        } catch (error) {
            console.error('Error fetching file info:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        if (translationChecked) {
            await handleTranslate();
        }
        if (taggingChecked) {
            await handleTag();
        }
        // window.location.reload();
        setLoading(false);
    };

    if (!fileInfo) {
        return <p>Loading file information...</p>;
    }

    return (
        <div style={{ margin: "3%", }}>
            <h2><u>{filename}</u></h2>
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
                <button type="submit" disabled={loading}>
                    {loading ? 'Loading...' : 'Confirm'}
                </button>
            </form>
            <h1>Current Information:</h1>
            {Object.keys(fileInfo).length > 0 ? (
                Object.entries(fileInfo).map(([key, value]) => (
                    // <p key={key}>{key}: {value}</p>
                    <details>
                        <summary className='text-info'> {key} </summary>
                        {value}
                    </details>
                ))
            ) : (
                <p>No information available for this file.</p>
            )}
        </div>
    );
}

export default FileDetailsPage;
