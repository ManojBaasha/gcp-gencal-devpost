import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ResponsiveLine } from '@nivo/line';
import { ResponsivePie } from '@nivo/pie';
import { 
  Assignment, 
  BugReport, 
  CheckCircle, 
  Schedule 
} from '@mui/icons-material';
import { doc, getDoc, collection, getDocs } from 'firebase/firestore';
import db from '../firebase-config';

const MetricCard = ({ icon, title, value, trend }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="card"
  >
    <div className="flex items-center space-x-4">
      <div className="p-3 bg-blue-100 rounded-full">
        {icon}
      </div>
      <div>
        <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
        {trend !== undefined && (
          <p className={`text-sm ${trend >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}% from last week
          </p>
        )}
      </div>
    </div>
  </motion.div>
);

const Dashboard = () => {
  const [projectInfo, setProjectInfo] = useState(null);
  const [tasks, setTasks] = useState({ completed: [], active: [], pending: [], blocked: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      // Fetch project info
      const projectDoc = await getDoc(doc(db, 'project', 'info'));
      let project = null;
      if (projectDoc.exists()) {
        project = projectDoc.data();
      }
      // Fetch tasks by status
      const statuses = ['completed', 'active', 'pending', 'blocked'];
      const tasksData = {};
      for (const status of statuses) {
        const statusDoc = await getDoc(doc(db, 'tasks', status));
        tasksData[status] = statusDoc.exists() ? statusDoc.data().items || [] : [];
      }
      setProjectInfo(project);
      setTasks(tasksData);
      setLoading(false);
    };
    fetchData();
  }, []);

  // Metrics
  const totalTasks = tasks.completed.length + tasks.active.length + tasks.pending.length + tasks.blocked.length;
  const completedTasks = tasks.completed.length;
  const openIssues = tasks.blocked.length;
  const sprintProgress = projectInfo && projectInfo.status && projectInfo.status.progress_percent ? projectInfo.status.progress_percent : 0;

  // Nivo chart data
  const sprintProgressData = [
    {
      id: 'tasks',
      data: [
        { x: 'Week 1', y: 0 },
        { x: 'Week 2', y: projectInfo?.status?.progress_percent || 0 },
        { x: 'Week 3', y: Math.min(100, (projectInfo?.status?.progress_percent || 0) + 20) },
        { x: 'Week 4', y: 100 }
      ]
    }
  ];
  const taskDistribution = [
    { id: 'Completed', value: completedTasks, color: 'hsl(152, 70%, 50%)' },
    { id: 'Active', value: tasks.active.length, color: 'hsl(241, 70%, 50%)' },
    { id: 'Blocked', value: openIssues, color: 'hsl(0, 70%, 50%)' },
    { id: 'Pending', value: tasks.pending.length, color: 'hsl(206, 70%, 50%)' }
  ];

  if (loading || !projectInfo) {
    return (
      <div className="p-6 ml-16 flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6 ml-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-800 mb-2">{projectInfo.name || 'Project Overview'}</h1>
        <p className="text-gray-600 mb-8 max-w-2xl">{projectInfo.summary}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            icon={<Assignment className="text-blue-500" />}
            title="Total Tasks"
            value={totalTasks}
          />
          <MetricCard
            icon={<CheckCircle className="text-green-500" />}
            title="Completed"
            value={completedTasks}
          />
          <MetricCard
            icon={<BugReport className="text-red-500" />}
            title="Blocked"
            value={openIssues}
          />
          <MetricCard
            icon={<Schedule className="text-purple-500" />}
            title="Sprint Progress"
            value={`${sprintProgress}%`}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            className="card"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-xl font-semibold mb-4">Sprint Progress</h2>
            <div className="h-80">
              <ResponsiveLine
                data={sprintProgressData}
                margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 0, max: 'auto' }}
                curve="cardinal"
                axisTop={null}
                axisRight={null}
                axisBottom={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                }}
                pointSize={10}
                pointColor={{ theme: 'background' }}
                pointBorderWidth={2}
                pointBorderColor={{ from: 'serieColor' }}
                pointLabelYOffset={-12}
                useMesh={true}
                legends={[
                  {
                    anchor: 'bottom-right',
                    direction: 'column',
                    justify: false,
                    translateX: 100,
                    translateY: 0,
                    itemsSpacing: 0,
                    itemDirection: 'left-to-right',
                    itemWidth: 80,
                    itemHeight: 20,
                    itemOpacity: 0.75,
                    symbolSize: 12,
                    symbolShape: 'circle',
                    symbolBorderColor: 'rgba(0, 0, 0, .5)',
                  }
                ]}
              />
            </div>
          </motion.div>

          <motion.div
            className="card"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h2 className="text-xl font-semibold mb-4">Task Distribution</h2>
            <div className="h-80">
              <ResponsivePie
                data={taskDistribution}
                margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                innerRadius={0.5}
                padAngle={0.7}
                cornerRadius={3}
                activeOuterRadiusOffset={8}
                borderWidth={1}
                borderColor={{ from: 'color', modifiers: [ [ 'darker', 0.2 ] ] }}
                arcLinkLabelsSkipAngle={10}
                arcLinkLabelsTextColor="#333333"
                arcLinkLabelsThickness={2}
                arcLinkLabelsColor={{ from: 'color' }}
                arcLabelsSkipAngle={10}
                arcLabelsTextColor={{ from: 'color', modifiers: [ [ 'darker', 2 ] ] }}
                legends={[
                  {
                    anchor: 'bottom',
                    direction: 'row',
                    justify: false,
                    translateX: 0,
                    translateY: 56,
                    itemsSpacing: 0,
                    itemWidth: 100,
                    itemHeight: 18,
                    itemTextColor: '#999',
                    itemDirection: 'left-to-right',
                    itemOpacity: 1,
                    symbolSize: 18,
                    symbolShape: 'circle',
                  }
                ]}
              />
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard; 