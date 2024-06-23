import React, { useState, useEffect, useContext } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import TimerContext from './TimerContext.js';

function TabThree() {
  const { startTimer, setStartTimer } = useContext(TimerContext);
  const [seconds, setSeconds] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [hours, setHours] = useState(0);
  const [days, setDays] = useState(0);
  const [years, setYears] = useState(0);

  // Second timer state
  const { startTimer2, setStartTimer2 } = useContext(TimerContext);
  const [seconds2, setSeconds2] = useState(0);
  const [minutes2, setMinutes2] = useState(0);
  const [hours2, setHours2] = useState(0);
  const [days2, setDays2] = useState(0);
  const [years2, setYears2] = useState(0);

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

  const resetTimer = () => {
    setStartTimer(false);
    setSeconds(0);
    setMinutes(0);
    setHours(0);
    setDays(0);
    setYears(0);
  };

  useEffect(() => {
    let interval2 = null;
    if (startTimer2) {
      interval2 = setInterval(() => {
        setSeconds2(seconds2 => {
          if (seconds2 === 59) {
            setMinutes2(minutes2 => {
              if (minutes2 === 59) {
                setHours2(hours2 => {
                  if (hours2 === 23) {
                    setDays2(days2 => {
                      if (days2 === 365) {
                        setYears(years2 => years2 + 1);
                        return 0;
                      }
                      return days2 + 1;
                    });
                    return 0;
                  }
                  return hours2 + 1;
                });
                return 0;
              }
              return minutes2 + 1;
            });
            return 0;
          }
          return seconds2 + 1;
        });
      }, 1000);
    } else {
      // Reset timer when stopped
      setSeconds2(0);
      setMinutes2(0);
      setHours2(0);
      setDays2(0);
      setYears2(0);
    }
    return () => clearInterval(interval2);
  }, [startTimer2]);

  const resetTimer2 = () => {
    setStartTimer2(false);
    setSeconds2(0);
    setMinutes2(0);
    setHours2(0);
    setDays2(0);
    setYears2(0);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.timerText}>
        Quit Smoking Cigarettes! {years}y {days}d {hours}h {minutes}m {seconds}s
      </Text>
      <Text style={styles.timerText}>
        Quit Vaping! {years2}y {days2}d {hours2}h {minutes2}m {seconds2}s
      </Text>
      <Text style={styles.text}>
        Hey there quitters! Growing up we've been told never to quit, but as we grow older, we realize that some things are worth letting go of in life. 
        This app is designed to help you quit your vices. Whether it's smoking, drinking, or any other bad habit, this app will help you keep track of how long you've been clean
        as well as motivate you to keep going. Remember, it's never too late to quit. You got this! ~ Pranav Praburam 
      </Text>
      <TouchableOpacity style={styles.button} onPress={resetTimer}>
        <Text style={styles.buttonText}>Reset Timer</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button} onPress={resetTimer2}>
        <Text style={styles.buttonText}>Reset Timer 2</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 20,
    paddingHorizontal: 20
  },
  text: {
    fontSize: 20
  },
  timerText: {
    fontSize: 14, // Smaller font size for the timer
    marginBottom: 20 // Add some space between the timer and the text
  },
  button: {
    marginTop: 20,
    backgroundColor: '#841584',
    padding: 10,
    borderRadius: 5
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center'
  }
});

export default TabThree;