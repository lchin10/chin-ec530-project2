// WelcomePage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function WelcomePage({ username }) {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [file, setFile] = useState(null);
    const [showConfirmation, setShowConfirmation] = useState(false);

    useEffect(() => {
        const fetchFiles = async () => {
            try {
                // Make a request to fetch files
                const response = await axios.post('http://localhost:5000/list_files', { username });
                setFiles(response.data.filenames);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching files:', error);
            }
        };
    
        fetchFiles(); // Call fetchFiles directly inside the effect
    
    }, [username]);

    const fetchFiles = async () => {
        try {
            // Make a request to fetch files
            const response = await axios.post('http://localhost:5000/list_files', { username });
            setFiles(response.data.filenames);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching files:', error);
        }
    };

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
            await axios.post(`http://localhost:5000/upload_file/${username}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Refresh the files list after successful upload
            fetchFiles();
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const handleRemoveFile = async () => {
        try {
            // Make a request to remove the selected file
            await axios.post('http://localhost:5000/remove_file', { username, file_title: file.name });
            
            // Refresh the files list after successful removal
            fetchFiles();
        } catch (error) {
            console.error('Error removing file:', error);
        } finally {
            // Reset selected file and confirmation state
            setFile(null);
            setShowConfirmation(false);
        }
    };

    return (
        <div>
            <h1>Welcome, {username}!</h1>
            <h2>Files:</h2>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <>
                    <ul>
                        {files && files.length > 0 ? (
                            (() => {
                                const fileItems = [];
                                for (let i = 0; i < files.length; i++) {
                                    fileItems.push(<li key={i}>{files[i]}</li>);
                                }
                                return fileItems;
                            })()
                        ) : (
                            <p>No files in your account.</p>
                        )}
                    </ul>
                    <input type="file" name="file" onChange={chooseFile} />
                    <button onClick={handleFileUpload} >Upload File</button><br></br><br></br>
                    <button onClick={() => handleRemoveFile()}>Remove File</button>
                    {showConfirmation && file && (
                        <div>
                            <p>Are you sure you want to remove {file.name}?</p>
                            <button onClick={handleRemoveFile}>Confirm</button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default WelcomePage;