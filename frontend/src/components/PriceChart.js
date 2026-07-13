// frontend/src/components/PriceChart.js

import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Scatter,
  ComposedChart
} from 'recharts';

const PriceChart = ({ data, events, associations, selectedEvent, onEventSelect }) => {
  const [hoveredPoint, setHoveredPoint] = useState(null);

  // Prepare chart data
  const chartData = data.dates.map((date, index) => ({
    date: date,
    price: data.prices[index]
  }));

  // Add event markers
  const eventData = events.map(event => {
    const idx = data.dates.indexOf(event.Date);
    return {
      ...event,
      price: idx !== -1 ? data.prices[idx] : null
    };
  });

  // Filter associations that have valid data
  const validAssociations = associations.filter(assoc => {
    const idx = data.dates.indexOf(assoc.Change_Date);
    return idx !== -1;
  });

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          backgroundColor: 'white',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{label}</p>
          <p style={{ margin: 0, color: '#1976d2' }}>
            Price: ${payload[0].value.toFixed(2)}
          </p>
          {selectedEvent && (
            <p style={{ margin: 0, color: '#dc3545', fontSize: '12px' }}>
              📌 {selectedEvent.Event_Name}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
        <XAxis 
          dataKey="date" 
          tick={{ fontSize: 10 }}
          interval="preserveStartEnd"
          tickFormatter={(value) => {
            const date = new Date(value);
            return `${date.getFullYear()}`;
          }}
        />
        <YAxis 
          domain={['auto', 'auto']}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />

        {/* Price Line */}
        <Line
          type="monotone"
          dataKey="price"
          stroke="#1976d2"
          strokeWidth={2}
          dot={false}
          name="Brent Oil Price"
        />

        {/* Event Reference Lines */}
        {validAssociations.map((assoc, index) => {
          const idx = data.dates.indexOf(assoc.Change_Date);
          if (idx === -1) return null;
          
          return (
            <ReferenceLine
              key={index}
              x={assoc.Change_Date}
              stroke="#dc3545"
              strokeDasharray="5 5"
              label={{
                value: assoc.Event.substring(0, 10) + '...',
                position: 'top',
                fill: '#dc3545',
                fontSize: 10,
                angle: -45
              }}
            />
          );
        })}

        {/* Event Points */}
        {eventData.map((event, index) => {
          if (event.price === null) return null;
          return (
            <ReferenceLine
              key={`event-${index}`}
              x={event.Date}
              stroke="#ffc107"
              strokeWidth={2}
              label={{
                value: '📌',
                position: 'top',
                fontSize: 16
              }}
              onClick={() => onEventSelect(event)}
            />
          );
        })}
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;