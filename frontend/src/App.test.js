import React from 'react';
import ReactDOM from 'react-dom';
import renderer from 'react-test-renderer';
import Enzyme, { shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import App from './App';
import Select from './components/Select';

Enzyme.configure({ adapter: new Adapter() });

describe('App', () => {

  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<App />, div);
    ReactDOM.unmountComponentAtNode(div);
  });

  test('has a valid snapshot', () => {
    const comp = renderer.create(<App />);
    const tree = comp.toJSON();
    expect(tree).toMatchSnapshot();
  });
});


describe('Select', () => {
    const props = {
        options: [
         {_id: '1', name: 'First'},
         {_id: '2', name: 'Second'},
        ],
        onChange: () => {},
        depth: 1,
        label: 'Label'
    };

    it('renders without crashing', () => {
        const div = document.createElement('div');
        ReactDOM.render(<Select { ...props } />, div);
    });

    it('shows tree options', () => {
        const element = shallow(<Select { ...props } />);
        /** third option is empty */
        expect(element.find('option').length).toBe(3);
    });

    test('has a valid snapshot', () => {
      const comp = renderer.create(<Select { ...props } />);
      const tree = comp.toJSON();
      expect(tree).toMatchSnapshot();
    });
});
