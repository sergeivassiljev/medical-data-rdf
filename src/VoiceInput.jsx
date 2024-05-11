import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone, faStop, faPaperPlane } from '@fortawesome/free-solid-svg-icons';

function VoiceInput() {
  const [text, setText] = useState('');
  const [correctedText, setCorrectedText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognition = new window.webkitSpeechRecognition();
  recognition.lang = 'en-US';

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    setText(transcript);
    recognition.stop();
    setIsListening(false);
  };

  recognition.onerror = function(event) {
    console.error('Speech recognition error: ', event.error);
    setIsListening(false);
  };

  const handleStart = () => {
    setIsListening(true);
    recognition.start();
  };

  const handleStop = () => {
    setIsListening(false);
    recognition.stop();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/process-text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text })
    });

    if (response.ok) {
      const data = await response.json();
      setCorrectedText(data.correctedText);
    } else {
      console.error('Error sending text to server');
    }
  };

  return (
    <div>
      <button className="btn btn-primary btn-sm mr-2" onClick={handleStart} disabled={isListening}>
        <FontAwesomeIcon icon={faMicrophone} />
      </button>
      <button className="btn btn-secondary btn-sm mr-2" onClick={handleStop} disabled={!isListening}>
        <FontAwesomeIcon icon={faStop} />
      </button>
      <button className="btn btn-success btn-sm" onClick={handleSubmit} disabled={!text}>
        <FontAwesomeIcon icon={faPaperPlane} />
      </button>
      <p>Entered text: {text}</p>
      <p>Corrected text: {correctedText}</p>
    </div>
  );
}

export default VoiceInput;