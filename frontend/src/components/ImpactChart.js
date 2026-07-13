// frontend/src/components/ImpactChart.js

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

const ImpactChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <p>No data available</p>
        </div>
      </ResponsiveContainer>
    );
  }

  // Transform data for chart
  const chartData = Object.entries(data).map(([category, values]) => ({
    category: category,
    'Mean Change (%)': values.mean || 0,
    count: values.count || 0,
    std: values.std || 0
  }));

  const colors = ['#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#d32f2f', '#0288d1'];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'white',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{data.category}</p>
          <p style={{ margin: 0 }}>Mean Change: {data['Mean Change (%)'].toFixed(1)}%</p>
          <p style={{ margin: 0 }}>Events: {data.count}</p>
          <p style={{ margin: 0 }}>Std Dev: {data.std.toFixed(1)}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
        <XAxis dataKey="category" />
        <YAxis label={{ value: 'Change (%)', angle: -90, position: 'insideLeft' }} />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar dataKey="Mean Change (%)" fill="#1976d2">
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default ImpactChart;