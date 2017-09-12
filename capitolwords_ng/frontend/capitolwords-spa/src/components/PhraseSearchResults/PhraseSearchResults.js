import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import './PhraseSearchResults.css';

import {
  isSearching,
  isSearchFailure,
  isSearchSuccess,
  searchResultCount,
  searchContent,
  searchResultList,
} from '../../selectors/phrase-search-selectors';

class PhraseSearchResults extends Component {
  static propTypes = {
    isSearching: PropTypes.bool.isRequired,
    isSearchFailure: PropTypes.bool.isRequired,
    isSearchSuccess: PropTypes.bool.isRequired,
    searchResultCount: PropTypes.number,
    searchResultList: PropTypes.array,
    searchContent: PropTypes.string
  };

  renderResultItem(item) {
    return (
      <li className="PhraseSearchResults-item" key={item._id}>
        <div className="PhraseSearchResults-item-id">{ item._source.ID }</div>
        <a href={ item._source.html_url } className="PhraseSearchResults-item-title">{ item._source.title }</a>
      </li>
    );
  }

  renderResultList() {
    const { searchResultList } = this.props;

    return (
      <ul className="PhraseSearchResults-list">
        { searchResultList.map(this.renderResultItem) }
      </ul>
    );
  }

  renderContents() {
    const {
      isSearching,
      isSearchFailure,
      isSearchSuccess,
      searchResultCount,
      searchContent
    } = this.props;

    if (isSearching) {
      return (<div>Searching...</div>);
    }

    if (isSearchFailure) {
      return (<div>Search failed. Please try again.</div>);
    }

    if (isSearchSuccess) {
      return (
        <div>
          <div className="PhraseSearchResults-results-for">Search results for:</div>
          <div className="PhraseSearchResults-phrase"> {searchContent} </div>
          <div className="PhraseSearchResults-date-selector">
            30 days | 3 months | 6 months
          </div>
          <div className="PhraseSearchResults-metrics-container">
            <div className="PhraseSearchResults-results-count-metric">
              <div className="PhraseSearchResults-metric-value">
                { searchResultCount }
              </div>
              <div className="PhraseSearchResults-metric-name">
                Total Mentions
              </div>
            </div>
            <div className="PhraseSearchResults-results-benchmark">
              <div className="PhraseSearchResults-metric-value">
                +10%
              </div>
              <div className="PhraseSearchResults-metric-name">
                Compared to previous 30 days
              </div>
            </div>
          </div>
          {this.renderResultList() }
        </div>
      )
    }

    return (<div />);
  }

  render() {
    return (
      <div className="PhraseSearchResults-container">
        { this.renderContents() }
      </div>
    );
  }

}


export default connect(state => ({
  isSearching: isSearching(state),
  isSearchFailure: isSearchFailure(state),
  isSearchSuccess: isSearchSuccess(state),
  searchContent: searchContent(state),
  searchResultCount: searchResultCount(state),
  searchResultList: searchResultList(state),
}))(PhraseSearchResults);
