import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize conversation on component mount
  useEffect(() => {
    initializeConversation();
  }, []);

  const initializeConversation = async () => {
    try {
      setError(null);
      const response = await axios.post(`${API_BASE_URL}/api/chat/conversations`, {
        title: new Date().toLocaleString()
      });
      setConversationId(response.data.id);
      setMessages([]);
    } catch (err) {
      setError('Failed to initialize conversation. Please ensure the backend is running.');
      console.error('Error initializing conversation:', err);
    }
  };

  const handleSendMessage = async (content) => {
    if (!conversationId) {
      setError('No active conversation. Please refresh the page.');
      return;
    }

    // Add user message to UI immediately
    const userMessage = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat/send`, {
        conversation_id: conversationId,
        content: content
      });

      setMessages(response.data.messages);
    } catch (err) {
      setError(`Failed to send message: ${err.response?.data?.detail || err.message}`);
      // Remove the user message if there was an error
      setMessages(prev => prev.slice(0, -1));
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    initializeConversation();
  };

  return (
    <div className="app">
      <div className="app-header">
        <h1>LLM Chatbot</h1>
        <button className="new-chat-btn" onClick={handleNewConversation}>
          New Chat
        </button>
      </div>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
          <button onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      {conversationId ? (
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSendMessage={handleSendMessage}
        />
      ) : (
        <div className="loading">
          <p>Initializing conversation...</p>
        </div>
      )}
    </div>
  );
}

export default App;
