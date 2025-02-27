// error-message.js
import React from "react";

const ErrorMessage = ({ message, onClose, retryable, onRetry }) => (
    <div style={{
        position: 'fixed',
        top: '20px',
        right: '20px',
        backgroundColor: '#ff4444',
        color: 'white',
        padding: '15px',
        borderRadius: '5px',
        zIndex: 1000,
        maxWidth: '300px'
    }}>
        <div style={{ marginBottom: '10px' }}>{message}</div>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            {retryable && (
                <button
                    onClick={onRetry}
                    style={{
                        backgroundColor: 'white',
                        color: '#ff4444',
                        border: 'none',
                        padding: '5px 10px',
                        marginRight: '10px',
                        cursor: 'pointer',
                        borderRadius: '3px'
                    }}
                >
                    Retry
                </button>
            )}
            <button
                onClick={onClose}
                style={{
                    background: 'none',
                    border: '1px solid white',
                    color: 'white',
                    padding: '5px 10px',
                    cursor: 'pointer',
                    borderRadius: '3px'
                }}
            >
                Close
            </button>
        </div>
    </div>
);
