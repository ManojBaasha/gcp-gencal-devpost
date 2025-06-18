import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { format, addDays, startOfWeek } from 'date-fns';
import {
  Add,
  ChevronLeft,
  ChevronRight,
  AccessTime,
  People,
  Room
} from '@mui/icons-material';

const TimeSlot = ({ time, event, onClick }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className={`p-3 rounded-lg mb-2 ${
      event 
        ? 'bg-blue-100 border-l-4 border-blue-500' 
        : 'bg-gray-50 cursor-pointer hover:bg-gray-100'
    }`}
    onClick={onClick}
  >
    <div className="flex items-center justify-between">
      <span className="text-gray-600">{time}</span>
      {event && (
        <div className="flex-1 ml-4">
          <h4 className="font-semibold text-blue-800">{event.title}</h4>
          <div className="flex items-center text-sm text-gray-600 mt-1">
            <AccessTime className="w-4 h-4 mr-1" />
            <span>{event.duration}</span>
            <People className="w-4 h-4 ml-3 mr-1" />
            <span>{event.attendees}</span>
            <Room className="w-4 h-4 ml-3 mr-1" />
            <span>{event.location}</span>
          </div>
        </div>
      )}
    </div>
  </motion.div>
);

const Schedule = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [showNewEventModal, setShowNewEventModal] = useState(false);

  // Sample data - replace with real data
  const events = {
    'Monday': {
      '09:00 AM': {
        title: 'Daily Standup',
        duration: '30min',
        attendees: 'Team',
        location: 'Meeting Room 1'
      },
      '02:00 PM': {
        title: 'Sprint Planning',
        duration: '2h',
        attendees: 'Dev Team',
        location: 'Virtual'
      }
    },
    'Wednesday': {
      '10:00 AM': {
        title: 'Product Review',
        duration: '1h',
        attendees: 'Stakeholders',
        location: 'Conference Room'
      }
    },
    'Friday': {
      '04:00 PM': {
        title: 'Sprint Retro',
        duration: '1h',
        attendees: 'Team',
        location: 'Virtual'
      }
    }
  };

  const weekDays = [...Array(7)].map((_, i) => {
    const date = addDays(startOfWeek(currentDate), i);
    return format(date, 'EEEE');
  });

  const timeSlots = [
    '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
    '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM',
    '05:00 PM'
  ];

  return (
    <div className="p-6 ml-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Team Schedule</h1>
          <div className="flex items-center space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-full bg-gray-200 hover:bg-gray-300"
              onClick={() => setCurrentDate(addDays(currentDate, -7))}
            >
              <ChevronLeft />
            </motion.button>
            <span className="text-lg font-semibold">
              {format(currentDate, 'MMMM d, yyyy')}
            </span>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-full bg-gray-200 hover:bg-gray-300"
              onClick={() => setCurrentDate(addDays(currentDate, 7))}
            >
              <ChevronRight />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              onClick={() => setShowNewEventModal(true)}
            >
              <Add className="mr-1" />
              New Meeting
            </motion.button>
          </div>
        </div>

        <div className="grid grid-cols-7 gap-4">
          {weekDays.map((day) => (
            <div key={day} className="card">
              <h3 className="text-lg font-semibold mb-4 text-gray-700">{day}</h3>
              {timeSlots.map((time) => (
                <TimeSlot
                  key={`${day}-${time}`}
                  time={time}
                  event={events[day]?.[time]}
                  onClick={() => !events[day]?.[time] && setShowNewEventModal(true)}
                />
              ))}
            </div>
          ))}
        </div>

        {/* Modal placeholder - implement full modal component */}
        {showNewEventModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="bg-white p-6 rounded-lg w-96"
            >
              <h2 className="text-xl font-semibold mb-4">Schedule New Meeting</h2>
              {/* Add form fields here */}
              <button
                className="mt-4 px-4 py-2 bg-gray-200 rounded-lg"
                onClick={() => setShowNewEventModal(false)}
              >
                Close
              </button>
            </motion.div>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Schedule; 