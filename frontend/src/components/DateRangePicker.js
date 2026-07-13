// frontend/src/components/DateRangePicker.js

import React, { useState } from 'react';
import { Box, Button, TextField, Grid } from '@mui/material';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const DateRangePicker = ({ onDateChange }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleApply = () => {
    if (startDate && endDate) {
      const start = startDate.toISOString().split('T')[0];
      const end = endDate.toISOString().split('T')[0];
      onDateChange(start, end);
    }
  };

  const handleReset = () => {
    setStartDate(null);
    setEndDate(null);
    onDateChange(null, null);
  };

  return (
    <Box>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={4}>
          <DatePicker
            selected={startDate}
            onChange={date => setStartDate(date)}
            selectsStart
            startDate={startDate}
            endDate={endDate}
            placeholderText="Start Date"
            className="form-control"
            customInput={<TextField fullWidth label="Start Date" variant="outlined" />}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <DatePicker
            selected={endDate}
            onChange={date => setEndDate(date)}
            selectsEnd
            startDate={startDate}
            endDate={endDate}
            minDate={startDate}
            placeholderText="End Date"
            className="form-control"
            customInput={<TextField fullWidth label="End Date" variant="outlined" />}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <Box display="flex" gap={1}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleApply}
              disabled={!startDate || !endDate}
            >
              Apply Filter
            </Button>
            <Button
              variant="outlined"
              onClick={handleReset}
            >
              Reset
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DateRangePicker;