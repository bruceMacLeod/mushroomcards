import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileManagementModal from './file-management-modal';
import PronunciationModal from './PronunciationModal'; // Import the new component

console.log('PronunciationModal:', PronunciationModal);
const App = () => {
    const [card, setCard] = useState(null);
    const [answer, setAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [hintsVisible, setHintsVisible] = useState(false);
    const [hints, setHints] = useState([]);
    const [attempts, setAttempts] = useState(0);
    const [pronounceEnabled, setPronounceEnabled] = useState(false);
    const [isFileModalOpen, setIsFileModalOpen] = useState(false);
    const [pronunciationModalOpen, setPronunciationModalOpen] = useState(false);
    const [pronunciationText, setPronunciationText] = useState('');

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        fetch(`${apiUrl}/get_card`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Data fetched:', data);
                fetchCard();
                fetchHints();
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }, []);

    const fetchCard = async () => {
        try {
            const response = await axios.get(`${apiUrl}/get_card`);
            if (response.data.completed) {
                setFeedback(response.data.message);
            } else {
                setCard(response.data);
                resetState();
            }
        } catch (err) {
            console.error(err);
        }
    };

    const fetchHints = async () => {
        try {
            const response = await axios.get(`${apiUrl}/get_hints`);
            const sortedHints = response.data.sort();
            setHints(sortedHints);
            console.log('Hints fetched:', sortedHints);
        } catch (err) {
            console.error('Error fetching hints:', err);
            setHints([]);
        }
    };

    const resetState = () => {
        setFeedback('');
        setAnswer('');
        setAttempts(0);
        setPronounceEnabled(false);
        setHintsVisible(false);
    };

    const checkAnswer = async () => {
        if (!card) return;

        try {
            const response = await axios.post(`${apiUrl}/check_answer`, { answer, card });
            setFeedback(response.data.message);
            if (response.data.correct) {
                setPronounceEnabled(true);
            } else {
                setAttempts((prev) => prev + 1);
                if (attempts + 1 >= 3) {
                    setFeedback(`Incorrect. The correct name is: ${card.scientific_name}`);
                    setPronounceEnabled(true);
                }
            }
        } catch (err) {
            console.error(err);
            setFeedback("Error while checking the answer.");
        }
    };

    const pronounceName = async () => {
        if (!card) return;

        try {
            const response = await axios.post(`${apiUrl}/pronounce_name`, { scientific_name: card.scientific_name });
            alert(response.data.pronunciation);
        } catch (err) {
            console.error(err);
        }
    };

    const toggleHints = () => {
        setHintsVisible(!hintsVisible);
    };

    const nextCard = async () => {
        try {
            await axios.post(`${apiUrl}/next_card`);
            fetchCard();
        } catch (err) {
            console.error(err);
        }
    };

    const selectHint = (hint) => {
        setAnswer(hint);
    };

    const handleFileSelect = async (filename, directory = 'MMAforays') => {
        try {
            console.log('Sending filename:', filename);
            console.log('Sending directory:', directory);

            const response = await axios.post(`${apiUrl}/select_csv`, {
                filename,
                directory
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.data.first_card) {
                setCard(response.data.first_card);
                resetState();

                try {
                    const hintsResponse = await axios.get(`${apiUrl}/get_hints`);
                    const sortedHints = hintsResponse.data.sort();
                    setHints(sortedHints);
                    console.log('Hints updated:', sortedHints);
                } catch (hintsError) {
                    console.error('Error fetching hints:', hintsError);
                }
            }
        } catch (error) {
            console.error('File selection error:', error);
            if (error.response) {
                console.error('Server error details:', error.response.data);
                console.error('Server error status:', error.response.status);
            }
        }
    };

    const handleFinish = async () => {
        try {
            await axios.post(`${apiUrl}/exit_application`);
        } catch (error) {
            console.error('Finish error:', error);
        }
    };

    const openPronunciationModal = async () => {
        if (!card) return;

        try {
            const response = await axios.post(`${apiUrl}/pronounce_name`, { scientific_name: card.scientific_name });
            setPronunciationText(response.data.pronunciation);
            setPronunciationModalOpen(true);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div style={{
            padding: '20px',
            fontFamily: 'Arial',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            maxWidth: '600px',
            margin: '0 auto'
        }}>
            <button
                onClick={() => setIsFileModalOpen(true)}
                style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px'
                }}
            >
                Manage Files
            </button>

            <PronunciationModal
                pronunciationModalOpen={pronunciationModalOpen}
                pronunciationText={pronunciationText}
                setPronunciationModalOpen={setPronunciationModalOpen}
            />


            <FileManagementModal
                isOpen={isFileModalOpen}
                onClose={() => setIsFileModalOpen(false)}
                onFileSelect={handleFileSelect}
            />

            {card && (
                <div style={{ textAlign: 'center', width: '100%' }}>
                    <h1>Species Flashcard</h1>

                    <img
                        src={`${apiUrl}/get_image?url=${encodeURIComponent(card.image_url)}`}
                        alt={card.image_url}
                        style={{
                            maxWidth: '300px',
                            maxHeight: '300px',
                            marginBottom: '20px'
                        }}
                    />

                    <div style={{ marginBottom: '20px' }}>
                        <input
                            type="text"
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            placeholder="Enter scientific name"
                            style={{
                                width: '100%',
                                padding: '10px',
                                marginBottom: '10px'
                            }}
                        />
                        <button
                            onClick={checkAnswer}
                            style={{
                                padding: '10px 20px',
                                marginRight: '10px'
                            }}
                        >
                            Check Answer
                        </button>
                        <button
                            onClick={toggleHints}
                            style={{ padding: '10px 20px' }}
                        >
                            {hintsVisible ? 'Hide Hints' : 'Show Hints'}
                        </button>
                    </div>

                    {feedback && (
                        <div
                            style={{
                                color: feedback.includes('Incorrect') ? 'red' : 'green',
                                marginBottom: '20px'
                            }}
                        >
                            {feedback}
                        </div>
                    )}

                    {pronounceEnabled && (
                        <button
                            onClick={openPronunciationModal}
                            style={{ padding: '10px 20px' }}
                        >
                            Pronounce Name
                        </button>
                    )}

                    <button
                        onClick={nextCard}
                        style={{
                            marginTop: '20px',
                            padding: '10px 20px'
                        }}
                    >
                        Next Card
                    </button>

                    {hintsVisible && (
                        <div style={{
                            backgroundColor: '#f0f0f0',
                            padding: '10px',
                            marginTop: '20px'
                        }}>
                            <h3>Hints</h3>
                            {hints.map((hint) => (
                                <button
                                    key={hint}
                                    onClick={() => selectHint(hint)}
                                    style={{
                                        margin: '5px',
                                        padding: '5px 10px'
                                    }}
                                >
                                    {hint}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default App;