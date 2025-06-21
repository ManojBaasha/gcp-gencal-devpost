import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Close, 
  Send, 
  ChatBubble,
  ExpandLess,
  ExpandMore,
  Settings,
  Delete
} from '@mui/icons-material';

const Message = ({ message, onDelete }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className={`p-3 rounded-lg ${
      message.sender === 'user' 
        ? 'bg-blue-500 text-white ml-auto' 
        : 'bg-gray-100 text-gray-800'
    } max-w-[80%] relative group`}
  >
    <p className="pr-6">{message.text}</p>
    {onDelete && (
      <motion.button
        initial={{ opacity: 0 }}
        whileHover={{ opacity: 1 }}
        className="absolute top-1 right-1 p-1 text-xs opacity-0 group-hover:opacity-100"
        onClick={() => onDelete(message.id)}
      >
        <Delete fontSize="small" className={message.sender === 'user' ? 'text-white' : 'text-gray-500'} />
      </motion.button>
    )}
  </motion.div>
);

async function callOrchestrator(message) {
    try {
        const response = await fetch('https://gcp-gencal-devpost.onrender.com/orchestrate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, context: {} }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Orchestrator response:", data.responses);
        return data.responses;
    } catch (error) {
        console.error("Failed to call orchestrator:", error);
        return null;
    }
}

const ChatPanel = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim()) {
      const newMessage = {
        id: Date.now(),
        text: input,
        sender: 'user',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newMessage]);
      setInput('');
      setLoading(true);
      try {
        const botText = await callOrchestrator(newMessage.text);
        const aiResponse = {
          id: Date.now() + 1,
          text: botText || 'Sorry, I could not get a response.',
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiResponse]);
      } catch (err) {
        setMessages(prev => [...prev, {
          id: Date.now() + 2,
          text: 'Error: Could not reach the assistant API.',
          sender: 'bot',
          timestamp: new Date()
        }]);
      }
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleDeleteMessage = (messageId) => {
    setMessages(prev => prev.filter(msg => msg.id !== messageId));
  };

  const handleClearChat = () => {
    setMessages([]);
    setIsSettingsOpen(false);
  };

  return (
    <div className="w-80 bg-white shadow-lg border-l flex flex-col h-screen">
      {/* Header */}
      <div className="flex justify-between items-center p-3 border-b bg-gray-50">
        <div className="flex items-center">
          <ChatBubble className="text-blue-500 mr-2" />
          <h2 className="text-lg font-semibold">AI Assistant</h2>
        </div>
        <div className="flex items-center space-x-1">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsSettingsOpen(!isSettingsOpen)}
            className="p-1 hover:bg-gray-200 rounded-full"
          >
            <Settings fontSize="small" />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsMinimized(!isMinimized)}
            className="p-1 hover:bg-gray-200 rounded-full"
          >
            {isMinimized ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
          </motion.button>
        </div>
      </div>

      {/* Settings Dropdown */}
      <AnimatePresence>
        {isSettingsOpen && !isMinimized && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-b"
          >
            <div className="p-4 bg-gray-50">
              <button
                onClick={handleClearChat}
                className="flex items-center space-x-2 text-red-500 hover:text-red-600"
              >
                <Delete fontSize="small" />
                <span>Clear Chat History</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Messages */}
      {!isMinimized && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <Message 
              key={msg.id} 
              message={msg} 
              onDelete={handleDeleteMessage}
            />
          ))}
          {loading && (
            <div className="text-xs text-gray-400 italic">AI Assistant is typing...</div>
          )}
        </div>
      )}

      {/* Input Area */}
      {!isMinimized && (
        <div className="p-4 border-t">
          <div className="flex space-x-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={1}
              style={{ minHeight: '40px', maxHeight: '120px' }}
              disabled={loading}
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSend}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center"
              disabled={loading}
            >
              <Send />
            </motion.button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatPanel; 