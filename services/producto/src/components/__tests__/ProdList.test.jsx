import React from 'react';
import { shallow } from 'enzyme';

import ProdList from '../ProdList';

const products = [
  {

    'id': 1,
    'nomb': 'A',
    'cat': 'S',
    'cod': '1',
    'stoc': '5',
    'prec': '1'
  },
  {

    'id': 2,
    'nomb': 'T',
    'cat': 'Z',
    'cod': '3',
    'stoc': '6',
    'prec': '10'
  }
];

test('ProdList renders properly', () => {
  const wrapper = shallow(<ProdList products={products}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(1).props.children).toBe('A');
});

