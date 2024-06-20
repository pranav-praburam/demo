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

  return (
    <View style={styles.container}>
      <Text style={styles.timerText}>
        Timer: {years}y {days}d {hours}h {minutes}m {seconds}s
      </Text>
      <Text style={styles.text}>
        Hey there quitters! Growing up we've been told never to quit, but as we grow older, we realize that some things are worth letting go of in life. 
        This app is designed to help you quit your vices. Whether it's smoking, drinking, or any other bad habit, this app will help you keep track of how long you've been clean
        as well as motivate you to keep going. Remember, it's never too late to quit. You got this! ~ Pranav Praburam 
      </Text>
      <TouchableOpacity style={styles.button} onPress={resetTimer}>
        <Text style={styles.buttonText}>Reset Timer</Text>
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