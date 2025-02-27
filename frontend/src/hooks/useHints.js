// src/hooks/useHints.js
import { useState, useCallback } from 'react';

export const useHints = () => {
    const [hints, setHints] = useState([]);
    const [hintsVisible, setHintsVisible] = useState(false);

    const updateHints = useCallback((cardArray) => {
        const uniqueNames = [...new Set(cardArray.map(card => card.scientific_name))];
        setHints(uniqueNames.sort());
    }, []);

    const toggleHints = useCallback(() => {
        setHintsVisible(prev => !prev);
    }, []);

    return {
        hints,
        hintsVisible,
        setHintsVisible,
        updateHints,
        toggleHints
    };
};
// export default useHints;