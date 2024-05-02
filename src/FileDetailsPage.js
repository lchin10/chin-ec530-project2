import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
// import { Document, Page, pdfjs } from 'react-pdf';

function FileDetailsPage({ username, currUrl }) {
    const { filename } = useParams();
    const [fileInfo, setFileInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [metadataChecked, setMetadataChecked] = useState(false);
    const [translationChecked, setTranslationChecked] = useState(false);
    const [taggingChecked, setTaggingChecked] = useState(false);
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        document.title = `${filename} - Smart Document Analyzer`;
    }, [filename]);

    useEffect(() => {
        const getFileInfo = async () => {
            try {
                const response = await axios.post(currUrl + '/get_file_info', { username, filename });
                setFileInfo(response.data.file_info);
            } catch (error) {
                console.error('Error fetching file info:', error);
            }
        };
    
        getFileInfo();
    }, [username, filename, currUrl]);

    const handleMetadata = async () => {
        try {
            const response = await axios.post(currUrl + '/get_metadata', { username, filename });
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

    const handleTranslate = async () => {
        try {
            const response = await axios.post(currUrl + '/doc_to_text', { username, filename });
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
            const response = await axios.post(currUrl + '/tag_keywords_topics', { username, filename });
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
        setProcessing(true); 

        if (metadataChecked) {
            await handleMetadata();
        }
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
                    Grab metadata:
                    <input
                        type="checkbox"
                        checked={metadataChecked}
                        onChange={() => setMetadataChecked(!metadataChecked)}
                    />
                </label>
                <br />
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
            <p>{processing ? 'Parsing file. Information will be shown on this page when it is finished.' : ''}</p>
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
