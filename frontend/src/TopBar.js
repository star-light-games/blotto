import React from 'react';
import { AppBar, Toolbar, Typography, SvgIcon, Box } from '@mui/material';
import logo from './tempLogo.svg';  // Make sure to update the path to your SVG logo
import { useContext } from 'react';
import {DarkModeContext} from './DarkModeContext';
import Switch from '@mui/material/Switch';
import { Link } from 'react-router-dom';

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
          <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
            <img src={logo} alt="BlottoBattler Logo" style={{ height: '50px', marginRight: '10px' }} />
          </Link>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            BlottoBattler
          </Typography>
          <Box display="flex" alignItems="center">
            <DarkModeToggle />
          </Box>
        </Toolbar>
      </AppBar>
    );
}

export default TopBar;
