import React, { useState, useCallback, useEffect, createContext } from 'react';

export const DarkModeContext = createContext({
  isDarkMode: false,
  toggleDarkMode: () => {}
});

export const DarkModeProvider = ({ children }) => {
  // Initialize state with value from localStorage or default to false
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const storedValue = localStorage.getItem('isDarkMode');
    return storedValue === 'true';
  });

  // Function to toggle dark mode
  const toggleDarkMode = useCallback(() => {
    setIsDarkMode(prevMode => !prevMode);
  }, []);

  // Effect to update localStorage whenever isDarkMode changes
  useEffect(() => {
    localStorage.setItem('isDarkMode', isDarkMode);
  }, [isDarkMode]);

  return (
    <DarkModeContext.Provider value={{ isDarkMode, toggleDarkMode }}>
      {children}
    </DarkModeContext.Provider>
  );
};
