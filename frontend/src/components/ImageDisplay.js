import React from 'react';

const ImageDisplay = ({ imageUrl }) => {
    return (
        <div>
            {imageUrl ? (
                <img src={`http://127.0.0.1:5000${imageUrl}`} alt="Generated" />
            ) : (
                <p>No image generated yet.</p>
            )}
        </div>
    );
};

export default ImageDisplay;
