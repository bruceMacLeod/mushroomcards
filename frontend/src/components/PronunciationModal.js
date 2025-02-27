import React from 'react';

const PronunciationModal = ({ pronunciationModalOpen, pronunciationText, setPronunciationModalOpen, isServerWakingUp }) => {
    if (!pronunciationModalOpen) return null;

    return (
        <div style={{
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
        }}>
            <div style={{
                backgroundColor: 'white',
                padding: '20px',
                borderRadius: '10px',
                width: '80%', // Adjusted width
                maxHeight: '80%', // Adjusted height
                overflowY: 'auto'
            }}>
                <h2>Pronunciation</h2>
                {isServerWakingUp ? (
                    <p style={{ color: '#ff0000', textAlign: 'center' }}>
                        Server is slowly waking up, should be ready in less than a minute.
                    </p>
                ) : (
                    <pre style={{
                        whiteSpace: 'pre-wrap',
                        wordWrap: 'break-word',
                        fontFamily: 'monospace',
                        backgroundColor: '#f4f4f4',
                        padding: '10px',
                        borderRadius: '5px'
                    }}>
                        {pronunciationText}
                    </pre>
                )}
                <button
                    onClick={() => setPronunciationModalOpen(false)}
                    style={{
                        marginTop: '10px',
                        padding: '10px 20px',
                        backgroundColor: '#f0f0f0',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                >
                    Close
                </button>
            </div>
        </div>
    );
};

export default PronunciationModal;