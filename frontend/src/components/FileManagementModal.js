import React, {useState, useEffect, useCallback} from 'react';
import axios from 'axios';

const FileManagementModal = ({isOpen, onClose, onFileSelect, onDirectImport}) => {
    const [serverFiles, setServerFiles] = useState([]);
    const [currentDirectory, setCurrentDirectory] = useState('mmaforays');
    const [isServerWakingUp, setIsServerWakingUp] = useState(false);
    const [serverStartupMessage, setServerStartupMessage] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [selectedFileName, setSelectedFileName] = useState('');
    const [uploadFileName, setUploadFileName] = useState('');
    const apiUrl = process.env.REACT_APP_API_URL;

    const fetchserverfiles = useCallback(async () => {
        setIsServerWakingUp(true);
        setServerStartupMessage('Server is slowly waking up, check back in a minute');

        try {
            await axios.get(`${apiUrl}/wakeup`);
            try {
                const response = await axios.get(`${apiUrl}/list_csv_files?directory=${currentDirectory}`);
                setServerFiles(response.data.files);
                setIsServerWakingUp(false);
                setServerStartupMessage('');
            } catch (filesErr) {
                console.error('Error fetching files:', filesErr);
                if (filesErr.message.includes('CORS') || filesErr.message.includes('Network Error')) {
                    setServerStartupMessage('Server is starting up. Please wait a moment and try again...');
                } else {
                    setServerStartupMessage('Unable to fetch files. Please try again.');
                }
            }
        } catch (wakeupErr) {
            console.error('Server wake-up error:', wakeupErr);
            setServerStartupMessage('Server is currently offline. Please try again in a few minutes.');
        }
    }, [apiUrl, currentDirectory]);

    useEffect(() => {
        if (isOpen) {
            fetchserverfiles();
        }
    }, [isOpen, fetchserverfiles]);

    const handleDirectoryChange = useCallback((directory) => {
        setCurrentDirectory(directory);
    }, []);

    const handleDirectImport = useCallback(async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setSelectedFileName(file.name);

        setIsProcessing(true);
        setServerStartupMessage('Processing file...');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${apiUrl}/upload_csv_json`, formData, {
                headers: {'Content-Type': 'multipart/form-data'}
            });

            if (response.data.records) {
                onDirectImport(response.data.records, file.name);
                onClose();
            }
        } catch (error) {
            console.error('Import error:', error);
            if (error.message.includes('CORS') || error.message.includes('Network Error')) {
                setServerStartupMessage('Server is starting up. Please try again in a moment.');
            } else {
                alert('File import failed');
            }
        } finally {
            setIsProcessing(false);
            setServerStartupMessage('');
        }
    }, [apiUrl, onDirectImport, onClose]);

   const handleFileUpload = useCallback(async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setUploadFileName(file.name);

        setIsServerWakingUp(true);
        setServerStartupMessage('Uploading file...');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('directory', 'uploads');

        try {
            await axios.post(`${apiUrl}/upload_csv`, formData, {
                headers: {'Content-Type': 'multipart/form-data'}
            });
            await fetchserverfiles();
            alert('File uploaded successfully');
        } catch (error) {
            console.error('Upload error:', error);
            if (error.message.includes('CORS') || error.message.includes('Network Error')) {
                setServerStartupMessage('Server is starting up. Please try again in a moment.');
            } else {
                alert('File upload failed');
                setIsServerWakingUp(false);
            }
        }
    }, [apiUrl, fetchserverfiles]);

    const handleFileSelect = useCallback(async (filename) => {
        try {
            await onFileSelect(filename, currentDirectory);
            onClose();
        } catch (error) {
            console.error('File selection error:', error);
            if (error.message.includes('CORS') || error.message.includes('Network Error')) {
                setServerStartupMessage('Server is starting up. Please try again in a moment.');
                setIsServerWakingUp(true);
            }
        }
    }, [currentDirectory, onFileSelect, onClose]);


    if (!isOpen) return null;

    return (
        <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="file-management-title"
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                backgroundColor: 'rgba(0,0,0,0.5)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 1000
            }}
        >
            <div
                style={{
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '10px',
                    width: '500px',
                    maxHeight: '80%',
                    overflowY: 'auto'
                }}
            >
                <h2 id="file-management-title">File Management</h2>

                {serverStartupMessage && (
                    <p style={{
                        color: '#ff0000',
                        textAlign: 'center',
                        padding: '10px',
                        margin: '10px 0',
                        backgroundColor: '#fff0f0',
                        borderRadius: '5px'
                    }}>
                        {serverStartupMessage}
                    </p>
                )}

                {!isServerWakingUp && !isProcessing && (
                    <>
                        <div style={{marginBottom: '20px'}}>
                            <h3>Select File</h3>
                            <div style={{marginBottom: '15px'}}>
                                <button
                                    onClick={() => handleDirectoryChange('mmaforays')}
                                    aria-label="Switch to MMAforays directory"
                                    style={{marginRight: '10px'}}
                                >
                                    MMAforays
                                </button>
                                <button
                                    onClick={() => handleDirectoryChange('uploads')}
                                    aria-label="Switch to Uploads directory"
                                >
                                    Uploads
                                </button>
                            </div>

                            <div style={{
                                border: '1px solid #eee',
                                borderRadius: '5px',
                                padding: '10px',
                                maxHeight: '200px',
                                overflowY: 'auto'
                            }}>
                                {serverFiles.map((file) => (
                                    <div
                                        key={file}
                                        style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            padding: '5px 0',
                                            borderBottom: '1px solid #eee'
                                        }}
                                    >
                                        <span style={{
                                            flex: 1,
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap',
                                            marginRight: '10px'
                                        }}>
                                            {file}
                                        </span>
                                        <button
                                            onClick={() => handleFileSelect(file)}
                                            aria-label={`Select ${file}`}
                                            style={{
                                                padding: '5px 10px',
                                                width: '80px',
                                                flexShrink: 0
                                            }}
                                        >
                                            Select
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div style={{marginBottom: '20px'}}>
                            <h3>Import iNaturalist CSV</h3>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px'
                            }}>
                                <label
                                    style={{
                                        padding: '8px 12px',
                                        backgroundColor: '#f0f0f0',
                                        borderRadius: '4px',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Choose File
                                    <input
                                        type="file"
                                        accept=".csv"
                                        onChange={handleDirectImport}
                                        style={{ display: 'none' }}
                                        aria-label="Import iNaturalist CSV file"
                                    />
                                </label>
                                {selectedFileName && (
                                    <span style={{ marginLeft: '10px' }}>
                                        {selectedFileName}
                                    </span>
                                )}
                            </div>
                            <p style={{fontSize: '0.9em', color: '#666', marginTop: '5px'}}>
                                Import directly without saving to server
                            </p>
                        </div>

                        <div style={{marginBottom: '20px'}}>
                            <h3>Upload and Save CSV</h3>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px'
                            }}>
                                <label
                                    style={{
                                        padding: '8px 12px',
                                        backgroundColor: '#f0f0f0',
                                        borderRadius: '4px',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Choose File
                                    <input
                                        type="file"
                                        accept=".csv"
                                        onChange={handleFileUpload}
                                        style={{ display: 'none' }}
                                        aria-label="Upload CSV file"
                                    />
                                </label>
                                {uploadFileName && (
                                    <span style={{ marginLeft: '10px' }}>
                                        {uploadFileName}
                                    </span>
                                )}
                            </div>
                        </div>
                    </>
                )}

                <div style={{display: 'flex', justifyContent: 'space-between', marginTop: '20px'}}>
                    <button
                        onClick={onClose}
                        aria-label="Close modal"
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#f0f0f0'
                        }}
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FileManagementModal;