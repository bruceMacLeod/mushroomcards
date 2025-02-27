// src/hooks/useFlashcardGame.js
import { useState, useCallback } from 'react';
// import useHints from './useHints';

export const useFlashcardGame = (currentCard) => {
    const [answer, setAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [attempts, setAttempts] = useState(0);
    const [pronounceEnabled, setPronounceEnabled] = useState(false);
//    const { toggleHints } = useHints(); // Call the hook and destructure

    function isString(value) {
      return typeof value === "string";
    }

    function formatScientificName(name) {
    // Trim leading and trailing spaces
        let trimmedName = name.trim().toLowerCase();

    // Replace multiple spaces between words with a single space
        trimmedName = trimmedName.replace(/\./g, '');
        return trimmedName.replace(/\s+/g, ' ');


    }
    const checkAnswer = useCallback((hint = null) => {
    if (!currentCard) {
        setFeedback('No card available.');
        return;
    }

    console.log('isString(hint)', isString(hint));
    const userAnswer = isString(hint) ? String(hint) : String(answer);
    // Debugging: Log the userAnswer and hint
    console.log('User Answer (raw):', userAnswer);
    console.log('Hint:', hint);
    console.log('answer', answer);

    console.log(formatScientificName(userAnswer), formatScientificName(currentCard.scientific_name));
    const isCorrect = formatScientificName(userAnswer) === formatScientificName(currentCard.scientific_name);
    console.log(isCorrect);
    const taxaUrl = currentCard.taxa_url;
    const hyperlinkedName = `<a href="${taxaUrl}" target="_blank" rel="noopener noreferrer">${currentCard.scientific_name}</a>`;
    const hyperlinkedCommonName = currentCard.common_name
        ? `<a href="${taxaUrl}" target="_blank" rel="noopener noreferrer">${currentCard.common_name}</a>`
        : '';

    if (isCorrect) {
        setFeedback(`Correct! ${hyperlinkedName} (${hyperlinkedCommonName})`);
        setPronounceEnabled(true);
    } else {
        const newAttempts = attempts + 1;
        setAttempts(newAttempts);
        if (newAttempts >= 3) {
            setFeedback(`Incorrect. The correct name is: ${hyperlinkedName} (${hyperlinkedCommonName})`);
            setPronounceEnabled(true);
        } else {
            setFeedback('Incorrect. Try again!');
        }
    }
}, [answer, attempts, currentCard]);


    const resetGameState = useCallback(() => {
        setFeedback('');
        setAnswer('');
        setAttempts(0);
        setPronounceEnabled(false);

    }, []);

    return {
        answer,
        setAnswer,
        feedback,
        attempts,
        pronounceEnabled,
        checkAnswer,
        resetGameState
    };
};
export default useFlashcardGame;