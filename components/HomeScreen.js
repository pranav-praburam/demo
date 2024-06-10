// HomeScreen.js

import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import TabOne from './TabOne';
import TabTwo from './TabTwo';
import TabThree from './TabThree';

const Tab = createBottomTabNavigator();

function HomeContent() {
  const [startTimer, setStartTimer] = useState(false);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    let interval = null;
    if (startTimer) {
      interval = setInterval(() => {
        setSeconds(seconds => seconds + 1);
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
        <Text style={{ fontSize: 20 }}>Quit your vices now</Text>
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

function HomeScreen() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeContent} />
      <Tab.Screen name="My Vices" component={TabOne} />
      <Tab.Screen name="Milestones" component={TabTwo} />
      <Tab.Screen name="About Us" component={TabThree} />
    </Tab.Navigator>
  );
}

export default HomeScreen;