import React from 'react';
import PropTypes from 'prop-types';
import './styles/TextBlock.css';

export default class TextBlock extends React.Component {
  constructor(props) {
    super();
    if (props.data) {
      this.state = {
        content: props.data.content,
        id: props.data.id,
        linkIn: props.data.linkIn,
        linkOut: props.data.linkOut,
      };
    }
    this.load(props);
  }

  // eslint-disable-next-line camelcase
  UNSAFE_componentWillReceiveProps(props) {
    this.load(props);
  }

  load(props) {
    if (props.data) {
      this.setState({
        content: props.data.content,
        id: props.data.id,
        linkIn: props.data.linkIn,
        linkOut: props.data.linkOut || null,
      });
    }
  }

  renderContent() {
    if (this.state && this.state.content) {
      const { content } = this.state;
      return content.map((token) => {
        if (token.type === 'REF') {
          return <a className="ref" href={`?id=${token.target}`}>{` ${token.value}`}</a>;
        }
        return <span>{` ${token.value}`}</span>;
      });
    }
    return null;
  }

  renderLinkOut() {
    const results = [];
    if (this.state && this.state.linkOut) {
      const { linkOut } = this.state;
      return (
        <div>
          {Object.keys(linkOut).map((linktype) => (
            <div>
              {linkOut[linktype].length > 0 ? (
                <div>
                  <hr />
                  <h3>{`${linktype} (out):`}</h3>
                </div>
              ) : null}
              <ul>
                {linkOut[linktype].map((link) => <li><TextBlock data={link} /></li>)}
              </ul>
            </div>
          ))}
        </div>
      );
    }
    return results;
  }

  renderLinkIn() {
    const results = [];
    if (this.state && this.state.linkIn) {
      const { linkIn } = this.state;
      return Object.keys(linkIn).map((linktype) => (
        <div>
          {linkIn[linktype].length > 0 ? (
            <div>
              <hr />
              <h3>{`${linktype} (in):`}</h3>
            </div>
          ) : null}
          <ul>
            {linkIn[linktype].map((link) => <li><TextBlock data={link} /></li>)}
          </ul>
        </div>
      ));
    }
    return results;
  }

  renderId() {
    if (this.state && this.state.id) {
      const { id } = this.state;
      return <a className="textblockLink" href={`?id=${id}`}>></a>;
    }
    return null;
  }

  render() {
    return (
      <div className="textblock">
        {this.renderId()}
        <div className="content">{this.renderContent()}</div>
        <div className="linkOut">
          {this.renderLinkOut()}
        </div>
        <div className="linkIn">
          {this.renderLinkIn()}
        </div>
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
