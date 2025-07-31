
import React, { useEffect, useState } from 'react';
import {
  Typography,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

interface Policy {
  id: string;
  name: string;
  description: string;
  data_type: string;
  rules: any[];
}

function Policies() {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [newPolicy, setNewPolicy] = useState({
    id: '',
    name: '',
    description: '',
    data_type: '',
    rules: [],
  });

  const fetchPolicies = async () => {
    try {
      const response = await fetch('http://localhost:8005/policies');
      const data = await response.json();
      setPolicies(data || []);
    } catch (error) {
      console.error('Error fetching policies:', error);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleAddPolicy = async () => {
    try {
      await fetch('http://localhost:8005/policies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPolicy),
      });
      fetchPolicies(); // Refresh the list
      setNewPolicy({ id: '', name: '', description: '', data_type: '', rules: [] }); // Clear the form
    } catch (error) {
      console.error('Error adding policy:', error);
    }
  };

  const handleDeletePolicy = async (id: string) => {
    try {
      await fetch(`http://localhost:8005/policies/${id}`, {
        method: 'DELETE',
      });
      fetchPolicies(); // Refresh the list
    } catch (error) {
      console.error('Error deleting policy:', error);
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Policies
      </Typography>
      <Paper style={{ padding: '20px', marginBottom: '20px' }}>
        <Typography variant="h6" gutterBottom>
          Add New Policy
        </Typography>
        <TextField
          label="ID"
          value={newPolicy.id}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPolicy({ ...newPolicy, id: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Name"
          value={newPolicy.name}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPolicy({ ...newPolicy, name: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Description"
          value={newPolicy.description}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPolicy({ ...newPolicy, description: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Data Type (e.g., transaction, loan_application)"
          value={newPolicy.data_type}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPolicy({ ...newPolicy, data_type: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <Button variant="contained" onClick={handleAddPolicy}>
          Add Policy
        </Button>
      </Paper>
      <Paper style={{ padding: '20px' }}>
        <Typography variant="h6" gutterBottom>
          Configured Policies
        </Typography>
        <List>
          {policies.map((policy) => (
            <ListItem
              key={policy.id}
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeletePolicy(policy.id)}>
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemText
                primary={policy.name}
                secondary={`${policy.data_type} - ${policy.description}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </div>
  );
}

export default Policies;
