import React from 'react';
import TextBlock from './TextBlock';

// import { ReactComponent as Contrast } from '../assets/contrast.svg';
// import { ReactComponent as Logo } from '../assets/favicon.svg';

export default class App extends React.Component {
  constructor() {
    super();
    this.state = {

    };
  }

  render() {
    const url = new URL(window.location);
    const ref = url.searchParams.get('ref') || '/~';
    return (
      <div>
        <TextBlock reference={ref} />
      </div>
    );
  }
}
