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
              <TableCell>Amount</TableCell>
              <TableCell>Currency</TableCell>
              <TableCell>Recipient</TableCell>
              <TableCell>Country</TableCell>
              <TableCell>Reason</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {anomalies.map((anomaly, index) => (
              <TableRow key={index}>
                <TableCell>{anomaly.transaction.user_id}</TableCell>
                <TableCell>{new Date(anomaly.transaction.timestamp).toLocaleString()}</TableCell>
                <TableCell>{anomaly.transaction.amount}</TableCell>
                <TableCell>{anomaly.transaction.currency}</TableCell>
                <TableCell>{anomaly.transaction.recipient}</TableCell>
                <TableCell>{anomaly.transaction.country}</TableCell>
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