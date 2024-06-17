import React, { useState } from 'react';

function HeronCalculator() {
  const [sides, setSides] = useState('');
  const [area, setArea] = useState(null);

  const calculateArea = () => {
    const sidesArray = sides.split(' ').map(Number);
    if (sidesArray.length !== 3 || sidesArray.some(side => isNaN(side) || side <= 0)) {
      alert('Please enter valid side lengths separated by spaces.');
      return;
    }
  
    const [a, b, c] = sidesArray;
    if (a + b <= c || a + c <= b || b + c <= a) {
      alert('The provided sides do not form a valid triangle.');
      return;
    }
  
    const s = (a + b + c) / 2;
    const areaCalculation = Math.sqrt(s * (s - a) * (s - b) * (s - c));
    setArea(areaCalculation);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', width: '100vw', position: 'absolute', top: 0, left: 0, flexDirection: 'column', fontSize: '24px' }}>
      <h1>Calculate area of triangle by Heron's rule</h1>
      <input
        type="text"
        value={sides}
        onChange={(e) => setSides(e.target.value)}
        placeholder="Enter sides A, B, C"
        style={{ backgroundColor: 'yellow', fontSize: '20px', padding: '10px', margin: '10px', width: '300px' }}
      />
      <button onClick={calculateArea} style={{ color: 'white', fontSize: '20px', padding: '10px 20px', margin: '10px', backgroundColor: 'blue' }}>Calculate Area</button>
      {area !== null && <p style={{ fontSize: '20px' }}>Area: {area.toFixed(2)}</p>}
    </div>
  );
}

export default HeronCalculator;