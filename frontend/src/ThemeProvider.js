// src/ThemeProvider.js
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import React, { useContext } from 'react';
import {DarkModeContext} from './DarkModeContext';



const ThemeProvider = ({ children }) => {
  const { isDarkMode } = useContext(DarkModeContext);

  const theme = createTheme({
    palette: {
      mode: isDarkMode ? 'light' : 'dark', // This line was changed
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          body: {
            backgroundColor: isDarkMode ? '#fff' : '#333',  // Colors swapped here
            color: isDarkMode ? '#333' : '#eee',             // And here
          },
        },
      },
    },
});

  return <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>;
};

export default ThemeProvider;
