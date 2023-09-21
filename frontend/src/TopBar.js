import React from 'react';
import { AppBar, Toolbar, Typography, SvgIcon, Box } from '@mui/material';
import logo from './tempLogo.svg';  // Make sure to update the path to your SVG logo
import { useContext } from 'react';
import {DarkModeContext} from './DarkModeContext';
import Switch from '@mui/material/Switch';
import { Link } from 'react-router-dom';
import { Grid } from '@mui/material';

function DarkModeToggle() {
    const { isDarkMode, toggleDarkMode } = useContext(DarkModeContext);
  
    return (
      <div>
        <span>{isDarkMode ? "Dark Mode" : "Light Mode" }</span>
        <Switch checked={isDarkMode} onChange={toggleDarkMode} />
      </div>
    );
  }
  

  const TopBar = () => {
    return (
      <AppBar position="static" style={{ backgroundColor: 'black' }}>
        <Toolbar>
          <Grid container alignItems="center" justify="space-between">
            
            {/* Left: Logo */}
            <Grid item xs={4} container alignItems="center">
              <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
                <img src={logo} alt="BlottoBattler Logo" style={{ height: '50px', marginRight: '10px' }} />
              </Link>
            </Grid>
            
            {/* Center: How to play */}
            <Grid item xs={4} container justifyContent="center">
              <Link external to="https://docs.google.com/document/d/12pSa81NvMgi8WRoDZQO4FrHMudNGaGx1aVrUjOtKp6w/edit?usp=sharing">
                <Typography variant='h5'>How to play</Typography>
              </Link>
            </Grid>
            
            {/* Right: Title and DarkModeToggle */}
            <Grid item xs={4} container justifyContent="flex-end" alignItems="center">
              <Typography variant="h6">
                BlottoBattler
              </Typography>
              <Box display="flex" alignItems="center" ml={2}>
                <DarkModeToggle />
              </Box>
            </Grid>

          </Grid>
        </Toolbar>
      </AppBar>
    );
}
export default TopBar;
