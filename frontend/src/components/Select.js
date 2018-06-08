import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './Select.css';


/** Select component */
export default class Select extends Component {

  constructor(props) {
      super(props);
      this.handleChange = this.handleChange.bind(this);
  }

  /** call parent handler with id of selected option and select depth */
  handleChange(event) {
    this.props.onChange(event.target.value, this.props.depth);
  }

  render() {
    return (
      <div>
        <label className="Select-label">{this.props.label}
          <select className="Select" defaultValue="" onChange={this.handleChange}>
            <option value=""> -- Select an option -- </option>
            {this.props.options.map((option) =>
              <option key={option._id} value={option._id}>{option.name}</option>
            )}
          </select>
        </label>
      </div>
    )
  }

}

Select.propTypes = {
  /** seelct options */
  options: PropTypes.array.isRequired,
  /** change handler */
  onChange: PropTypes.func.isRequired,
  /** Depth of the select and nodes */
  depth: PropTypes.number.isRequired,
  /** Select label */
  label: PropTypes.string.isRequired
}
