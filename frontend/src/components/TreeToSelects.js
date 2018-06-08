import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import Select from './Select';
import './TreeToSelects.css';

/**
  Converts tree structure with parent references into series of select inputs.
  Shows the description of selected leaf node on the top.
  Allows to set labels based on depth.
  Works with remote API to get the data.
  example data structure:
  {_id: 1, name: 'Root Node', parentId: null}
  {_id: 2, name: 'First Level', parentId: 1}
  {_id: 3, name: 'Leaf', parentId: 2, description: 'Desc'}
*/
export default class TreeToSelects extends Component {

  /** Used to make sure that we are not trying to set state
  *   to the unmounted Component in async task */
  _isMounted = false;

  constructor(props) {
      super(props);
      this.state = {
          /** data for selects [[first select nodes],[second select nodes], etc.]
          * Index in this array ia also a depth of nodes
          */
          data: [],
          result: null,
          error: null
      };
      this.handleSelectChange = this.handleSelectChange.bind(this);
  }

  /** Get root nodes and create first select */
  componentDidMount() {
    this._isMounted = true;
    axios.get(this.props.rootNodesUrl)
      .then(res => {
        this._isMounted && this.setState(() => ({
          data: [res.data]
        }));
      })
      .catch(error => {
        this._isMounted && this.setState(() => ({
          'error': `Error: ${error.message}`
        }));
      });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  /** Handle any select change */
  handleSelectChange(id, depth) {
    if (!id){
      /** empty value has been selected
      * remove all selects after current
      */
      this.setState(() => ({
        data: this.state.data.slice(0, depth+1),
        result: null
      }));
    }
    else{
      // try to get child nodes
      axios.get(`${this.props.childNodesUrl}${id}`)
        .then(res => {
          if (Array.isArray(res.data) && !res.data.length) {
            /** node is a leaf
            * get node data and set result
            */
            axios.get(`${this.props.nodeDataUrl}${id}`)
              .then(res => {
                if ('description' in res.data && 'name' in res.data) {
                  this.setState(() => ({
                    result: res.data
                  }));
                }
              }).catch(error => {
                  this.setState(() => ({
                  'error': `Error: ${error.message}`
                  }));
              });
          }else{
            /* node has childs
            * remove all selects after current and concat with response data
            */
            this.setState(() => ({
              data: this.state.data.slice(0, depth+1).concat([res.data]),
              result: null
            }));
          }
        }).catch(error => {
            this.setState(() => ({
              'error': `Error: ${error.message}`
            }));
        });
    }
  }

  /** Return label for select based on depth(index) */
  getLabel(depth) {
    const labels = this.props.labels;
    if (labels && depth < labels.length) {
      return labels[depth];
    }
    return '';
  }


  render() {
    return (
      <div>
        {this.state.error
          ? <div className='TreeToSelects-error'>
              <p> Something went wrong, please reload your page and try again.</p>
            </div>
          : <div>
              {this.state.result &&
              <div className='TreeToSelects-result'>
                  <h5 className='TreeToSelects-fullCode'>{this.state.result.name}</h5>
                  <p>Description: {this.state.result.description}</p>
              </div>
              }
              {this.state.data.map((options, index) =>
                <Select key={index} depth={index} options={options} label={this.getLabel(index)}
                        onChange={this.handleSelectChange} />
              )}
            </div>
        }
      </div>
    );
  }
}

TreeToSelects.propTypes = {
  /** Complete url to root nodes */
  rootNodesUrl: PropTypes.string.isRequired,
  /** Url to child nodes ending with '/', parentId will be added */
  childNodesUrl: PropTypes.string.isRequired,
  /** Url to specific node data ending with '/', Id will be added */
  nodeDataUrl: PropTypes.string.isRequired,
  /** Array of labels based on depth ['Depth 1 label', 'Depth 2 level', etc.]
      where index of the array is depth
  */
  labels: PropTypes.array
}
