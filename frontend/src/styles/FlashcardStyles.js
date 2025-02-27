// src/styles/FlashcardStyles.js
import styled from 'styled-components';

export const FlashcardContainer = styled.div`
    text-align: center;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;

    .input-section {
        margin-bottom: 20px;
        
        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
        }
    }

    .feedback {
        margin-bottom: 20px;
        
        &.error { color: red; }
        &.success { color: green; }
    }

    .hints-container {
        background-color: #f0f0f0;
        padding: 10px;
        margin-top: 20px;
        
        .hints-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            padding: 10px;
        }
    }
`;

export const ImageContainer = styled.div`
    cursor: pointer;
    margin-bottom: 20px;
    
    img {
        max-width: 300px;
        max-height: 300px;
        object-fit: contain;
    }
`;

export const ButtonContainer = styled.div`
    display: flex;
    gap: 10px;
    justify-content: center;
    margin: 10px 0;
    
    button {
        padding: 10px 20px;
    }
`;
