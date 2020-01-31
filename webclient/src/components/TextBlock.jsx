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

  // eslint-disable-next-line camelcase
  UNSAFE_componentWillReceiveProps(props) {
    this.load(props);
  }

  // eslint-disable-next-line class-methods-use-this
  load(props) {
    fetch(`http://localhost:5000/b/${props.reference}`, {
      method: 'get',
    }).then((response) => response.json())
      .then((textblock) => {
        this.setState({ content: textblock.content });
        this.setState({ children: textblock.children });
        this.setState({ id: textblock.id });
      });

    fetch(`http://localhost:5000/o/${props.reference}`, {
      method: 'get',
    }).then((response) => response.json())
      .then((occurences) => {
        this.setState({ occurences });
      });
  }

  render() {
    const { content } = this.state;
    const { children } = this.state;
    const { occurences } = this.state;
    const { id } = this.state;
    const { depth } = this.props;
    let data = <span>Loading...</span>;
    let childrenElem = <span>Loading...</span>;
    let linksElem = <span>Loading...</span>;
    let permalink = <span>Loading...</span>;
    if (content !== undefined) {
      data = content.map((token) => {
        if (token.type === 'TXT') {
          return <span className="txt">{` ${token.value} `}</span>;
        }
        if (token.type === 'REF') {
          return <a href={`?ref=${token.data}`} className="ref">{`${token.value}`}</a>;
        }
        return null;
      });
    }
    if (depth <= 0) {
      childrenElem = null;
      linksElem = null;
    } else {
      if (children !== undefined) {
        childrenElem = children.map((child) => <li><TextBlock depth={0} reference={child.id} /></li>);
      }
      if (occurences !== undefined) {
        linksElem = occurences.map((block) => <li><TextBlock depth={0} reference={block.id} /></li>);
      }
    }
    if (id !== undefined) {
      permalink = <a className="blocklink" href={`?ref=${id}`}>{id}</a>;
    }
    return (
      <div className="textblock">
        {permalink}
        <div>{ data }</div>
        {children ? <ul className="children">{ childrenElem }</ul> : <span></span>}
        {linksElem && linksElem.length > 0
          ? (
            <div>
              <hr></hr>
              <span className="linksTitle">Links:</span>
              <ul className="links">{linksElem}</ul>
            </div>
          )
          : <span />}
      </div>
    );
  }
}

TextBlock.defaultProps = {
  reference: '0',
  depth: 2,
};

TextBlock.propTypes = {
  reference: PropTypes.string,
  depth: PropTypes.number,
};
