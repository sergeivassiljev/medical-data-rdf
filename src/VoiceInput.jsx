import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faMicrophone,
  faStop,
  faPaperPlane,
} from "@fortawesome/free-solid-svg-icons";

function VoiceInput() {
  const [text, setText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const recognition = new window.webkitSpeechRecognition();
  recognition.lang = "en-US";

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    setText(transcript);
    setCorrectedText("");
    recognition.stop();
    setIsListening(false);
  };

  recognition.onerror = function (event) {
    console.error("Speech recognition error: ", event.error);
    setIsListening(false);
    setIsLoading(false);
  };

  const handleStart = () => {
    setIsListening(true);
    recognition.start();
  };

  const handleStop = () => {
    setIsListening(false);
    recognition.stop();
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    const response = await fetch("http://localhost:5000/process-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (response.ok) {
      const data = await response.json();
      setCorrectedText(data.correctedText);
    } else {
      console.error("Error sending text to server");
    }
    setIsLoading(false);
  };

  return (
    <div>
      <button
        className="btn btn-primary btn-sm mr-2"
        onClick={handleStart}
        disabled={isListening}
      >
        <FontAwesomeIcon icon={faMicrophone} />
      </button>
      <button
        className="btn btn-secondary btn-sm mr-2"
        onClick={handleStop}
        disabled={!isListening}
      >
        <FontAwesomeIcon icon={faStop} />
      </button>
      <button
        className="btn btn-success btn-sm"
        onClick={handleSubmit}
        disabled={!text || isLoading}
      >
        <FontAwesomeIcon icon={faPaperPlane} />
      </button>
      <div className="text-display">
        {isLoading && <p className="loading-text">Loading...</p>}
        <p>Audio to text: {text}</p>
        {correctedText && <p>Fixed text: {correctedText}</p>}
      </div>
    </div>
  );
}

export default VoiceInput;
