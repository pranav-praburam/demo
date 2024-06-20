import React, { useState, useEffect, useContext } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import TimerContext from './TimerContext.js';

const HomeContent = () => {
  const { startTimer, setStartTimer } = useContext(TimerContext);
  const [seconds, setSeconds] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [hours, setHours] = useState(0);
  const [days, setDays] = useState(0);
  const [years, setYears] = useState(0);

  useEffect(() => {
    let interval = null;
    if (startTimer) {
      interval = setInterval(() => {
        setSeconds(seconds => {
          if (seconds === 59) {
            setMinutes(minutes => {
              if (minutes === 59) {
                setHours(hours => {
                  if (hours === 23) {
                    setDays(days => {
                      if (days === 365) {
                        setYears(years => years + 1);
                        return 0;
                      }
                      return days + 1;
                    });
                    return 0;
                  }
                  return hours + 1;
                });
                return 0;
              }
              return minutes + 1;
            });
            return 0;
          }
          return seconds + 1;
        });
      }, 1000);
    } else {
      // Reset timer when stopped
      setSeconds(0);
      setMinutes(0);
      setHours(0);
      setDays(0);
      setYears(0);
    }
    return () => clearInterval(interval);
  }, [startTimer]);

  return (
    <View style={{ flex: 1, justifyContent: 'center' }}>
      <View style={{ alignSelf: 'center' }}>
        <Text style={{ fontSize: 20 }}>Quit your vices now!!!</Text>
        <Text style={{ fontSize: 30 }}>
          Timer: {years} years {days} days {hours} hours {minutes} minutes {seconds} seconds
        </Text>
      </View>
      <View style={{ alignSelf: 'center' }}>
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
    </View>
  );
}

export default HomeContent;