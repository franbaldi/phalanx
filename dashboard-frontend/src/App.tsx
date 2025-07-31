import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  CssBaseline,
  createTheme,
  ThemeProvider,
  Box,
  Link,
  Button,
} from '@mui/material';
import SecurityIcon from '@mui/icons-material/Security';
import SettingsIcon from '@mui/icons-material/Settings';
import DescriptionIcon from '@mui/icons-material/Description';
import Anomalies from './Anomalies';
import Reports from './Reports';
import ReportDetail from './ReportDetail';
import Settings from './Settings';

// Define a dark theme for the dashboard
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#764abc',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
});

interface Transaction {
  user_id: string;
  amount: number;
  currency: string;
  recipient: string;
  country: string;
  timestamp: string;
}

interface Anomaly {
  transaction: Transaction;
  reason: string;
}

function App() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/anomalies');

    ws.onopen = () => console.log('WebSocket connected');
    ws.onclose = () => console.log('WebSocket disconnected');
    ws.onerror = (error) => console.error('WebSocket Error:', error);

    ws.onmessage = (event) => {
      const newAnomaly = JSON.parse(event.data);
      setAnomalies((prevAnomalies) => [newAnomaly, ...prevAnomalies]);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <SecurityIcon sx={{ mr: 2 }} />
              <Typography variant="h6" noWrap component={RouterLink} to="/" sx={{ textDecoration: 'none', color: 'inherit' }}>
                Phalanx.ai Security Dashboard
              </Typography>
              <Box sx={{ flexGrow: 1 }} />
              <Button color="inherit" startIcon={<SettingsIcon />} component={RouterLink} to="/settings">
                Settings
              </Button>
              <Button color="inherit" startIcon={<DescriptionIcon />} component={RouterLink} to="/reports">
                Reports
              </Button>
            </Toolbar>
          </AppBar>
          <Container component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
            <Routes>
              <Route path="/" element={<Anomalies anomalies={anomalies} />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/reports/:reportName" element={<ReportDetail />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Container>
        </Box>
        <Box
          component="footer"
          sx={{
            p: 2,
            mt: 'auto',
            backgroundColor: (theme) => theme.palette.background.paper,
            textAlign: 'center',
            position: 'fixed',
            bottom: 0,
            width: '100%',
          }}
        >
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} Phalanx.ai -{' '}
            <Link color="inherit" href="https://github.com/franbaldi/phalanx">
              phalanx.ai
            </Link>
          </Typography>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;