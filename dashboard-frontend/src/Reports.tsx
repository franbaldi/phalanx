
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemText, Typography } from '@mui/material';

function Reports() {
  const [reports, setReports] = useState<string[]>([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch('http://localhost:8002/reports');
        const data = await response.json();
        setReports(data.reports || []);
      } catch (error) {
        console.error('Error fetching reports:', error);
      }
    };

    fetchReports();
  }, []);

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        DORA Reports
      </Typography>
      <List>
        {reports.map((report, index) => (
          <ListItem key={index} component={Link} to={`/reports/${report}`}>
            <ListItemText primary={report} />
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default Reports;
