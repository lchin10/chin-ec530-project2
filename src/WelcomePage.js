// WelcomePage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function WelcomePage({ username }) {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [file, setFile] = useState(null);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [selectedFile, setSelectedFile] = useState(files.length > 0 ? files[0] : '');

    useEffect(() => {
        document.title = "Welcome - Smart Document Analyzer"
    }, [])

    useEffect(() => {
        const fetchFiles = async () => {
            try {
                // Make a request to fetch files
                const response = await axios.post('https://chin-ec530-project2-2.onrender.com/list_files', { username });
                // const response = await axios.post('http://localhost:5000/list_files', { username });
                setFiles(response.data.filenames);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching files:', error);
            }
        };
    
        fetchFiles(); // Call fetchFiles directly inside the effect
    
    }, [username]);

    const chooseFile = (e) => {
        setFile(e.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!file) {
            alert('Please choose a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Make a request to upload the file
            await axios.post(`https://chin-ec530-project2-2.onrender.com/upload_file/${username}`, formData, {
            // await axios.post(`http://localhost:5000/upload_file/${username}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            window.location.reload();
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const handleRemoveFile = async () => {
        if (files.length === 0) {
            alert('There are no files.');
            return;
        }

        setSelectedFile(files[0]);
        setShowConfirmation(true);
    };

    const confirmRemoveFile = async (e) => {
        e.preventDefault();
        try {
            await axios.post('https://chin-ec530-project2-2.onrender.com/remove_file', { username, file_title: selectedFile });
            // await axios.post('http://localhost:5000/remove_file', { username, file_title: selectedFile });
            window.location.reload();
        } catch (error) {
            console.error('Error removing file:', error);
        } finally {
            setFile(null);
            setShowConfirmation(false);
        }
    };

    return (
        <div style={{ margin: "3%", }}>
            <h1>Welcome, {username}!</h1>
            <h2>Files:</h2>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <>
                    <ul>
                        {files && files.length > 0 ? (
                            files.map((file, index) => (
                                <li key={index}>
                                    <Link to={`/chin-ec530-project2/welcome/${file}`}>{file}</Link>
                                </li>
                            ))
                        ) : (
                            <p>No files in your account.</p>
                        )}
                    </ul>
                    <input type="file" name="file" onChange={chooseFile} />
                    <button onClick={handleFileUpload} >Upload File</button><br></br><br></br>
                    {files.length > 0 ? (
                        <>
                            <button onClick={handleRemoveFile}>Remove File</button>
                            {showConfirmation && (
                                <div>
                                    <form onSubmit={confirmRemoveFile}>
                                        <select value={selectedFile} onChange={(e) => setSelectedFile(e.target.value)}>
                                            {files.map((file, index) => (
                                                <option key={index} value={file}>{file}</option>
                                            ))}
                                        </select>
                                        <button type="submit">Confirm</button>
                                    </form>
                                </div>
                            )}
                        </>
                    ) : null}
                </>
            )}
        </div>
    );
}

export default WelcomePage;