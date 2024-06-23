import React, { useState, useEffect, useContext } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import TimerContext from './TimerContext.js';
import { saveTimerState, loadTimerState } from './AsyncStorageHandler'; // Import AsyncStorage functions

const HomeContent = () => {
  const { startTimer, setStartTimer, startTimer2, setStartTimer2 } = useContext(TimerContext);

  // Timer states initialization
  const [seconds, setSeconds] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [hours, setHours] = useState(0);
  const [days, setDays] = useState(0);
  const [years, setYears] = useState(0);
  const [seconds2, setSeconds2] = useState(0);
  const [minutes2, setMinutes2] = useState(0);
  const [hours2, setHours2] = useState(0);
  const [days2, setDays2] = useState(0);
  const [years2, setYears2] = useState(0);

  // Load timer states from AsyncStorage on component mount
  useEffect(() => {
    const loadState = async () => {
      const timer1State = await loadTimerState('timer1');
      if (timer1State) {
        setSeconds(timer1State.seconds);
        setMinutes(timer1State.minutes);
        setHours(timer1State.hours);
        setDays(timer1State.days);
        setYears(timer1State.years);
      }
      const timer2State = await loadTimerState('timer2');
      if (timer2State) {
        setSeconds2(timer2State.seconds);
        setMinutes2(timer2State.minutes);
        setHours2(timer2State.hours);
        setDays2(timer2State.days);
        setYears2(timer2State.years);
      }
    };
    loadState();
  }, []);

  // Timer 1 logic
  useEffect(() => {
    let interval = null;
    if (startTimer) {
      interval = setInterval(() => {
        setSeconds(prevSeconds => {
          if (prevSeconds === 59) {
            setMinutes(prevMinutes => {
              if (prevMinutes === 59) {
                setHours(prevHours => {
                  if (prevHours === 23) {
                    setDays(prevDays => {
                      if (prevDays === 365) {
                        setYears(prevYears => prevYears + 1);
                        return 0;
                      }
                      return prevDays + 1;
                    });
                    return 0;
                  }
                  return prevHours + 1;
                });
                return 0;
              }
              return prevMinutes + 1;
            });
            return 0;
          }
          return prevSeconds + 1;
        });
      }, 1000);
    } else {
      setSeconds(0);
      setMinutes(0);
      setHours(0);
      setDays(0);
      setYears(0);
    }
    return () => {
      clearInterval(interval);
      saveTimerState('timer1', { seconds, minutes, hours, days, years });
    };
  }, [startTimer, seconds, minutes, hours, days, years]);

  // Timer 2 logic (mirrors Timer 1 with adjustments for Timer 2's state variables)
  useEffect(() => {
    let interval2 = null;
    if (startTimer2) {
      interval2 = setInterval(() => {
        setSeconds2(prevSeconds2 => {
          if (prevSeconds2 === 59) {
            setMinutes2(prevMinutes2 => {
              if (prevMinutes2 === 59) {
                setHours2(prevHours2 => {
                  if (prevHours2 === 23) {
                    setDays2(prevDays2 => {
                      if (prevDays2 === 365) {
                        setYears2(prevYears2 => prevYears2 + 1);
                        return 0;
                      }
                      return prevDays2 + 1;
                    });
                    return 0;
                  }
                  return prevHours2 + 1;
                });
                return 0;
              }
              return prevMinutes2 + 1;
            });
            return 0;
          }
          return prevSeconds2 + 1;
        });
      }, 1000);
    } else {
      setSeconds2(0);
      setMinutes2(0);
      setHours2(0);
      setDays2(0);
      setYears2(0);
    }
    return () => {
      clearInterval(interval2);
      saveTimerState('timer2', { seconds2, minutes2, hours2, days2, years2 });
    };
  }, [startTimer2, seconds2, minutes2, hours2, days2, years2]);

  // UI for both timers and their control buttons
  return (
    <View style={{ flex: 1, justifyContent: 'center' }}>
      {/* First Timer Display and Control Button */}
      <View style={{ alignSelf: 'center' }}>
        <Text style={{ fontSize: 20 }}>Quit Smoking Cigarettes!</Text>
        <Text style={{ fontSize: 30 }}>
          Timer: {years} years {days} days {hours} hours {minutes} minutes {seconds} seconds
        </Text>
        <TouchableOpacity
          style={{
            backgroundColor: 'red',
            padding: 10,
            borderRadius: 5,
            width: 200,
            alignItems: 'center'
          }}
          onPress={() => setStartTimer(!startTimer)}
        >
          <Text style={{ color: 'white', fontSize: 18 }}>{startTimer ? 'STOP' : 'START'}</Text>
        </TouchableOpacity>
      </View>
      {/* Second Timer Display and Control Button */}
      <View style={{ alignSelf: 'center', marginTop: 20 }}>
        <Text style={{ fontSize: 20 }}>Quit Vaping!</Text>
        <Text style={{ fontSize: 30 }}>
          Timer: {years2} years {days2} days {hours2} hours {minutes2} minutes {seconds2} seconds
        </Text>
        <TouchableOpacity
          style={{
            backgroundColor: 'blue',
            padding: 10,
            borderRadius: 5,
            width: 200,
            alignItems: 'center'
          }}
          onPress={() => setStartTimer2(!startTimer2)}
        >
          <Text style={{ color: 'white', fontSize: 18 }}>{startTimer2 ? 'STOP' : 'START'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default HomeContent;