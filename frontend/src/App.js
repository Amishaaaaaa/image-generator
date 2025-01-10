import './styles/App.css';
import React, { useState } from 'react';
import WorkflowForm from './components/WorkflowForm';

const App = () => {
  const [imageUrl, setImageUrl] = useState(null);
  const [error, setError] = useState(null);  // Track error state

  const onGenerate = (params) => {
    const { seed, width, height, text } = params;

    // Make the fetch request to the backend
    fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ seed, width, height, text }), // Send the form data to the backend
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.image_url) {
          setImageUrl(`http://localhost:5000${data.image_url}`);  // Prepend the base URL to the image path
          setError(null);  // Clear any previous errors
        } else {
          console.error('Image generation failed');
          setError('Failed to generate image. Please try again.');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        setError('An error occurred while generating the image.');
      });
  };

  return (
    <div>
      <h1>IndieImages</h1>
      <WorkflowForm onGenerate={onGenerate} />
      
      {error && <p style={{ color: 'red' }}>{error}</p>}  {/* Display error message if present */}
      
      {imageUrl && (
        <div>
          <h3>Generated Image:</h3>
          <img src={imageUrl} alt="Generated" />
        </div>
      )}
    </div>
  );
};

export default App;
