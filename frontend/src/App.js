import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Schedule from './components/Schedule';
import TeamProgress from './components/TeamProgress';
import About from './components/About';
import './App.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex min-h-screen bg-gray-50">
          <Sidebar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/schedule" element={<Schedule />} />
            <Route path="/team" element={<TeamProgress />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
