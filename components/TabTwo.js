// TabTwo.js

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Modal, StyleSheet, Button } from 'react-native';

function TabTwo() {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalText, setModalText] = useState('');
  const [popupText, setPopupText] = useState('');

  const handleBoxPress = (text, popupText) => {
    setPopupText(popupText);
    setModalVisible(true);
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.box} onPress={() => handleBoxPress('1 minute of Sobriety', 'one')}>
        <Text style={styles.boxText}>1 minute of Sobriety</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.box} onPress={() => handleBoxPress('1 week of Sobriety', 'two')}>
        <Text style={styles.boxText}>1 week of Sobriety</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.box} onPress={() => handleBoxPress('1 month of Sobriety', 'three')}>
        <Text style={styles.boxText}>1 month of Sobriety</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.box} onPress={() => handleBoxPress('1 year of Sobriety', 'four')}>
        <Text style={styles.boxText}>1 year of Sobriety</Text>
      </TouchableOpacity>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <Text style={styles.modalText}>{modalText}</Text>
            <Button title="Close" onPress={() => setModalVisible(false)} />
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20
  },
  box: {
    width: '100%',
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 10,
    backgroundColor: '#841584'
  },
  boxText: {
    color: '#fff',
    fontSize: 20
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
    width: '80%', // adjust this value to change the width
    height: '60%', // adjust this value to change the height
  },
  modalText: {
    marginBottom: 15,
    textAlign: 'center'
  }
});

export default TabTwo;