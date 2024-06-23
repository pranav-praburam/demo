import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

const TimerContext = createContext();

export const TimerProvider = ({ children }) => {
  const [startTimer, setStartTimer] = useState(false);
  const [startTimer2, setStartTimer2] = useState(false);

  // Load timers state from AsyncStorage when component mounts
  useEffect(() => {
    const loadTimers = async () => {
      const savedStartTimer = await AsyncStorage.getItem('startTimer');
      const savedStartTimer2 = await AsyncStorage.getItem('startTimer2');

      if (savedStartTimer !== null) {
        setStartTimer(JSON.parse(savedStartTimer));
      }
      if (savedStartTimer2 !== null) {
        setStartTimer2(JSON.parse(savedStartTimer2));
      }
    };

    loadTimers();
  }, []);

  // Save timers state to AsyncStorage whenever they change
  useEffect(() => {
    AsyncStorage.setItem('startTimer', JSON.stringify(startTimer));
    AsyncStorage.setItem('startTimer2', JSON.stringify(startTimer2));
  }, [startTimer, startTimer2]);

  return (
    <TimerContext.Provider value={{ startTimer, setStartTimer, startTimer2, setStartTimer2 }}>
      {children}
    </TimerContext.Provider>
  );
};

export const TimerConsumer = TimerContext.Consumer;

export default TimerContext;