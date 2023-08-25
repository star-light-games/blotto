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
  CardContent,
  Card,
} from '@mui/material';
import TcgCard from './TcgCard';

import { URL } from './settings';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

import TopBar from './TopBar.js';


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

  const navigate = useNavigate();

  const hostGame = () => {
    const data = {
      deckId: selectedDeck.id, // Assuming each deck object has an 'id' property
      username: userName,
      rand: Math.random(), // To prevent caching
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
      gameId: joinGameId,
      rand: Math.random(), // To prevent caching
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
    .then(() => {
      navigate(`/game/${joinGameId}?playerNum=1`); // Redirect to the game page
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
    fetch(`${URL}/api/decks?username=${userName}&rand=${Math.random()}}`)
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
      rand: Math.random(), // To prevent caching
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
      <TopBar />
      <Typography variant="h5">Deck Builder</Typography>
      
      
  <TextField 
    label="User Name" 
    variant="outlined" 
    margin="normal"
    value={userName}
    onChange={(e) => setUserName(e.target.value)}
  />

  <Card>
    <CardContent>
    <Typography variant="h6" style={{ marginTop: '20px' }}>All Your Created Decks:</Typography>
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
      {/* Host and Join game actions */}
      <Grid container spacing={2} alignItems="center" style={{ marginTop: '20px' }}>
        <Grid item>
          <Button variant="contained" color="primary" onClick={hostGame} disabled={!selectedDeck}>
            {selectedDeck ? 'Host Game' : 'Select Deck'}
          </Button>
        </Grid>
        <Grid item>
          {/* Display Game ID when hosting a game */}
          {hostGameId && (
            <Typography variant="h6" style={{ marginTop: '20px' }}>
              Game ID: <Link to={`/game/${hostGameId}?playerNum=0`}>{hostGameId}</Link>
            </Typography>
          )}
        </Grid>
        </Grid>

      <Grid container spacing={2} alignItems="center" style={{ marginTop: '20px' }}>
        <Grid item>
          <TextField 
            variant="outlined"
            label="Game ID"
            value={joinGameId}
            onChange={(e) => setJoinGameId(e.target.value)}
          />
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={joinGame} disabled={!selectedDeck}>
            {selectedDeck ? 'Join Game' : 'Select Deck'}
          </Button>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
  
  {/*space between the two cards*/}
  <br></br>

  {/* A card with the title create a new deck 
  that contains a text feild and create deck button */}
<Card>
  <CardContent>
    <Typography variant="h6" style={{ marginTop: '20px' }}>Create a New Deck:</Typography>
    
    <Grid container alignItems="center" spacing={2}>
      <Grid item>
        <TextField 
          label="Deck Name" 
          variant="outlined" 
          value={deckName}
          onChange={(e) => setDeckName(e.target.value)}
        />
      </Grid>
      
      <Grid item>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={saveDeck} 
          disabled={!userName || !deckName || !currentDeck || currentDeck.length === 0}>
          {!userName ? 'Enter User Name' : !deckName ? 'Enter Deck Name' : !currentDeck || currentDeck.length === 0 ? 'Add Cards to Deck' : 'Save Deck'}
        </Button>
      </Grid>
    </Grid>
    </CardContent>
    <CardContent>
    <Typography variant="h6">Deck You Are Building:</Typography>
      <List>
        {currentDeck.map((cardName, index) => (
          <ListItem key={index}>{cardName}</ListItem>
        ))}
      </List>
  </CardContent>

  <CardContent>
     <Typography variant="h6" style={{ marginTop: '20px' }}>Available Cards:</Typography>
      <Grid container spacing={3}>
        {cards.map((card) => (
          <Grid item key={card.name} xs={12} sm={6} md={4} lg={3} onClick={() => addToDeck(card.name)}>
            <TcgCard card={card} />
          </Grid>
        ))}
      </Grid>
  </CardContent>
</Card>
      

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