// src/theme.js
import { createTheme } from '@mui/material';

export const darkTheme = createTheme({
  palette: {
    type: 'dark',
    primary: {
      main: '#90caf9',  // Customize as needed
    },
    secondary: {
      main: '#f48fb1',  // Customize as needed
    },
  },
});

export const lightTheme = createTheme({
  palette: {
    type: 'light',
    primary: {
      main: '#1976d2',  // Customize as needed
    },
    secondary: {
      main: '#d81b60',  // Customize as needed
    },
  },
});
