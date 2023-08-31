import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import React, { useContext } from 'react';
import { DarkModeContext } from './DarkModeContext';

const ThemeProvider = ({ children }) => {
  const { isDarkMode } = useContext(DarkModeContext);

  const theme = createTheme({
    palette: {
      mode: isDarkMode ? 'dark' : 'light' ,
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          body: {
            backgroundColor: isDarkMode ? '#333' : '#fff',
            color: isDarkMode ? '#eee' : '#333',
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            backgroundColor: isDarkMode ? 'rgba(51, 51, 51, 0.9)' : 'rgba(255, 255, 255, 0.85)', 
          },
        },
      },
    },
  });

  return <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>;
};

export default ThemeProvider;
