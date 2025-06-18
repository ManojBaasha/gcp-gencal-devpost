import React from 'react';
import { motion } from 'framer-motion';
import { ResponsiveBar } from '@nivo/bar';
import { 
  Star,
  AccessTime,
  CheckCircle,
  Warning,
  Block
} from '@mui/icons-material';

const MemberCard = ({ member }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="card"
  >
    <div className="flex items-start space-x-4">
      <img
        src={member.avatar}
        alt={member.name}
        className="w-12 h-12 rounded-full"
      />
      <div className="flex-1">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold">{member.name}</h3>
            <p className="text-gray-600">{member.role}</p>
          </div>
          {member.performance >= 90 && (
            <Star className="text-yellow-400" />
          )}
        </div>
        
        <div className="mt-4">
          <div className="flex justify-between mb-2">
            <span className="text-sm text-gray-600">Sprint Progress</span>
            <span className="text-sm font-semibold">{member.progress}%</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full">
            <div
              className="h-full bg-blue-500 rounded-full"
              style={{ width: `${member.progress}%` }}
            />
          </div>
        </div>

        <div className="mt-4 grid grid-cols-4 gap-2 text-center text-sm">
          <div className="p-2 bg-green-100 rounded-lg">
            <CheckCircle className="mx-auto text-green-500 mb-1" />
            <span className="block font-semibold">{member.completed}</span>
            <span className="text-gray-600">Done</span>
          </div>
          <div className="p-2 bg-blue-100 rounded-lg">
            <AccessTime className="mx-auto text-blue-500 mb-1" />
            <span className="block font-semibold">{member.inProgress}</span>
            <span className="text-gray-600">Active</span>
          </div>
          <div className="p-2 bg-yellow-100 rounded-lg">
            <Warning className="mx-auto text-yellow-500 mb-1" />
            <span className="block font-semibold">{member.pending}</span>
            <span className="text-gray-600">Pending</span>
          </div>
          <div className="p-2 bg-red-100 rounded-lg">
            <Block className="mx-auto text-red-500 mb-1" />
            <span className="block font-semibold">{member.blocked}</span>
            <span className="text-gray-600">Blocked</span>
          </div>
        </div>
      </div>
    </div>
  </motion.div>
);

const TeamProgress = () => {
  // Sample data - replace with real data
  const teamMembers = [
    {
      name: 'Sarah Johnson',
      role: 'Frontend Developer',
      avatar: 'https://i.pravatar.cc/150?img=1',
      progress: 85,
      performance: 95,
      completed: 12,
      inProgress: 3,
      pending: 4,
      blocked: 1
    },
    {
      name: 'Michael Chen',
      role: 'Backend Developer',
      avatar: 'https://i.pravatar.cc/150?img=2',
      progress: 92,
      performance: 90,
      completed: 15,
      inProgress: 2,
      pending: 2,
      blocked: 0
    },
    {
      name: 'Emily Rodriguez',
      role: 'UI/UX Designer',
      avatar: 'https://i.pravatar.cc/150?img=3',
      progress: 78,
      performance: 88,
      completed: 8,
      inProgress: 4,
      pending: 3,
      blocked: 2
    },
    {
      name: 'David Kim',
      role: 'Full Stack Developer',
      avatar: 'https://i.pravatar.cc/150?img=4',
      progress: 95,
      performance: 92,
      completed: 18,
      inProgress: 2,
      pending: 1,
      blocked: 0
    }
  ];

  const productivityData = [
    {
      member: 'Sarah',
      'Story Points': 34,
      'Story PointsColor': 'hsl(190, 70%, 50%)',
      'Bugs Fixed': 12,
      'Bugs FixedColor': 'hsl(95, 70%, 50%)',
      'Code Reviews': 8,
      'Code ReviewsColor': 'hsl(340, 70%, 50%)'
    },
    {
      member: 'Michael',
      'Story Points': 45,
      'Story PointsColor': 'hsl(190, 70%, 50%)',
      'Bugs Fixed': 8,
      'Bugs FixedColor': 'hsl(95, 70%, 50%)',
      'Code Reviews': 15,
      'Code ReviewsColor': 'hsl(340, 70%, 50%)'
    },
    {
      member: 'Emily',
      'Story Points': 28,
      'Story PointsColor': 'hsl(190, 70%, 50%)',
      'Bugs Fixed': 5,
      'Bugs FixedColor': 'hsl(95, 70%, 50%)',
      'Code Reviews': 6,
      'Code ReviewsColor': 'hsl(340, 70%, 50%)'
    },
    {
      member: 'David',
      'Story Points': 52,
      'Story PointsColor': 'hsl(190, 70%, 50%)',
      'Bugs Fixed': 15,
      'Bugs FixedColor': 'hsl(95, 70%, 50%)',
      'Code Reviews': 12,
      'Code ReviewsColor': 'hsl(340, 70%, 50%)'
    }
  ];

  return (
    <div className="p-6 ml-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Team Progress</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {teamMembers.map((member) => (
            <MemberCard key={member.name} member={member} />
          ))}
        </div>

        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold mb-6">Sprint Productivity</h2>
          <div className="h-96">
            <ResponsiveBar
              data={productivityData}
              keys={['Story Points', 'Bugs Fixed', 'Code Reviews']}
              indexBy="member"
              margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
              padding={0.3}
              valueScale={{ type: 'linear' }}
              indexScale={{ type: 'band', round: true }}
              colors={{ scheme: 'nivo' }}
              borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
              axisTop={null}
              axisRight={null}
              axisBottom={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: 'Team Member',
                legendPosition: 'middle',
                legendOffset: 32
              }}
              axisLeft={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: 'Count',
                legendPosition: 'middle',
                legendOffset: -40
              }}
              labelSkipWidth={12}
              labelSkipHeight={12}
              labelTextColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
              legends={[
                {
                  dataFrom: 'keys',
                  anchor: 'bottom-right',
                  direction: 'column',
                  justify: false,
                  translateX: 120,
                  translateY: 0,
                  itemsSpacing: 2,
                  itemWidth: 100,
                  itemHeight: 20,
                  itemDirection: 'left-to-right',
                  itemOpacity: 0.85,
                  symbolSize: 20,
                  effects: [
                    {
                      on: 'hover',
                      style: {
                        itemOpacity: 1
                      }
                    }
                  ]
                }
              ]}
              animate={true}
              motionStiffness={90}
              motionDamping={15}
            />
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default TeamProgress; 