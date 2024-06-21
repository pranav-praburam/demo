// TimerContext.js

import React, { createContext, useState } from 'react';

const TimerContext = createContext();

export const TimerProvider = ({ children }) => {
  const [startTimer, setStartTimer] = useState(false);
  const [startTimer2, setStartTimer2] = useState(false);

  return (
    <TimerContext.Provider value={{ startTimer, setStartTimer, startTimer2, setStartTimer2 }}>
      {children}
    </TimerContext.Provider>
  );
};

export const TimerConsumer = TimerContext.Consumer;

export default TimerContext;