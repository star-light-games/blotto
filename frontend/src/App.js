import './App.css';

import { URL } from './settings';
import React, { useState, useEffect } from 'react';
import { Container, CircularProgress, Snackbar, Alert } from '@mui/material';
import DeckBuilder from './DeckBuilder';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GamePage from './GamePage';
import ThemeProvider from './ThemeProvider';
import { CssBaseline } from '@mui/material';
import { DarkModeProvider } from './DarkModeContext';
import { SocketProvider } from './SocketContext';
import oldPainting from './oldPainting.jpg';

import TopBar from './TopBar.js';


function CardPoolPage() {
  const [cards, setCards] = useState([]);
  const [laneRewards, setLaneRewards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toastOpen, setToastOpen] = useState(false);

  // console.log(cards);

  useEffect(() => {
    fetch(`${URL}/api/card_pool`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        // Custom order map for creature types
        const creatureTypeOrder = {
          "Avatar": 1,
          "Earth": 2,
          "Water": 3,
          "Air": 4,
          "Fire": 5
        };

        setCards(Object.values(data.cards).sort((a, b) => {
          const aOrder = creatureTypeOrder[a.creatureTypes?.[0]] || Infinity;
          const bOrder = creatureTypeOrder[b.creatureTypes?.[0]] || Infinity;

          if (aOrder < bOrder) {
              return -1;
          }
          if (aOrder > bOrder) {
              return 1;
          }

          const aCost = a.cost;
          const bCost = b.cost;

          if (aCost < bCost) {
              return -1;
          }
          if (aCost > bCost) {
              return 1;
          }

          // If creatureTypes order is the same, compare the names
          return a.name.localeCompare(b.name);
        }));
        setLaneRewards(data.laneRewards);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setToastOpen(true);
        setLoading(false);
      });
  }, []);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setToastOpen(false);
  };

  if (loading) {
    return (
      <Container>
        <CircularProgress />
      </Container>
    );
  }

  return (

    <div 
    style={{ 
      backgroundImage: `url(${oldPainting})`, 
      backgroundSize: 'cover', 
      backgroundPosition: 'left top', 
      backgroundRepeat: 'no-repeat', }}
      >
    <Container>
      <Snackbar 
        open={toastOpen} 
        autoHideDuration={6000} 
        onClose={handleClose} 
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleClose} severity="error" variant="filled">
          {error}
        </Alert>
      </Snackbar>
      {/* <Grid container spacing={3}>
        {cards.map((card) => (
          <Grid item key={card.name} xs={12} sm={6} md={4} lg={3}>
            <TcgCard card={card} />
          </Grid>
        ))}
      </Grid> */}
      <DeckBuilder cards={cards} laneRewards={laneRewards}/>
    </Container>
    </div>
  );
}


function App() {
  return (
    <SocketProvider>
    <DarkModeProvider> 
      <ThemeProvider>

      <CssBaseline />

    <Router>
      <TopBar />

      <Routes>
        <Route exact path="/" element={<CardPoolPage />} />
        <Route path="/game/:gameId" element={<GamePage />} />
      </Routes>
    </Router>
    </ThemeProvider>
    </DarkModeProvider>
    </SocketProvider>
  );
}

export default App;
