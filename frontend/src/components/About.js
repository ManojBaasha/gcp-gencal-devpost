import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import {
  Flag,
  Star,
  Group,
  TrendingUp,
  CheckCircle,
  Engineering,
  BugReport,
  NewReleases
} from '@mui/icons-material';
import { doc, getDoc } from 'firebase/firestore';
import db from '../firebase-config';

const iconMap = {
  completed: <Flag className="text-green-500" />, // fallback
  'Project Kickoff': <Flag className="text-green-500" />,
  'Alpha Release': <Star className="text-green-500" />,
  'Beta Testing': <Engineering className="text-blue-500" />,
  'Version 1.0': <NewReleases className="text-gray-500" />
};

const FeatureCard = ({ icon, title, description }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="card"
  >
    <div className="flex items-start space-x-4">
      <div className="p-3 bg-blue-100 rounded-full">
        {icon}
      </div>
      <div>
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <p className="text-gray-600 mt-1">{description}</p>
      </div>
    </div>
  </motion.div>
);

const About = () => {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProject = async () => {
      setLoading(true);
      const projectDoc = await getDoc(doc(db, 'project', 'info'));
      if (projectDoc.exists()) {
        setProject(projectDoc.data());
      }
      setLoading(false);
    };
    fetchProject();
  }, []);

  if (loading || !project) {
    return (
      <div className="p-6 ml-16 flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Milestones: use timeline string and status from project.status
  const timeline = project.timeline || '';
  const status = project.status || {};
  // For demo, create milestones from timeline and status
  const milestones = [
    {
      date: timeline.split('(')[0]?.trim() || '',
      title: status.sprint ? `Current Sprint: ${status.sprint}` : 'Sprint',
      description: status.next_milestone || '',
      status: 'in-progress',
      icon: <Engineering className="text-blue-500" />
    },
    {
      date: '',
      title: 'Blockers',
      description: status.blockers || '',
      status: 'blocked',
      icon: <BugReport className="text-red-500" />
    }
  ];

  // Features: use project.goals as features
  const features = (project.goals || []).map((goal, i) => ({
    icon: <CheckCircle className="text-purple-500" />,
    title: `Goal ${i + 1}`,
    description: goal
  }));

  return (
    <div className="p-6 ml-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="mb-12">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">{project.name || 'About the Project'}</h1>
          <p className="text-gray-600 max-w-3xl">{project.summary}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>

        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold mb-6">Project Timeline</h2>
          <Timeline position="alternate">
            {milestones.map((milestone, index) => (
              <TimelineItem key={index}>
                <TimelineSeparator>
                  <TimelineDot 
                    sx={{
                      bgcolor: milestone.status === 'completed' ? '#22c55e' :
                             milestone.status === 'in-progress' ? '#3b82f6' :
                             milestone.status === 'blocked' ? '#ef4444' :
                             '#d1d5db'
                    }}
                  >
                    {milestone.icon}
                  </TimelineDot>
                  {index < milestones.length - 1 && <TimelineConnector />}
                </TimelineSeparator>
                <TimelineContent>
                  <div className={`p-4 rounded-lg ${index % 2 === 0 ? 'text-right' : 'text-left'}`}>
                    <h3 className="text-lg font-semibold">{milestone.title}</h3>
                    <p className="text-gray-500 text-sm">{milestone.date}</p>
                    <p className="text-gray-600 mt-1">{milestone.description}</p>
                  </div>
                </TimelineContent>
              </TimelineItem>
            ))}
          </Timeline>
        </motion.div>

        <motion.div
          className="mt-12 p-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h2 className="text-2xl font-bold mb-4">Get Involved</h2>
          <p className="mb-6">
            We're always looking for feedback and contributions to make our platform better.
            Join our community and help shape the future of project management.
          </p>
          <div className="flex space-x-4">
            <button className="px-6 py-2 bg-white text-blue-500 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
              Join Community
            </button>
            <button className="px-6 py-2 border-2 border-white rounded-lg font-semibold hover:bg-white hover:text-blue-500 transition-colors">
              Learn More
            </button>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default About; 