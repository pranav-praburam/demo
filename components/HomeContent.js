import React, { useState, useEffect, useContext } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import TimerContext from './TimerContext.js';


const HomeContent=()=> {
    const { startTimer, setStartTimer, seconds, setSeconds, quitTimes, getQuitTimes } = useContext(TimerContext);
    const [vice, setVice] = useState('smoking');
  useEffect(() => {
    let interval = null;
    if (startTimer) {
      interval = setInterval(() => {
        setSeconds(seconds => (new Date().getTime() - quitTimes[vice])/1000);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [startTimer]);

  const secondsInMinute = 60;
  const secondsInHour = secondsInMinute * 60;
  const secondsInDay = secondsInHour * 24;
  const secondsInWeek = secondsInDay * 7;
  const secondsInYear = secondsInDay * 365;

  const years = Math.floor(seconds / secondsInYear);
  const weeks = Math.floor((seconds % secondsInYear) / secondsInWeek);
  const days = Math.floor((seconds % secondsInWeek) / secondsInDay);
  const hours = Math.floor((seconds % secondsInDay) / secondsInHour);
  const minutes = Math.floor((seconds % secondsInHour) / secondsInMinute);
  const remainingSeconds = seconds % secondsInMinute;

  return (
    <View style={{ flex: 1, justifyContent: 'center' }}>
      <View style={{ alignSelf: 'center' }}>
        <Text style={{ fontSize: 20 }}>Quit your vices now!!!</Text>
        <Text style={{ fontSize: 30 }}>Time since you've quit:</Text>
        <Text style={{ fontSize: 30 }}>{years} years, {weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {remainingSeconds} seconds</Text>
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
          onPress={() => setStartTimer(true)}
        >
          <Text style={{ color: 'white', fontSize: 18 }}>QUIT</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default HomeContent;