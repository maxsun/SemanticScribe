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
    const id = url.searchParams.get('id') || '~';
    return (
      <div id="App">
        <TextBlock id={id} />
      </div>
    );
  }
}
