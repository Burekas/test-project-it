import React from 'react';
import './App.css';
import TreeToSelects from './components/TreeToSelects';


const baseUrl = "http://127.0.0.1:8080"
const rootNodesUrl = `${baseUrl}/api/v1/get-root-nodes`;
// get-child-nodes/parentId
const childNodesUrl = `${baseUrl}/api/v1/get-child-nodes/`;
// get-node-data/id
const nodeDataUrl = `${baseUrl}/api/v1/get-node-data/`
// Specify labels for tree, index == depth of node
const labels = ['Education Standard', 'Grade Level', 'Learning Domain', 'Alignment Tag']

const App = () => (
  <div className="App">
    <header className="App-header">
      <h1 className="App-title">Test Project IT</h1>
    </header>
    <TreeToSelects rootNodesUrl={rootNodesUrl} childNodesUrl={childNodesUrl}
      nodeDataUrl={nodeDataUrl} labels={labels} />
  </div>
)

export default App;
