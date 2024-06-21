import React, { useState, useEffect, useContext } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import TimerContext from './TimerContext.js';

const HomeContent = () => {
  const { startTimer, setStartTimer, startTimer2, setStartTimer2 } = useContext(TimerContext);
  // First timer state
  const [seconds, setSeconds] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [hours, setHours] = useState(0);
  const [days, setDays] = useState(0);
  const [years, setYears] = useState(0);
  // Second timer state
  const [seconds2, setSeconds2] = useState(0);
  const [minutes2, setMinutes2] = useState(0);
  const [hours2, setHours2] = useState(0);
  const [days2, setDays2] = useState(0);
  const [years2, setYears2] = useState(0);

  // First timer logic
  useEffect(() => {
    let interval = null;
    if (startTimer) {
      interval = setInterval(() => {
        setSeconds(seconds => seconds === 59 ? 0 : seconds + 1);
        if (seconds === 59) {
          setMinutes(minutes => minutes === 59 ? 0 : minutes + 1);
          if (minutes === 59) {
            setHours(hours => hours === 23 ? 0 : hours + 1);
            if (hours === 23) {
              setDays(days => days === 365 ? 0 : days + 1);
              if (days === 365) {
                setYears(years => years + 1);
              }
            }
          }
        }
      }, 1000);
    } else {
      setSeconds(0);
      setMinutes(0);
      setHours(0);
      setDays(0);
      setYears(0);
    }
    return () => clearInterval(interval);
  }, [startTimer, seconds, minutes, hours, days]);

  // Second timer logic (mirrors the first timer)
  useEffect(() => {
    let interval2 = null;
    if (startTimer2) {
      interval2 = setInterval(() => {
        setSeconds2(seconds2 => seconds2 === 59 ? 0 : seconds2 + 1);
        if (seconds2 === 59) {
          setMinutes2(minutes2 => minutes2 === 59 ? 0 : minutes2 + 1);
          if (minutes2 === 59) {
            setHours2(hours2 => hours2 === 23 ? 0 : hours2 + 1);
            if (hours2 === 23) {
              setDays2(days2 => days2 === 365 ? 0 : days2 + 1);
              if (days2 === 365) {
                setYears2(years2 => years2 + 1);
              }
            }
          }
        }
      }, 1000);
    } else {
      setSeconds2(0);
      setMinutes2(0);
      setHours2(0);
      setDays2(0);
      setYears2(0);
    }
    return () => clearInterval(interval2);
  }, [startTimer2, seconds2, minutes2, hours2, days2]);

  // UI for both timers and their control buttons
  return (
    <View style={{ flex: 1, justifyContent: 'center' }}>
      {/* First Timer Display and Control Button */}
      <View style={{ alignSelf: 'center' }}>
        <Text style={{ fontSize: 20 }}>First Timer</Text>
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
        <Text style={{ fontSize: 20 }}>Second Timer</Text>
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