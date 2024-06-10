// App.js

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from 'C:/Users/15088/OneDrive/Desktop/COSI 153/demo/components/HomeScreen.js';
import { TimerProvider } from 'C:/Users/15088/OneDrive/Desktop/COSI 153/demo/components/TimerContext.js';

const Stack = createNativeStackNavigator();

function App() {
  const [startTimer, setStartTimer] = React.useState(false);
  const [seconds, setSeconds] = React.useState(0);

  return (
    <TimerProvider value={{ startTimer, setStartTimer, seconds, setSeconds }}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen name="NotMyVice" component={HomeScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </TimerProvider>
  );
}


export default App;