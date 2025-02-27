import React, { useEffect } from 'react';

const LargeImageModal = ({ isOpen, onClose, currentCard }) => {
    // Handle Escape key press
    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            window.addEventListener('keydown', handleKeyDown);
        }

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [isOpen, onClose]);

    // Early return if modal is not open or no card is provided
    if (!isOpen || !currentCard || !currentCard.image_url) return null;

    // Create the full-size image URL by replacing 'medium.jpg' with 'large.jpg'
    const largeImageUrl = currentCard.image_url.replace('medium', 'large');

    // Function to check if the attribution is a URL
    const isUrl = (string) => {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    };

    return (
        <div
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                backgroundColor: 'rgba(0,0,0,0.9)', // Dark overlay
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 1000,
                padding: '10px' // Reduced padding to maximize space
            }}
            onClick={onClose} // Close modal when clicking outside the image
        >
            <div
                style={{
                    backgroundColor: 'white',
                    padding: '10px', // Reduced padding
                    borderRadius: '8px',
                    width: '99%', // Increased width
                    height: '99%', // Increased height
                    maxWidth: '2000px', // Increased maximum width
                    maxHeight: '99vh', // Increased maximum height
                    display: 'flex',
                    flexDirection: 'column',
                    position: 'relative'
                }}
                onClick={(e) => e.stopPropagation()} // Prevent clicks inside the modal from closing it
            >
                {/* Image container */}
                <div style={{
                    flex: 1,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    overflow: 'hidden',
                    margin: '0',
                    position: 'relative'
                }}>
                    <img
                        src={largeImageUrl}
                        alt="Large species"
                        style={{
                            maxWidth: '99%',
                            maxHeight: 'calc(99vh - 100px)', // Adjusted to leave space for attribution
                            objectFit: 'contain',
                            borderRadius: '4px'
                        }}
                        onClick={onClose} // Close modal when clicking on the image
                    />
                </div>

                {/* Attribution overlay at the bottom */}
                <div style={{
                    position: 'absolute',
                    bottom: '10px', // Adjusted to ensure visibility
                    left: '10px', // Adjusted to ensure visibility
                    right: '10px', // Adjusted to ensure visibility
                    background: 'rgba(255, 255, 255, 0.9)', // Semi-transparent white background
                    padding: '8px',
                    fontSize: '12px',
                    color: '#666',
                    textAlign: 'center',
                    borderRadius: '4px',
                    zIndex: 1001 // Ensure attribution is above the image
                }}>
                    {isUrl(currentCard.attribution) ? (
                        <a href={currentCard.attribution} target="_blank" rel="noopener noreferrer" style={{ color: '#666', textDecoration: 'underline' }}>
                            {currentCard.attribution}
                        </a>
                    ) : (
                        currentCard.attribution
                    )}
                </div>

                {/* Close button */}
                <button
                    onClick={onClose}
                    style={{
                        position: 'absolute',
                        top: '10px',
                        right: '10px',
                        padding: '6px 12px',
                        backgroundColor: 'rgba(0, 123, 255, 0.8)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: 'bold',
                        transition: 'all 0.2s',
                        zIndex: 1002 // Ensure close button is above everything
                    }}
                    onMouseOver={(e) => {
                        e.target.style.backgroundColor = 'rgba(0, 86, 179, 0.9)';
                        e.target.style.transform = 'scale(1.05)';
                    }}
                    onMouseOut={(e) => {
                        e.target.style.backgroundColor = 'rgba(0, 123, 255, 0.8)';
                        e.target.style.transform = 'scale(1)';
                    }}
                >
                    Close
                </button>
            </div>
        </div>
    );
};

export default LargeImageModal;