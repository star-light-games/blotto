import { Typography } from '@mui/material';
import React, { useState, useEffect } from 'react';

function Timer({ lastRollTime, secondsPerTurn }) {
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  useEffect(() => {
    // When the component mounts or lastRollTime changes, reset the timer and start counting.
    setSecondsElapsed(0);
    
    const intervalId = setInterval(() => {
      const currentTime = Date.now(); // Current timestamp in milliseconds

      const difference = Math.floor((lastRollTime * 1000 - currentTime + secondsPerTurn * 1000) / 1000); // Difference in seconds
      setSecondsElapsed(difference);
    }, 1000); // Update every second

    // Cleanup: clear the interval when the component unmounts or when lastRollTime changes
    return () => clearInterval(intervalId);
  }, [lastRollTime]);

  function formatTime(seconds) {
    if (seconds < 0) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`; // padStart ensures there are always two digits for seconds
  }

  if (!secondsPerTurn) return null;

  return (
    <Typography variant="h5">
      {formatTime(secondsElapsed)}
    </Typography>
  );
}

export default Timer;
