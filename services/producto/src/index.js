import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';  // nuevo
 
 
class App extends Component {
  constructor() {
	super();
  }
  // nuevo
  getProducts() {
	axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/products`)
	.then((res) => { console.log(res); })
	.catch((err) => { console.log(err); });
  }
  render() {
	return (
  	<section className="section">
    	<div className="container">
      	<div className="columns">
      	  <div className="column is-one-third">
          	<br/>
          	<h1 className="title is-1">Todos los Productos</h1>
          	<hr/><br/>
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

