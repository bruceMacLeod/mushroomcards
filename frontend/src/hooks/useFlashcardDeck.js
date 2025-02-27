// src/hooks/useFlashcardDeck.js
import { useState, useCallback } from 'react';
import axios from 'axios';
import useFlashcardGame  from './useFlashcardGame';

export const useFlashcardDeck = (apiUrl) => {
    const [cards, setCards] = useState([]);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const [currentFileName, setCurrentFileName] = useState('intro-obs-taxa');
    const {resetGameState} = useFlashcardGame();

    const shuffleCards = useCallback((array) => {
        const newArray = [...array];
        let currentIndex = newArray.length;
        while (currentIndex !== 0) {
            const randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;
            [newArray[currentIndex], newArray[randomIndex]] =
                [newArray[randomIndex], newArray[currentIndex]];
        }
        return newArray;
    }, []);

    const loadCardsFromFile = useCallback(async (filename, directory = 'mmaforays') => {
        try {
            if (!filename) return;

            const response = await axios.post(`${apiUrl}/load_cards`, {
                filename,
                directory
            });
            const shuffledCards = shuffleCards([...response.data]);
            setCards(shuffledCards);
            setCurrentCardIndex(0);
            setCurrentFileName(filename.replace('.csv', ''));
            return shuffledCards;
        } catch (error) {
            console.error('Error loading cards:', error);
            return [];
        }
    }, [apiUrl, shuffleCards]);

    const nextCard = useCallback(() => {
        if (cards.length === 0) return;
        setCurrentCardIndex(prev => (prev + 1) % cards.length);
    }, [cards.length]);

    const restartDeck = useCallback(() => {
        if (cards.length === 0) return;
        const shuffledCards = shuffleCards([...cards]);
        setCards(shuffledCards);
        setCurrentCardIndex(0);
        resetGameState(); // Reset game state (including hints visibility)
    }, [cards, shuffleCards, resetGameState]);


    return {
        cards,
        currentCard: cards[currentCardIndex],
        currentFileName,
        loadCardsFromFile,
        nextCard,
        restartDeck,
        setCards,
        shuffleCards
    };
};
// export default useFlashcardDeck;
