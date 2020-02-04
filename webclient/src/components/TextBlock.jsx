import React from 'react';
import PropTypes from 'prop-types';
import './styles/TextBlock.css';


function makeQuery(id, callback, depth = 2) {
  const query = ` query{
        block(id:"${id}") {
          content {
            value,
            type
          },
          id,
          linkIn {
            children,
            references
          },
          linkOut {
            children,
            references
          }
        }
      }`;
  const url = 'http://127.0.0.1:5000/graphql';
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  }).then((res) => res.json())
    .then((response) => {
      if (depth === 0) {
        callback(response);
      } else {
        let contextLinks = [];
        if (response.data.block.linkIn) {
          Object.keys(response.data.block.linkIn).forEach((linkType) => {
            contextLinks = contextLinks.concat(response.data.block.linkIn[linkType])
          });
        }
        if (response.data.block.linkOut) {
          Object.keys(response.data.block.linkOut).forEach((linkType) => {
            contextLinks = contextLinks.concat(response.data.block.linkOut[linkType])
          });
        }
        console.log(contextLinks);

      }
    })
    .catch(console.error);
}


export default class TextBlock extends React.Component {
  constructor(props) {
    super();
    this.load(props);
    this.state = {
    };
  }

  // eslint-disable-next-line camelcase
  UNSAFE_componentWillReceiveProps(props) {
    this.load(props);
  }

  // eslint-disable-next-line class-methods-use-this
  load(props) {
    makeQuery(props.id, (response) => {
      const blockData = response.data.block;
      this.setState({
        id: blockData.id,
        content: blockData.content,
        linkIn: blockData.linkIn,
        linkOut: blockData.linkOut,
      });
    });
  }

  renderContent() {
    const { content } = this.state;
    if (content) {
      return content.map((token) => {
        if (token.type === 'REF') {
          return <a href={`?ref=${token.value}`}>{token.value}</a>;
        }
        return <span>{` ${token.value}`}</span>;
      });
    }
    return null;
  }

  renderChildren() {
    const { linkOut } = this.state;
    if (linkOut) {
      console.log(linkOut);
    }
  }


  render() {
    return (
      <div className="textblock">
        {this.renderContent()}
        {this.renderChildren()}
      </div>
    );
  }
}

TextBlock.defaultProps = {
  // reference: '0',
  // depth: 2,
};

TextBlock.propTypes = {
  // reference: PropTypes.string,
  // depth: PropTypes.number,
};
