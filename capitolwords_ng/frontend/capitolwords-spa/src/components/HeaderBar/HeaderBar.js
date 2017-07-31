import React, { Component } from 'react';
import PropTypes from 'prop-types';

import './HeaderBar.css';

import SearchInput from '../SearchInput/SearchInput';

class HeaderBar extends Component {
  static propTypes = {
    onSearchSubmit: PropTypes.func.isRequired,
  };

  render() {
    return (
      <div>
        <div className="HeaderBar-container">
          <div>
            <h1 className="HeaderBar-title">Capitol Words</h1>
          </div>
          <div className="headerBarSearch">
            <SearchInput onSubmit={this.props.onSearchSubmit}/>
          </div>
        </div>

        <div className="SearchResults">
          <div className="ResultsHeader">
            <span className="TextSmall">Search results for:</span>
            <h1>Education</h1>
          </div>
          <div className="DateToggle">
            <ul>
              <li className="TabActive">30 days</li>
              <li>3 months</li>
              <li>6 months</li>
            </ul>
          </div>
          <div className="TopMetricsList">
            <div className="MetricListItem">
              <h2>261</h2>
              <span>Total Mentions</span>
            </div>
            <div className="MetricListItem">
              <h2>+2%</h2>
              <span>Compared to previous 30 days</span>
            </div>
          </div>

          <div className="TopRecords">
            <h3>Records with the most mentions</h3>
            <div className="Record">
              <div className="Date">
                May 24, 2017
              </div>
              <h4 className="RecordTitle">Education Funding in the President’s Budget</h4>
              <span className="MentionCount">3 mentions</span>
              <blockquote>“This is why I was shocked the President's budget makes drastic cuts to <span className="Highlight">education</span>—cuts that will have the biggest impact on kids who need our help the most.”</blockquote>
              <div class="SentorAvatar"></div>
            </div>

          </div> 
        </div>
      </div>
    );
  }
}

export default HeaderBar;
