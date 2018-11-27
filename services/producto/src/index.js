import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';  // new
import ProdList from './components/ProdList';
import AddProduct from './components/AddProduct';

class App extends Component {
  constructor() {
    super();
    // new
  this.state = {
    products: []
  };
  };
  componentDidMount() {
    this.getProducts();
  };

  getProducts() {
  axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/products`)  // new
  .then((res) => { this.setState({ products: res.data.data.products }); })
  .catch((err) => { console.log(err); });
};

  render() {
  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <div className="column is-one-third">
            <br/>
            <h1 className="title is-1">Todos los Productos</h1>
            <hr/><br/>
            <ProdList products={this.state.products}/>
          </div>
        </div>
      </div>
    </section>
  )
  }

};


ReactDOM.render(
  <App />,
  document.getElementById('root')
);
