import React from 'react';
import PropTypes from 'prop-types';
import './styles/TextBlock.css';

export default class TextBlock extends React.Component {
  constructor(props) {
    super();
    this.load(props);
    this.state = {
    };
  }

  UNSAFE_componentWillReceiveProps(props) {
    this.load(props);
  }

  load(props) {
    fetch(`http://localhost:5000/r/${props.reference.replace(/\//g, '.')}`, {
      method: 'get',
    }).then((response) => response.json())
      .then((textblock) => {
        this.setState({ content: textblock.content });
        this.setState({ children: textblock.children });
        this.setState({ path: textblock.path });
      });
    fetch(`http://localhost:5000/o/${props.reference.replace(/\//g, '.')}`, {
      method: 'get',
    }).then((response) => response.json())
      .then((textblocks) => {
        this.setState({ occurences: textblocks });
      });
  }

  render() {
    const { content } = this.state;
    const { children } = this.state;
    const { occurences } = this.state;
    const contentItems = [];
    const childBlocks = [];
    const occurenceBlocks = [];

    if (children !== undefined) {
      children.forEach((child) => {
        const path = `${child.path}`;
        if (this.state.path !== undefined && path !== this.props.reference && path.startsWith(this.props.reference)) {
          childBlocks.push(<TextBlock reference={path} />);
        } else {
          // pass
        }
      });
    }

    if (occurences !== undefined) {
        occurences.forEach((block) => {
            console.log(block.path)
          occurenceBlocks.push(<TextBlock key={block.path} reference={block.path} />);
        });
    }

    if (content !== undefined) {
      content.forEach((token) => {
        if (token.type === 'REF') {
          contentItems.push(
            <span className="ref" key={token.value}>
              <a href={`?ref=${token.value}`}>{`${token.value} `}</a>
            </span>,
          );
        } else if (token.type === 'TXT') {
          contentItems.push(<span className="txt" key={token.value}>{`${token.value} `}</span>);
        }
      });
    }
    return (
        <div>
            <ul className="block">
                <li>{contentItems}</li>
                <div className="children">{childBlocks}</div>
            </ul>
            <div>
                {occurenceBlocks}
            </div>
        </div>

    );
  }
}

TextBlock.defaultProps = {
  reference: '/~',
};

TextBlock.propTypes = {
  reference: PropTypes.string,
};
