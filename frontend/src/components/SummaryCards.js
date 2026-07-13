// frontend/src/components/SummaryCards.js

import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AttachMoney,
  CalendarToday,
  Event,
  Assessment
} from '@mui/icons-material';

const SummaryCards = ({ summary }) => {
  if (!summary) {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography>Loading summary...</Typography>
        </Grid>
      </Grid>
    );
  }

  const cards = [
    {
      title: 'Price Range',
      value: `$${summary.price_stats?.min?.toFixed(2)} - $${summary.price_stats?.max?.toFixed(2)}`,
      subtitle: `Avg: $${summary.price_stats?.mean?.toFixed(2)}`,
      icon: <AttachMoney />,
      color: '#1976d2'
    },
    {
      title: 'Observations',
      value: summary.total_observations?.toLocaleString() || '0',
      subtitle: `${summary.date_range?.start} to ${summary.date_range?.end}`,
      icon: <CalendarToday />,
      color: '#2e7d32'
    },
    {
      title: 'Total Events',
      value: summary.total_events || '0',
      subtitle: `${summary.total_associations || 0} associated with changes`,
      icon: <Event />,
      color: '#ed6c02'
    },
    {
      title: 'Price Volatility',
      value: `$${summary.price_stats?.std?.toFixed(2)}`,
      subtitle: 'Standard deviation',
      icon: <Assessment />,
      color: '#9c27b0'
    }
  ];

  return (
    <Grid container spacing={3}>
      {cards.map((card, index) => (
        <Grid item xs={12} sm={6} md={3} key={index}>
          <Card style={{ height: '100%' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    {card.title}
                  </Typography>
                  <Typography variant="h5" style={{ fontWeight: 'bold' }}>
                    {card.value}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {card.subtitle}
                  </Typography>
                </Box>
                <Box
                  style={{
                    backgroundColor: card.color,
                    color: 'white',
                    borderRadius: '50%',
                    padding: 8,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  {card.icon}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default SummaryCards;