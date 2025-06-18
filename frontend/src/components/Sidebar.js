import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Dashboard, 
  Schedule, 
  People, 
  Info, 
  Chat,
  Close 
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const SidebarIcon = ({ icon, text, active, onClick }) => {
  return (
    <div className="relative group" onClick={onClick}>
      <motion.div
        whileHover={{ scale: 1.1 }}
        className={`sidebar-icon ${active ? 'bg-green-600 text-white' : ''}`}
      >
        {icon}
      </motion.div>
      <span className="sidebar-tooltip group-hover:scale-100">
        {text}
      </span>
    </div>
  );
};

const ChatPanel = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      // TODO: Integrate with actual LLM
      setMessages(prev => [...prev, { 
        text: "I'm here to help automate your PM tasks!", 
        sender: 'bot' 
      }]);
      setInput('');
    }
  };

  return (
    <motion.div
      initial={{ x: '100%' }}
      animate={{ x: isOpen ? 0 : '100%' }}
      transition={{ type: 'spring', damping: 20 }}
      className="fixed right-0 top-0 h-full w-80 bg-white shadow-xl z-50"
    >
      <div className="flex flex-col h-full">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">AI Assistant</h2>
          <Close className="cursor-pointer" onClick={onClose} />
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg ${
                msg.sender === 'user' 
                  ? 'bg-blue-500 text-white ml-auto' 
                  : 'bg-gray-100 text-gray-800'
              } max-w-[80%]`}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="p-4 border-t">
          <div className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Type your message..."
            />
            <button
              onClick={handleSend}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isChatOpen, setIsChatOpen] = useState(false);

  const routes = [
    { path: '/', icon: <Dashboard />, text: 'Dashboard' },
    { path: '/schedule', icon: <Schedule />, text: 'Schedule' },
    { path: '/team', icon: <People />, text: 'Team Progress' },
    { path: '/about', icon: <Info />, text: 'About' },
  ];

  return (
    <>
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: 'auto' }}
        className="fixed left-0 top-0 h-screen w-16 m-0 flex flex-col
                   bg-gray-900 text-white shadow-lg"
      >
        <div className="flex flex-col items-center mt-4 mb-auto">
          {routes.map((route) => (
            <SidebarIcon
              key={route.path}
              icon={route.icon}
              text={route.text}
              active={location.pathname === route.path}
              onClick={() => navigate(route.path)}
            />
          ))}
        </div>
        
        <div className="mb-4">
          <SidebarIcon
            icon={<Chat />}
            text="AI Assistant"
            onClick={() => setIsChatOpen(true)}
          />
        </div>
      </motion.div>

      <ChatPanel 
        isOpen={isChatOpen} 
        onClose={() => setIsChatOpen(false)} 
      />
    </>
  );
};

export default Sidebar; 