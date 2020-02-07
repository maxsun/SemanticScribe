import React from 'react';
import TextBlock from './TextBlock';
import './styles/App.css';

function makeQuery(id, callback) {
  const query = `
    query {
      block(id: "${id}") {
        id
        content {
          value,
          type,
          target
        },
        linkOut {
          children {
            id
            content {
              value,
              type,
              target
            }
          }
          references {
            id
            content {
              value,
              type,
              target
            }
          }
        },
        linkIn {
          references {
            id
            content {
              value
              type
              target
            }
          }
          children {
            id
            content {
              value
              type
              target
            }
          }
        }
      }
    }
`;
  const url = 'http://127.0.0.1:5000/graphql';
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  }).then((res) => res.json())
    .then(callback)
    .catch(console.error);
}


export default class App extends React.Component {
  constructor() {
    const url = new URL(window.location);
    const id = url.searchParams.get('id') || '~';
    super();
    makeQuery(id, (response) => {
      const blockData = response.data.block;
      this.setState({ blockData });
    });
    this.state = {
      blockData: null,
    };
  }

  render() {
    const { blockData } = this.state;
    return (
      <div id="App">
        <TextBlock data={blockData} />
      </div>
    );
  }
}
