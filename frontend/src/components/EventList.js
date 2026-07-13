// frontend/src/components/EventList.js

import React, { useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Box,
  Typography,
  Paper,
  Badge
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  TrendingUp,
  TrendingDown
} from '@mui/icons-material';

const EventList = ({ events, associations, selectedEvent, onEventSelect }) => {
  const [expanded, setExpanded] = useState(null);

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'Very_High': return '#dc3545';
      case 'High': return '#ff6b35';
      case 'Medium': return '#ffc107';
      case 'Low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getImpactIcon = (impact) => {
    switch (impact) {
      case 'Very_High': return <Error />;
      case 'High': return <Warning />;
      case 'Medium': return <Info />;
      case 'Low': return <CheckCircle />;
      default: return <Info />;
    }
  };

  const getAssociation = (eventName) => {
    return associations.find(a => a.Event === eventName);
  };

  return (
    <List>
      {events.map((event, index) => {
        const association = getAssociation(event.Event_Name);
        const isSelected = selectedEvent?.Event_Name === event.Event_Name;
        const color = getImpactColor(event.Expected_Impact);
        
        return (
          <ListItem
            key={index}
            button
            selected={isSelected}
            onClick={() => onEventSelect(event)}
            style={{
              backgroundColor: isSelected ? '#e3f2fd' : 'transparent',
              borderLeft: isSelected ? `4px solid ${color}` : '4px solid transparent',
              marginBottom: 4,
              borderRadius: 4
            }}
          >
            <ListItemAvatar>
              <Avatar style={{ backgroundColor: color }}>
                {getImpactIcon(event.Expected_Impact)}
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={
                <Box display="flex" alignItems="center">
                  <Typography variant="body1" style={{ fontWeight: isSelected ? 'bold' : 'normal' }}>
                    {event.Event_Name}
                  </Typography>
                  {association && (
                    <Chip
                      size="small"
                      label={`${association.Percent_Change > 0 ? '+' : ''}${association.Percent_Change.toFixed(1)}%`}
                      style={{
                        marginLeft: 8,
                        backgroundColor: association.Percent_Change > 0 ? '#d4edda' : '#f8d7da',
                        color: association.Percent_Change > 0 ? '#155724' : '#721c24'
                      }}
                      icon={association.Percent_Change > 0 ? <TrendingUp /> : <TrendingDown />}
                    />
                  )}
                </Box>
              }
              secondary={
                <Box>
                  <Typography variant="caption" color="textSecondary">
                    {event.Date} • {event.Category}
                  </Typography>
                  {association && (
                    <Typography variant="caption" display="block" color="textSecondary">
                      Change: ${association.Price_Change.toFixed(2)} • Days apart: {association.Days_Difference}
                    </Typography>
                  )}
                </Box>
              }
            />
          </ListItem>
        );
      })}
    </List>
  );
};

export default EventList;