
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Paper, Typography } from '@mui/material';

function ReportDetail() {
  const { reportName } = useParams<{ reportName: string }>();
  const [reportContent, setReportContent] = useState('');

  useEffect(() => {
    const fetchReportContent = async () => {
      try {
        const response = await fetch(`http://localhost:8002/reports/${reportName}`);
        const data = await response.text();
        setReportContent(data);
      } catch (error) {
        console.error('Error fetching report content:', error);
      }
    };

    fetchReportContent();
  }, [reportName]);

  return (
    <Paper style={{ padding: '20px' }}>
      <Typography variant="h5" gutterBottom>
        {reportName}
      </Typography>
      <pre>{reportContent}</pre>
    </Paper>
  );
}

export default ReportDetail;
