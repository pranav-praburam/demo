// HomeScreen.js

import React from 'react';
import { View, Text, Button } from 'react-native';

function HomeScreen({ navigation }) {
return (
    <View style={{ flex: 1, justifyContent: 'center' }}>
        <View style={{ alignSelf: 'center' }}>
            <Text style={{ fontSize: 20 }}>Quit your vices now</Text>
        </View>
        <View style={{ alignSelf: 'center' }}>
            <Button
                title="QUIT"
                onPress={() => navigation.navigate('Details')}
            />
        </View>
    </View>
);
}

export default HomeScreen;