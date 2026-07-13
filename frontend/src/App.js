// src/App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  CircularProgress,
  Alert,
  Card,
  CardContent
} from '@mui/material';
import {
  Dashboard as DashboardIcon
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
  ReferenceLine,
  BarChart,
  Bar
} from 'recharts';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [priceData, setPriceData] = useState({ dates: [], prices: [] });
  const [events, setEvents] = useState([]);
  const [associations, setAssociations] = useState([]);
  const [summary, setSummary] = useState(null);
  const [impactByCategory, setImpactByCategory] = useState({});
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      setError(null);

      const pricesRes = await axios.get(API_URL + '/prices');
      const eventsRes = await axios.get(API_URL + '/events');
      const associationsRes = await axios.get(API_URL + '/associations');
      const summaryRes = await axios.get(API_URL + '/summary');
      const impactRes = await axios.get(API_URL + '/impact-by-category');

      setPriceData(pricesRes.data);
      setEvents(eventsRes.data || []);
      setAssociations(associationsRes.data || []);
      setSummary(summaryRes.data);
      setImpactByCategory(impactRes.data || {});

    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data. Please make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleDateFilter = async () => {
    if (!startDate || !endDate) return;
    
    try {
      const params = {
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0]
      };
      const response = await axios.get(API_URL + '/prices', { params });
      setPriceData(response.data);
    } catch (err) {
      console.error('Error filtering data:', err);
    }
  };

  const handleReset = async () => {
    setStartDate(null);
    setEndDate(null);
    await fetchAllData();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
        <Typography variant="h6" style={{ marginLeft: 16 }}>
          Loading dashboard...
        </Typography>
      </Box>
    );
  }

  const chartData = priceData.dates.map((date, index) => ({
    date: date,
    price: priceData.prices[index]
  }));

  const impactChartData = Object.entries(impactByCategory).map(([category, values]) => ({
    category: category,
    'Mean Change (%)': values.mean || 0,
    count: values.count || 0
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ backgroundColor: 'white', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{label}</p>
          <p style={{ margin: 0, color: '#1976d2' }}>Price: ${payload[0].value.toFixed(2)}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <AppBar position="static" color="primary">
        <Toolbar>
          <IconButton edge="start" color="inherit">
            <DashboardIcon />
          </IconButton>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Brent Oil Price Dashboard
          </Typography>
          <Typography variant="body2">
            {summary?.date_range?.start} - {summary?.date_range?.end}
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" style={{ marginTop: 24 }}>
        {error && (
          <Alert severity="error" style={{ marginBottom: 16 }}>
            {error}
          </Alert>
        )}

        {/* Summary Cards */}
        <Grid container spacing={3} style={{ marginBottom: 16 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>Price Range</Typography>
                <Typography variant="h5" style={{ fontWeight: 'bold' }}>
                  ${summary?.price_stats?.min?.toFixed(2)} - ${summary?.price_stats?.max?.toFixed(2)}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Avg: ${summary?.price_stats?.mean?.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>Observations</Typography>
                <Typography variant="h5" style={{ fontWeight: 'bold' }}>
                  {summary?.total_observations?.toLocaleString() || '0'}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Data points
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>Total Events</Typography>
                <Typography variant="h5" style={{ fontWeight: 'bold' }}>
                  {summary?.total_events || '0'}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {summary?.total_associations || 0} associated with changes
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>Price Volatility</Typography>
                <Typography variant="h5" style={{ fontWeight: 'bold' }}>
                  ${summary?.price_stats?.std?.toFixed(2)}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Standard deviation
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Date Filter */}
        <Paper style={{ padding: 16, marginBottom: 16 }}>
          <Typography variant="h6" gutterBottom>Date Range Filter</Typography>
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
                customInput={<input className="form-control" style={{ width: '100%', padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }} />}
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
                customInput={<input className="form-control" style={{ width: '100%', padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }} />}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box display="flex" gap={1}>
                <button onClick={handleDateFilter} style={{ padding: '8px 16px', backgroundColor: '#1976d2', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  Apply Filter
                </button>
                <button onClick={handleReset} style={{ padding: '8px 16px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  Reset
                </button>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        {/* Charts */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper style={{ padding: 16 }}>
              <Typography variant="h6" gutterBottom>Brent Oil Price History</Typography>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} interval="preserveStartEnd" />
                  <YAxis domain={['auto', 'auto']} tickFormatter={(value) => '$' + value} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#1976d2" strokeWidth={2} dot={false} name="Brent Oil Price" />
                  
                  {associations.slice(0, 10).map((assoc, index) => {
                    const idx = priceData.dates.indexOf(assoc.Change_Date);
                    if (idx === -1) return null;
                    return (
                      <ReferenceLine
                        key={index}
                        x={assoc.Change_Date}
                        stroke="#dc3545"
                        strokeDasharray="5 5"
                        label={{ value: '📌', position: 'top', fontSize: 16 }}
                      />
                    );
                  })}
                </ComposedChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper style={{ padding: 16, maxHeight: 500, overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>Key Events</Typography>
              {events.slice(0, 10).map((event, index) => {
                const assoc = associations.find(a => a.Event === event.Event_Name);
                return (
                  <div key={index} style={{ 
                    padding: '8px 12px', 
                    marginBottom: '8px', 
                    backgroundColor: '#f5f5f5', 
                    borderRadius: '4px',
                    borderLeft: '4px solid ' + (assoc?.Percent_Change > 0 ? '#28a745' : '#dc3545')
                  }}>
                    <Typography variant="body2" style={{ fontWeight: 'bold' }}>{event.Event_Name}</Typography>
                    <Typography variant="caption" color="textSecondary">{event.Date}</Typography>
                    {assoc && (
                      <Typography variant="caption" display="block" color="textSecondary">
                        Change: {assoc.Percent_Change > 0 ? '+' : ''}{assoc.Percent_Change.toFixed(1)}%
                      </Typography>
                    )}
                  </div>
                );
              })}
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16 }}>
              <Typography variant="h6" gutterBottom>Impact by Category</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={impactChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis label={{ value: 'Change (%)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="Mean Change (%)" fill="#1976d2" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16 }}>
              <Typography variant="h6" gutterBottom>Top Events by Impact</Typography>
              {associations
                .sort((a, b) => Math.abs(b.Percent_Change) - Math.abs(a.Percent_Change))
                .slice(0, 5)
                .map((assoc, index) => (
                  <div key={index} style={{ marginBottom: 8, padding: '8px 12px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
                    <Typography variant="body2" style={{ fontWeight: 'bold' }}>{assoc.Event}</Typography>
                    <Box display="flex" justifyContent="space-between">
                      <Typography variant="caption" color="textSecondary">{assoc.Event_Date}</Typography>
                      <Typography variant="body2" style={{ color: assoc.Percent_Change > 0 ? 'green' : 'red', fontWeight: 'bold' }}>
                        {assoc.Percent_Change > 0 ? '+' : ''}{assoc.Percent_Change.toFixed(1)}%
                      </Typography>
                    </Box>
                  </div>
                ))}
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default App;