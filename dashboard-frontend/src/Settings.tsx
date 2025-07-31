import React, { useEffect, useState } from 'react';
import {
  Typography,
  Paper,
  TextField,
  Button,
  Box,
  List,
  ListItem,
  ListItemText,
  IconButton,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

interface Connector {
  id: string;
  name: string;
  type: string;
  connection_string: string;
}

function Settings() {
  const [connectors, setConnectors] = useState<Connector[]>([]);
  const [newConnector, setNewConnector] = useState({
    id: '',
    name: '',
    type: '',
    connection_string: '',
  });

  const fetchConnectors = async () => {
    try {
      const response = await fetch('http://localhost:8004/connectors');
      const data = await response.json();
      setConnectors(data || []);
    } catch (error) {
      console.error('Error fetching connectors:', error);
    }
  };

  useEffect(() => {
    fetchConnectors();
  }, []);

  const handleAddConnector = async () => {
    try {
      await fetch('http://localhost:8004/connectors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConnector),
      });
      fetchConnectors(); // Refresh the list
      setNewConnector({ id: '', name: '', type: '', connection_string: '' }); // Clear the form
    } catch (error) {
      console.error('Error adding connector:', error);
    }
  };

  const handleDeleteConnector = async (id: string) => {
    try {
      await fetch(`http://localhost:8004/connectors/${id}`, {
        method: 'DELETE',
      });
      fetchConnectors(); // Refresh the list
    } catch (error) {
      console.error('Error deleting connector:', error);
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      <Paper style={{ padding: '20px', marginBottom: '20px' }}>
        <Typography variant="h6" gutterBottom>
          Add New Connector
        </Typography>
        <TextField
          label="ID"
          value={newConnector.id}
          onChange={(e) => setNewConnector({ ...newConnector, id: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Name"
          value={newConnector.name}
          onChange={(e) => setNewConnector({ ...newConnector, name: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Type (e.g., mongodb, postgresql)"
          value={newConnector.type}
          onChange={(e) => setNewConnector({ ...newConnector, type: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <TextField
          label="Connection String"
          value={newConnector.connection_string}
          onChange={(e) => setNewConnector({ ...newConnector, connection_string: e.target.value })}
          fullWidth
          sx={{ mb: 1 }}
        />
        <Button variant="contained" onClick={handleAddConnector}>
          Add Connector
        </Button>
      </Paper>
      <Paper style={{ padding: '20px' }}>
        <Typography variant="h6" gutterBottom>
          Configured Connectors
        </Typography>
        <List>
          {connectors.map((connector) => (
            <ListItem
              key={connector.id}
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteConnector(connector.id)}>
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemText
                primary={connector.name}
                secondary={`${connector.type} - ${connector.connection_string}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </div>
  );
}

export default Settings;