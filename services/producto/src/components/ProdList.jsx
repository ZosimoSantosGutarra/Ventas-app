import React from 'react';

const ProdList = (props) => {
  return (
    <div>
      {
        props.products.map((prod) => {
          return (
            <h4
              key={prod.id}
              className="box title is-4"
            >{prod.nomb}
            </h4>
          )
        })
      }
    </div>
  )
};

export default ProdList;
