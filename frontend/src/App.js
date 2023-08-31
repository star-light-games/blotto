import logo from './logo.svg';
import './App.css';

import React, { useState, useEffect } from 'react';
import { Container, Grid, CircularProgress, Snackbar, Alert } from '@mui/material';
import TcgCard from './TcgCard';
import DeckBuilder from './DeckBuilder';
import { URL } from './settings';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GamePage from './GamePage';
import ThemeProvider from './ThemeProvider';
import { CssBaseline } from '@mui/material';
import { DarkModeContext, DarkModeProvider } from './DarkModeContext';
import oldPainting from './oldPainting.jpg';

import TopBar from './TopBar.js';




function CardPoolPage() {
  const [cards, setCards] = useState([]);
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
        setCards(Object.values(data));
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
      <DeckBuilder cards={cards}/>
    </Container>
    </div>
  );
}


function App() {
  return (
    <DarkModeProvider> 
      <ThemeProvider>

      <CssBaseline />

      <TopBar />
    <Router>
      <Routes>
        <Route exact path="/" element={<CardPoolPage />} />
        <Route path="/game/:gameId" element={<GamePage />} />
      </Routes>
    </Router>
    </ThemeProvider>
    </DarkModeProvider>
  );
}

export default App;
