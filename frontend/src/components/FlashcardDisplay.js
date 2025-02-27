// src/components/FlashcardDisplay.js
import React from 'react';
import { FlashcardContainer, ImageContainer, ButtonContainer } from '../styles/FlashcardStyles';

export const FlashcardDisplay = ({
    currentCard,
    answer,
    setAnswer,
    handleKeyDown,
    checkAnswer,
    toggleHints,
    hintsVisible,
    feedback,
    pronounceEnabled,
    openPronunciationModal,
    nextCard,
    restartDeck,
    openLargeImageModal,
    hints,
    selectHint
}) => (
    <FlashcardContainer>
        <h1>Species Flashcard</h1>

        <ImageContainer onClick={openLargeImageModal}>
            <img
                src={currentCard.image_url}
                alt={currentCard.scientific_name}
            />
        </ImageContainer>

        <div className="input-section">
            <input
                type="text"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Enter scientific name"
            />
            <ButtonContainer>
                <button onClick={checkAnswer}>Check Answer</button>
                <button onClick={toggleHints}>
                    {hintsVisible ? 'Hide Hints' : 'Show Hints'}
                </button>
            </ButtonContainer>
        </div>

        {feedback && (
            <div
                className={`feedback ${feedback.includes('Incorrect') ? 'error' : 'success'}`}
                dangerouslySetInnerHTML={{__html: feedback}}
            />
        )}

        {pronounceEnabled && (
            <button onClick={openPronunciationModal}>
                Pronounce Name
            </button>
        )}

        <ButtonContainer>
            <button onClick={nextCard}>Next Card</button>
            <button onClick={restartDeck}>Restart Deck</button>
        </ButtonContainer>

        {hintsVisible && (
            <div className="hints-container">
                <h3>Hints</h3>
                <div className="hints-grid">
                    {hints.map((hint) => (
                        <button
                            key={hint}
                            onClick={() => selectHint(hint)}
                        >
                            {hint}
                        </button>
                    ))}
                </div>
            </div>
        )}
    </FlashcardContainer>
);
