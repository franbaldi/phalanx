
import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
} from '@mui/material';

interface GenericTransaction {
  user_id: string;
  timestamp: string;
  data: Record<string, any>;
}

interface Anomaly {
  transaction: GenericTransaction;
  reason: string;
}

interface AnomaliesProps {
  anomalies: Anomaly[];
}

function Anomalies({ anomalies }: AnomaliesProps) {
  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Detected Anomalies
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>User ID</TableCell>
              <TableCell>Timestamp</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Data</TableCell>
              <TableCell>Reason</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {anomalies.map((anomaly, index) => (
              <TableRow key={index}>
                <TableCell>{anomaly.transaction.user_id}</TableCell>
                <TableCell>{new Date(anomaly.transaction.timestamp).toLocaleString()}</TableCell>
                <TableCell>{anomaly.transaction.data.type}</TableCell>
                <TableCell>
                  <pre>{JSON.stringify(anomaly.transaction.data, null, 2)}</pre>
                </TableCell>
                <TableCell>{anomaly.reason}</TableCell>
                <TableCell>
                  <Button variant="contained" color="primary" size="small">
                    Investigate
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default Anomalies;
