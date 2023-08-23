import React, { useState, useEffect } from 'react';
import {
  Container,
  TextField,
  Button,
  List,
  ListItem,
  Typography,
  Grid,
  Snackbar,
  Alert,
  Box,
} from '@mui/material';
import TcgCard from './TcgCard';

import { URL } from './settings';

function DeckBuilder({ cards }) {
  const [currentDeck, setCurrentDeck] = useState([]);
  const [decks, setDecks] = useState([]);
  const [userName, setUserName] = useState(localStorage.getItem('userName') || ''); // Retrieve from localStorage
  const [deckName, setDeckName] = useState('');
  const [toastOpen, setToastOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedDeck, setSelectedDeck] = useState(null); // For highlighting the selected deck

  const [hostGameId, setHostGameId] = useState(''); // For displaying gameId
  const [joinGameId, setJoinGameId] = useState(''); // For entering gameId

  const hostGame = () => {
    const data = {
      deckId: selectedDeck.id, // Assuming each deck object has an 'id' property
      username: userName
    };

    fetch(`${URL}/api/host_game`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.error);
        });
      }
      return response.json();
    })
    .then(data => {
      setHostGameId(data.gameId); // Display the received gameId
    })
    .catch(error => {
      setErrorMessage(error.message);
      setToastOpen(true);
    });
  };

  const joinGame = () => {
    const data = {
      deckId: selectedDeck.id,
      username: userName,
      gameId: joinGameId
    };

    fetch(`${URL}/api/join_game`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.error);
        });
      }
      // Handle successful join, if necessary
    })
    .catch(error => {
      setErrorMessage(error.message);
      setToastOpen(true);
    });
  };  

  useEffect(() => {
    // Fetch decks and other initial setup

    // Set the userName in localStorage whenever it changes
    localStorage.setItem('userName', userName);
  }, [userName]);

  const fetchDecks = () => {
    fetch(`${URL}/api/decks?username=${userName}`)
      .then(response => response.json())
      .then(data => setDecks(data))
      .catch(error => {
        setErrorMessage("Failed to fetch decks.");
        setToastOpen(true);
      });
  }

  useEffect(fetchDecks, [userName]);

  const addToDeck = (cardName) => {
    setCurrentDeck([...currentDeck, cardName]);
  };

  const saveDeck = () => {
    const deckData = {
      name: deckName,
      username: userName,
      cards: currentDeck,
    };

    fetch(`${URL}/api/decks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(deckData)
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.error);
        });
      }
      return response.json();
    })
    .then(data => {
      setDecks(prevDecks => [...prevDecks, data]); // Assuming your backend returns the saved deck
      setCurrentDeck([]);
      setDeckName('');
    })
    .catch(error => {
      setErrorMessage(error.message);
      setToastOpen(true);
    });
  };

  const handleCloseToast = () => {
    setToastOpen(false);
  };

  return (
    <Container>
      <Typography variant="h5">Deck Builder</Typography>
      
      <TextField 
        label="User Name" 
        variant="outlined" 
        margin="normal"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      
      <TextField 
        label="Deck Name" 
        variant="outlined" 
        margin="normal"
        value={deckName}
        onChange={(e) => setDeckName(e.target.value)}
      />
      
      <Button variant="contained" color="primary" onClick={saveDeck} style={{ marginBottom: '20px' }}>
        Save Deck
      </Button>

      {/* Host and Join game actions */}
      <Grid container spacing={2} alignItems="center" style={{ marginTop: '20px' }}>
        <Grid item>
          <Button variant="contained" color="primary" onClick={hostGame}>
            Host Game
          </Button>
        </Grid>
        <Grid item>
          <TextField 
            variant="outlined"
            label="Game ID"
            value={joinGameId}
            onChange={(e) => setJoinGameId(e.target.value)}
          />
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={joinGame}>
            Join Game
          </Button>
        </Grid>
      </Grid>

      {/* Display Game ID when hosting a game */}
      {hostGameId && (
        <Typography variant="h6" style={{ marginTop: '20px' }}>
          Game ID: {hostGameId}
        </Typography>
      )}

      <Typography variant="h6">Current Deck:</Typography>
      <List>
        {currentDeck.map((cardName, index) => (
          <ListItem key={index}>{cardName}</ListItem>
        ))}
      </List>

      <Typography variant="h6" style={{ marginTop: '20px' }}>All Decks:</Typography>
      {decks.map((deck, index) => (
        <Box 
          key={index}
          component="button"
          display="block"
          border={deck === selectedDeck ? "2px solid #3f51b5" : "none"} // Highlight if selected
          borderRadius="4px"
          padding="10px"
          margin="5px 0"
          textAlign="left"
          onClick={() => setSelectedDeck(deck)}
        >
          {deck.name}
        </Box>
      ))}

      <Typography variant="h6" style={{ marginTop: '20px' }}>Available Cards:</Typography>
      <Grid container spacing={3}>
        {cards.map((card) => (
          <Grid item key={card.name} xs={12} sm={6} md={4} lg={3} onClick={() => addToDeck(card.name)}>
            <TcgCard card={card} />
          </Grid>
        ))}
      </Grid>

      <Snackbar 
        open={toastOpen}
        autoHideDuration={6000}
        onClose={handleCloseToast}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseToast} severity="error" variant="filled">
          {errorMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default DeckBuilder;