import React, {useEffect, useCallback, useState} from 'react';
import axios from 'axios';
import {useFlashcardDeck} from './hooks/useFlashcardDeck';
import {useFlashcardGame} from './hooks/useFlashcardGame';
import {useHints} from './hooks/useHints';
import {FlashcardDisplay} from './components/FlashcardDisplay';
import FileManagementModal from './components/FileManagementModal';
import PronunciationModal from './components/PronunciationModal';
import LargeImageModal from './components/LargeImageModal';
import HelpModal from './components/HelpModal'; // Import the new HelpModal component
import static_cards from './data/uploads/Spring2024Maine';

const App = () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const [isFileModalOpen, setIsFileModalOpen] = useState(false);
    const [isLargeImageModalOpen, setIsLargeImageModalOpen] = useState(false);
    const [pronunciationModalOpen, setPronunciationModalOpen] = useState(false);
    const [pronunciationText, setPronunciationText] = useState('');
    const [isServerWakingUp, setIsServerWakingUp] = useState(false);
    const [importedFileName, setImportedFileName] = useState('');
    const [isHelpModalOpen, setIsHelpModalOpen] = useState(false); // Add this state for help modal

    const {
        currentCard,
        currentFileName,
        loadCardsFromFile,
        nextCard,
        restartDeck,
        setCards,
        shuffleCards
    } = useFlashcardDeck(apiUrl);

    const {
        answer,
        setAnswer,
        feedback,
        pronounceEnabled,
        checkAnswer,
        resetGameState
    } = useFlashcardGame(currentCard);

    const {
        hints,
        hintsVisible,
        setHintsVisible,
        updateHints,
        toggleHints
    } = useHints();

    // Retry mechanism for waking up the server
    const wakeUpServer = useCallback(async () => {
        let retries = 5; // Number of retries
        let delay = 3000; // Delay between retries in milliseconds

        setIsServerWakingUp(true); // Show "Server is starting up" message

        while (retries > 0) {
            try {
                const wakeupResponse = await axios.get(`${apiUrl}/wakeup`);
                if (wakeupResponse.status === 200) {
                    console.log('Server is awake!');
                    setIsServerWakingUp(false); // Hide "Server is starting up" message
                    return;
                }
            } catch (error) {
                console.log('Error waking up server:', error);
            }

            retries--;
            if (retries > 0) {
                console.log(`Retrying in ${delay / 1000} seconds...`);
                await new Promise((resolve) => setTimeout(resolve, delay));
            }
        }

        // If all retries fail, show an error message
        console.error('Failed to wake up server after multiple retries.');
        setIsServerWakingUp(false); // Optionally, you can keep this true to show an error message
    }, [apiUrl]);

    useEffect(() => {
        wakeUpServer();
    }, [wakeUpServer]);

    useEffect(() => {
        const shuffledCards = shuffleCards([...static_cards]);
        setCards(shuffledCards);
        updateHints(shuffledCards);
    }, [shuffleCards, setCards, updateHints]);

    const handleKeyDown = useCallback((e) => {
        if (e.key === 'Enter') {
            checkAnswer();
        }
    }, [checkAnswer]);

    const handleFileSelect = useCallback(async (filename, directory) => {
        const newCards = await loadCardsFromFile(filename, directory);
        setImportedFileName('');
        updateHints(newCards);
        resetGameState();
        setHintsVisible(false); // Hide hints when a new file is selected
        setIsFileModalOpen(false);
    }, [loadCardsFromFile, updateHints, resetGameState, setHintsVisible]);

    const handleDirectImport = useCallback((records,filename) => {
        // Remove .csv extension if present
        const cleanFileName = filename.replace('.csv', '');
        setImportedFileName(cleanFileName);
        loadCardsFromFile('', ''); // This should clear currentFileName

        const shuffledCards = shuffleCards([...records]);
        setCards(shuffledCards);
        updateHints(shuffledCards);
        resetGameState();
        setHintsVisible(false);
        setIsFileModalOpen(false);
    }, [shuffleCards, setCards, updateHints, resetGameState, setHintsVisible, loadCardsFromFile]);

    const openPronunciationModal = useCallback(async () => {
        if (!currentCard) {
            alert('No card available.');
            return;
        }

        setIsServerWakingUp(true);
        setPronunciationModalOpen(true);

        try {
            // First try to wake up the server
            await axios.get(`${apiUrl}/wakeup`);

            try {
                // If server is awake, try to get pronunciation
                const response = await axios.post(`${apiUrl}/pronounce_name`, {
                    scientific_name: currentCard.scientific_name
                });

                setPronunciationText(response.data.pronunciation);
                setIsServerWakingUp(false);
            } catch (pronunciationErr) {
                // Check if it's a CORS error (indicates server is still starting)
                if (pronunciationErr.message.includes('CORS') || pronunciationErr.message.includes('Network Error')) {
                    setPronunciationText('Server is slowly waking up. Please try again in a minute.');
                } else {
                    setPronunciationText('Unable to fetch pronunciation. Please try again.');
                }
            }
        } catch (wakeupErr) {
            // If wakeup endpoint fails, server is likely completely down
            setPronunciationText('Server is currently offline. Please try again in a few minutes.');
        }
    }, [apiUrl, currentCard]);

    const selectHint = useCallback((hint) => {
        setAnswer(hint);
        checkAnswer(hint);
    }, [setAnswer, checkAnswer]);

    if (!currentCard) {
        return <p>No cards available. Please load a file.</p>;
    }

    return (
        <div className="app-container">
            {/* Updated file-management div with new styling */}
            <div style={{
                position: 'fixed',
                top: '20px',
                right: '20px',
                textAlign: 'right',
                zIndex: 1000
            }}>
                <button onClick={() => setIsFileModalOpen(true)}>
                    Manage Flashcard Decks
                </button>
                <div style={{marginTop: '10px'}}>
                    <span><span>{importedFileName || currentFileName}</span></span>
                </div>
            </div>

            {/* Help icon in bottom right */}
            <div style={{
                position: 'fixed',
                bottom: '20px',
                right: '20px',
                zIndex: 1000,
                cursor: 'pointer',
                backgroundColor: '#4682B4',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: 'white',
                fontWeight: 'bold',
                boxShadow: '0px 2px 5px rgba(0,0,0,0.2)'
            }} onClick={() => setIsHelpModalOpen(true)}>
                ?
            </div>

            <FileManagementModal
                isOpen={isFileModalOpen}
                onClose={() => setIsFileModalOpen(false)}
                onFileSelect={handleFileSelect}
                onDirectImport={handleDirectImport}
            />

            <PronunciationModal
                pronunciationModalOpen={pronunciationModalOpen}
                pronunciationText={pronunciationText}
                setPronunciationModalOpen={setPronunciationModalOpen}
                isServerWakingUp={isServerWakingUp}
            />

            <LargeImageModal
                isOpen={isLargeImageModalOpen}
                onClose={() => setIsLargeImageModalOpen(false)}
                currentCard={currentCard}
            />

            <HelpModal
                isOpen={isHelpModalOpen}
                onClose={() => setIsHelpModalOpen(false)}
            />

            <FlashcardDisplay
                currentCard={currentCard}
                answer={answer}
                setAnswer={setAnswer}
                handleKeyDown={handleKeyDown}
                checkAnswer={checkAnswer}
                toggleHints={toggleHints}
                hintsVisible={hintsVisible}
                feedback={feedback}
                pronounceEnabled={pronounceEnabled}
                openPronunciationModal={openPronunciationModal}
                nextCard={() => {
                    nextCard();
                    resetGameState();
                    setHintsVisible(false);
                }}
                restartDeck={() => {
                    restartDeck(); // Restart the deck
                    resetGameState(); // Reset game state (including hints visibility)
                    setHintsVisible(false);
                }}
                openLargeImageModal={() => setIsLargeImageModalOpen(true)}
                hints={hints}
                selectHint={selectHint}
            />
        </div>
    );
};

export default App;