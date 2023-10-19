import { Typography } from '@mui/material';
import React, { useState, useEffect } from 'react';

function Timer({ lastTimerStart, secondsPerTurn, secondsElapsed, setSecondsElapsed, doNotUpdateTimer }) {
  useEffect(() => {
    // When the component mounts or lastTimerStart changes, reset the timer and start counting.

    if (!lastTimerStart || doNotUpdateTimer) return;
    
    const intervalId = setInterval(() => {
      const currentTime = Date.now(); // Current timestamp in milliseconds

      const difference = Math.floor((lastTimerStart * 1000 - currentTime + secondsPerTurn * 1000) / 1000); // Difference in seconds
      setSecondsElapsed(difference);
    }, 1000); // Update every second

    // Cleanup: clear the interval when the component unmounts or when lastTimerStart changes
    return () => clearInterval(intervalId);
  }, [lastTimerStart]);

  function formatTime(seconds) {
    if (seconds < 0) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`; // padStart ensures there are always two digits for seconds
  }

  if (!secondsPerTurn || !lastTimerStart || secondsElapsed === null) return null;

  return (
    <Typography variant="h2">
      {formatTime(secondsElapsed)}
    </Typography>
  );
}

export default Timer;
