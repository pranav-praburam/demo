// App.js

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from 'C:/Users/15088/OneDrive/Desktop/COSI 153/demo/components/HomeScreen.js';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="NotMyVice" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;