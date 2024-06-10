// TabThree.js

import React, { useContext } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import TimerContext from 'C:/Users/15088/OneDrive/Desktop/COSI 153/demo/components/TimerContext.js';

function TabThree() {
  const { setStartTimer, setSeconds } = useContext(TimerContext);

  const resetTimer = () => {
    setStartTimer(false);
    setSeconds(0);
  };

  return (
    <View style={styles.container}>
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