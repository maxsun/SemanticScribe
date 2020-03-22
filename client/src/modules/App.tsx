import React from 'react';
// import logo from '../static/logo.svg';
import '../styles/App.css';
import '../modules/DisplayPanel';
import DisplayPanel from '../modules/DisplayPanel';
import PlaintextPanel from './PlaintextPanel';
import JsonPanel from './JsonPanel';

function App() {
  return (
    <div className="App">
      <DisplayPanel
        source={'http://localhost:5000/read/mtc'}
      >
        { [JsonPanel, PlaintextPanel] }
      </DisplayPanel>
    </div>
  );
}

export default App;
