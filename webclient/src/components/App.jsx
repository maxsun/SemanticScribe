import React from 'react';
import TextBlock from './TextBlock';
import './styles/App.css';

export default class App extends React.Component {
  constructor() {
    super();
    this.state = {

    };
  }

  render() {
    const url = new URL(window.location);
    const ref = url.searchParams.get('ref') || '~';
    return (
      <div id="App">
        <TextBlock reference={ref} />
      </div>
    );
  }
}
