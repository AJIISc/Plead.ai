import React from 'react';
import './Chatbot.css';

function Chatbot() {
  return (
    <div className="chatbot">
      <button className="chatbot-button"></button>
      <div className="chatbot-window">
        <p>Welcome to DigiLab! How can we assist you today?</p>
        {/* Chatbot interaction logic will go here */}
      </div>
    </div>
  );
}

export default Chatbot; 